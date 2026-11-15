import os
import subprocess
import sys
import time
import unittest
from unittest.mock import Mock, patch

import psutil

from modules.process_control import ProcessControlError, control_process


class ProcessControlTests(unittest.TestCase):
    def setUp(self):
        self.current = Mock(pid=200)
        self.current.parents.return_value = [Mock(pid=100)]
        self.current.username.return_value = 'owner'
        self.target = Mock(pid=300)
        self.target.create_time.return_value = 123.0
        self.target.is_running.return_value = True
        self.target.username.return_value = 'owner'
        self.target.status.return_value = psutil.STATUS_SLEEPING

    def run_action(self, action='suspend', created=123.0, pid=300):
        with patch('modules.process_control.psutil.Process', side_effect=[self.current, self.target]):
            return control_process(pid, created, action)

    def test_sends_only_the_requested_action(self):
        for action in ('suspend', 'resume', 'terminate'):
            self.target.reset_mock()
            self.assertIn('request sent', self.run_action(action))
            getattr(self.target, action).assert_called_once_with()
            for other in {'suspend', 'resume', 'terminate'} - {action}:
                getattr(self.target, other).assert_not_called()

    def test_stale_pid_is_never_signalled(self):
        with self.assertRaisesRegex(ProcessControlError, 'PID was reused'):
            self.run_action(created=122.0)
        self.target.suspend.assert_not_called()

    def test_protects_dashboard_ancestors_and_system_pids(self):
        for pid in (0, 1, 100, 200):
            with self.subTest(pid=pid), self.assertRaises(ProcessControlError):
                self.run_action(pid=pid)
        self.target.suspend.assert_not_called()

    def test_other_account_and_zombie_processes_are_blocked(self):
        self.target.username.return_value = 'system'
        with self.assertRaisesRegex(ProcessControlError, 'owned'):
            self.run_action()
        self.target.username.return_value = 'owner'
        self.target.status.return_value = psutil.STATUS_ZOMBIE
        with self.assertRaisesRegex(ProcessControlError, 'already exited'):
            self.run_action()
        self.target.suspend.assert_not_called()

    def test_permission_and_exit_errors_have_actionable_messages(self):
        for error, message in [(psutil.AccessDenied(300), 'denied access'),
                               (psutil.NoSuchProcess(300), 'has exited')]:
            self.target.suspend.side_effect = error
            with self.subTest(error=error), self.assertRaisesRegex(ProcessControlError, message):
                self.run_action()

    def test_rejects_unknown_actions_and_invalid_identities(self):
        for pid, created, action in [(300, 123, 'kill'), (True, 123, 'suspend'),
                                     (300, float('nan'), 'suspend'), (300, None, 'suspend')]:
            with self.subTest(pid=pid, created=created), self.assertRaises(ProcessControlError):
                control_process(pid, created, action)

    @unittest.skipIf(os.name == 'nt', 'Real process lifecycle is verified on POSIX; Windows requires a Windows run.')
    def test_real_disposable_child_can_be_suspended_resumed_and_terminated(self):
        try:
            psutil.Process().parents()
        except (psutil.Error, OSError) as error:
            self.skipTest(f'This environment blocks OS process inspection: {error}')
        # This test acts only on the child it creates, never an existing user app.
        child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])
        try:
            process = psutil.Process(child.pid)
            created = process.create_time()
            control_process(child.pid, created, 'suspend')
            deadline = time.monotonic() + 3
            while process.status() != psutil.STATUS_STOPPED and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertEqual(process.status(), psutil.STATUS_STOPPED)
            control_process(child.pid, created, 'resume')
            deadline = time.monotonic() + 3
            while process.status() == psutil.STATUS_STOPPED and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertNotEqual(process.status(), psutil.STATUS_STOPPED)
            control_process(child.pid, created, 'terminate')
            child.wait(timeout=3)
            self.assertIsNotNone(child.returncode)
        finally:
            if child.poll() is None:
                process.resume()
                child.kill()
                child.wait(timeout=3)


if __name__ == '__main__':
    unittest.main()
