"""Exercise dashboard interactions with fixed OS readings and mocked actions."""

from pathlib import Path
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from modules.process_control import ProcessControlError


ROOT = Path(__file__).resolve().parents[1]


def widget(elements, label):
    return next(element for element in elements if element.label == label)


class DashboardTests(unittest.TestCase):
    def setUp(self):
        process = dict(pid=300, created_at=123.0, name='worker', status='sleeping',
                       cpu_percent=10.0, memory_percent=2.0, memory_bytes=1024**2,
                       threads=1, elapsed_seconds=10, read_bytes=None, write_bytes=None,
                       read_bytes_per_sec=None, write_bytes_per_sec=None)
        self.processes = [process, dict(process, pid=301, name='other-worker')]
        self.system = dict(cpu_percent=20.0, memory_percent=30.0,
                           memory_total_bytes=1024**3, disk_percent=40.0)
        for name, readings in [('modules.process_monitor.ProcessMonitor.sample', self.processes),
                               ('modules.system_monitor.SystemMonitor.sample', self.system)]:
            patcher = patch(name, return_value=readings)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = patch('modules.process_control.control_process', return_value='Suspend request sent to PID 300.')
        self.control = patcher.start()
        self.addCleanup(patcher.stop)
        self.app = AppTest.from_file(str(ROOT / 'dashboard.py'), default_timeout=20)

    def open_dashboard(self):
        self.app.session_state['setup_step'] = 'ready'
        self.app.session_state['save_history'] = False
        self.app.run()
        self.assertFalse(self.app.exception)

    def review_suspend(self):
        self.open_dashboard()
        widget(self.app.radio, 'Workspace view').set_value('Processes').run()
        widget(self.app.toggle, 'Enable process controls').set_value(True).run()
        widget(self.app.selectbox, 'Process').set_value((300, 123.0)).run()
        widget(self.app.button, 'Review action').click().run()

    def test_guide_reaches_dashboard_with_controls_off(self):
        self.app.run()
        for label in ('Set up monitoring →', 'Allow monitoring', 'Use session only', 'Open dashboard'):
            widget(self.app.button, label).click().run()
            self.assertFalse(self.app.exception)
        self.assertFalse(widget(self.app.toggle, 'Enable process controls').value)
        self.assertEqual(widget(self.app.selectbox, 'Refresh interval').value, 2)
        self.assertTrue(self.app.metric)
        for page in ('Processes', 'Analysis', 'Diagnostics', 'Overview'):
            widget(self.app.radio, 'Workspace view').set_value(page).run()
            self.assertFalse(self.app.exception, page)

    def test_review_wrong_pid_and_cancel_do_not_send_actions(self):
        self.review_suspend()
        self.control.assert_not_called()
        widget(self.app.text_input, 'Type the target PID to confirm').set_value('301')
        widget(self.app.button, 'Confirm action').click().run()
        self.assertTrue(any('PID does not match' in error.value for error in self.app.error))
        self.control.assert_not_called()
        widget(self.app.button, 'Cancel').click().run()
        self.assertNotIn('pending_action', self.app.session_state)
        self.control.assert_not_called()
        self.assertFalse(self.app.exception)

    def test_confirmation_uses_reviewed_target_after_selection_changes(self):
        self.review_suspend()
        widget(self.app.selectbox, 'Process').set_value((301, 123.0)).run()
        widget(self.app.selectbox, 'Action').set_value('resume').run()
        widget(self.app.text_input, 'Type the target PID to confirm').set_value('300')
        widget(self.app.button, 'Confirm action').click().run()
        self.assertFalse(self.app.exception)
        self.control.assert_called_once_with(300, 123.0, 'suspend')
        self.assertEqual(self.app.session_state['action_history'][-1]['outcome'], 'Request sent')
        self.assertNotIn('pending_action', self.app.session_state)
        self.app.run()
        self.control.assert_called_once()

    def test_os_denial_is_logged_and_does_not_crash_dashboard(self):
        self.review_suspend()
        self.control.side_effect = ProcessControlError('The operating system denied access.')
        widget(self.app.text_input, 'Type the target PID to confirm').set_value('300')
        widget(self.app.button, 'Confirm action').click().run()
        self.assertFalse(self.app.exception)
        self.assertEqual(self.app.session_state['action_history'][-1]['outcome'], 'Blocked or failed')
        self.assertIn('denied access', self.app.session_state['action_notice'])

    def test_disabling_controls_cancels_pending_action(self):
        self.review_suspend()
        widget(self.app.toggle, 'Enable process controls').set_value(False).run()
        self.assertNotIn('pending_action', self.app.session_state)
        self.assertFalse(any(button.label == 'Confirm action' for button in self.app.button))
        self.control.assert_not_called()

    def test_resource_pressure_and_zombies_are_visible_on_every_page(self):
        self.system['cpu_percent'] = 95.0
        self.processes[0]['status'] = 'zombie'
        self.open_dashboard()
        for page in ('Overview', 'Processes', 'Analysis', 'Diagnostics'):
            widget(self.app.radio, 'Workspace view').set_value(page).run()
            self.assertFalse(self.app.exception)
            warnings = [warning.value for warning in self.app.warning]
            self.assertTrue(any('High resource usage' in text for text in warnings))
            self.assertTrue(any('zombie' in text for text in warnings))


if __name__ == '__main__':
    unittest.main()
