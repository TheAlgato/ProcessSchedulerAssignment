import unittest
from contextlib import nullcontext
from collections import namedtuple
from unittest.mock import Mock, patch

from modules.system_monitor import cpu_utilization, counter_rate, SystemMonitor
from modules.process_history import ProcessHistory
from modules.resource_predictor import ResourcePredictor
from modules.process_monitor import ProcessMonitor


class MonitoringTests(unittest.TestCase):
    def test_process_intervals_io_rates_and_pid_reuse(self):
        process = Mock(pid=42)
        process.oneshot.side_effect = lambda: nullcontext()
        process.create_time.side_effect = [10, 10, 11]
        process.cpu_times.side_effect = [Mock(user=n, system=0) for n in (1, 2, 4)]
        process.io_counters.side_effect = [Mock(read_bytes=n, write_bytes=n) for n in (100, 2100, 3100)]
        process.name.return_value = 'worker'
        process.status.return_value = 'running'
        process.memory_percent.return_value = 1
        process.memory_info.return_value = Mock(rss=1024)
        process.num_threads.return_value = 1
        with patch('modules.process_monitor.psutil.process_iter', return_value=[process]), \
             patch('modules.process_monitor.time.monotonic', side_effect=[1, 3, 5]):
            monitor = ProcessMonitor()
            self.assertIsNone(monitor.sample()[0]['cpu_percent'])
            reading = monitor.sample()[0]
            self.assertEqual(reading['cpu_percent'], 50)
            self.assertEqual(reading['read_bytes_per_sec'], 1000)
            reused = monitor.sample()[0]
            self.assertIsNone(reused['cpu_percent'])
            self.assertIsNone(reused['read_bytes_per_sec'])

    def test_cpu_excludes_guest_and_iowait(self):
        Times = namedtuple('Times', 'user system idle iowait guest')
        # 20 busy ticks, 60 idle ticks, 20 waiting; guest already in user.
        result = cpu_utilization(Times(0, 0, 0, 0, 0), Times(15, 5, 60, 20, 5))
        self.assertAlmostEqual(result, 20)

    def test_counter_rate_never_fabricates_reset_or_first_rates(self):
        self.assertEqual(counter_rate(100, 200, 2), 50)
        self.assertIsNone(counter_rate(None, 200, 2))
        self.assertIsNone(counter_rate(200, 100, 2))
        self.assertIsNone(counter_rate(100, 200, 0))

    def test_system_cpu_uses_owned_counters_instead_of_thread_local_percent(self):
        Times = namedtuple('Times', 'user system idle')
        before, after = Times(0, 0, 0), Times(2, 1, 7)
        with patch('modules.system_monitor.psutil.cpu_times', side_effect=[before, [before], after, [after]]), \
             patch('modules.system_monitor.psutil.cpu_percent', side_effect=AssertionError('thread dependent call')), \
             patch('modules.system_monitor.psutil.virtual_memory', return_value=Mock(percent=20, used=2, available=8, total=10)), \
             patch('modules.system_monitor.psutil.swap_memory', return_value=Mock(percent=0, used=0)), \
             patch('modules.system_monitor.psutil.disk_usage', return_value=Mock(percent=30)):
            monitor = SystemMonitor('/')
            self.assertEqual(monitor.sample()['cpu_percent'], 30)

    def test_process_history_is_bounded_and_handles_pid_reuse(self):
        history = ProcessHistory(limit=2)
        process = dict(pid=1, created_at=1, cpu_percent=10, memory_bytes=1024)
        for i in range(3):
            history.update(str(i), [process])
        self.assertEqual(len(history.for_process(1, 1)), 2)
        history.update('new', [dict(process, created_at=2)])
        self.assertEqual(history.for_process(1, 1), [])
        self.assertEqual(len(history.for_process(1, 2)), 1)

    def test_predictor_reuses_result_between_training_intervals(self):
        with patch('modules.resource_predictor.time.monotonic', side_effect=[0, 5, 65]), \
             patch('modules.resource_predictor.predict_resources', return_value={'cpu_percent': 10}) as fit:
            predictor = ResourcePredictor()
            predictor.predict([])
            predictor.predict([])
            self.assertEqual(fit.call_count, 1)
            predictor.predict([])
            self.assertEqual(fit.call_count, 2)


if __name__ == '__main__':
    unittest.main()
