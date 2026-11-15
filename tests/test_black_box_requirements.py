"""Requirement-driven UI checks using controlled OS inputs, not live OS evidence.

Run: python -m unittest discover -s tests -p test_black_box_requirements.py -v
Only the OS collection/action boundary is substituted. Assertions use displayed
widgets, tables and messages; no application helper functions are called.
"""

from pathlib import Path
from copy import deepcopy
import time
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from modules.process_control import ProcessControlError


ROOT = Path(__file__).resolve().parents[1]


def widget(elements, label):
    return next(element for element in elements if element.label == label)


class BlackBoxRequirementTests(unittest.TestCase):
    def setUp(self):
        base = dict(created_at=123.0, status='sleeping', threads=1,
                    elapsed_seconds=10, read_bytes=None, write_bytes=None,
                    read_bytes_per_sec=None, write_bytes_per_sec=None)
        self.processes = [
            dict(base, pid=300, name='Alpha-worker', cpu_percent=19.9,
                 memory_percent=4.9, memory_bytes=1048576),
            dict(base, pid=301, name='Beta-worker', cpu_percent=20.0,
                 memory_percent=5.0, memory_bytes=2097152),
            dict(base, pid=302, name='Gamma-worker', cpu_percent=145.0,
                 memory_percent=6.0, memory_bytes=3145728),
        ]
        self.system = dict(cpu_percent=20.0, memory_percent=30.0,
                           memory_total_bytes=1024**3, disk_percent=40.0)
        for name, value in (
            ('modules.process_monitor.ProcessMonitor.sample', self.processes),
            ('modules.system_monitor.SystemMonitor.sample', self.system),
        ):
            patcher = patch(name, side_effect=lambda source=value: deepcopy(source))
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = patch('modules.process_control.control_process',
                        return_value='Action request sent to selected PID.')
        self.action = patcher.start()
        self.addCleanup(patcher.stop)
        self.app = AppTest.from_file(str(ROOT / 'dashboard.py'), default_timeout=20)

    def open(self, page='Overview'):
        self.app.run()
        for label in ('Set up monitoring →', 'Allow monitoring',
                      'Use session only', 'Open dashboard'):
            widget(self.app.button, label).click().run()
        if page != 'Overview':
            widget(self.app.radio, 'Workspace view').set_value(page).run()
        self.assertFalse(self.app.exception)

    def table(self):
        return next(item.value for item in self.app.dataframe
                    if 'PID' in item.value.columns and 'Status' in item.value.columns)

    def pressure_warning(self):
        return any('High resource usage' in item.value for item in self.app.warning)

    def review(self, action):
        self.open('Processes')
        widget(self.app.toggle, 'Enable process controls').set_value(True).run()
        widget(self.app.selectbox, 'Process').set_value((300, 123.0)).run()
        widget(self.app.selectbox, 'Action').set_value(action).run()
        widget(self.app.button, 'Review action').click().run()

    def test_BB01_dashboard_and_all_workspace_views(self):
        self.open()
        self.assertEqual(widget(self.app.selectbox, 'Refresh interval').value, 2)
        self.assertFalse(widget(self.app.toggle, 'Enable process controls').value)
        for page in ('Overview', 'Processes', 'Analysis', 'Diagnostics'):
            widget(self.app.radio, 'Workspace view').set_value(page).run()
            self.assertFalse(self.app.exception, page)
            self.assertEqual(widget(self.app.metric, 'CPU').value, '20.0%')
            self.assertEqual(widget(self.app.metric, 'RAM').value, '30.0%')

    def test_BB02_process_identity_state_cpu_and_memory(self):
        self.processes[0]['status'] = 'stopped'
        self.open('Processes')
        row = self.table().set_index('PID').loc[300]
        self.assertEqual(row['Name'], 'Alpha-worker')
        self.assertEqual(row['Status'], 'stopped')
        self.assertAlmostEqual(row['CPU %'], 19.9)
        self.assertAlmostEqual(row['Memory %'], 4.9)
        self.assertEqual(row['RAM (MiB)'], 1.0)
        self.assertEqual(self.table().set_index('PID').loc[302, 'CPU %'], 145.0)

    def test_BB03_search_name_pid_and_no_match(self):
        self.open('Processes')
        for query, expected in [('ALPHA', [300]), ('301', [301])]:
            widget(self.app.text_input, 'Search').set_value(query).run()
            self.assertEqual(self.table()['PID'].tolist(), expected)
        widget(self.app.text_input, 'Search').set_value('no-such-process').run()
        self.assertTrue(any('No visible processes match' in item.value for item in self.app.info))
        self.assertFalse(self.app.exception)

    def test_BB04_usage_filter_boundaries(self):
        self.open('Processes')
        for label in ('High CPU (≥ 20%)', 'High memory (≥ 5%)'):
            widget(self.app.selectbox, 'Show').set_value(label).run()
            self.assertEqual(set(self.table()['PID']), {301, 302})

    def test_BB05_sorting(self):
        self.open('Processes')
        for label, expected in [('CPU', [302, 301, 300]), ('Memory', [302, 301, 300]),
                                ('Name', [300, 301, 302]), ('PID', [300, 301, 302])]:
            widget(self.app.selectbox, 'Sort by').set_value(label).run()
            self.assertEqual(self.table()['PID'].tolist(), expected)

    def test_BB06_unavailable_cpu_and_io(self):
        self.system['cpu_percent'] = None
        self.processes[0]['cpu_percent'] = None
        self.open('Processes')
        self.assertEqual(widget(self.app.metric, 'CPU').value, 'Warming up')
        import pandas as pd
        self.assertTrue(pd.isna(self.table().set_index('PID').loc[300, 'CPU %']))
        self.assertTrue(self.table()['Read MiB/s'].isna().all())
        self.assertFalse(self.app.exception)

    def test_BB07_empty_process_snapshot(self):
        self.processes.clear()
        self.open('Processes')
        self.assertEqual(widget(self.app.metric, 'PROCESSES').value, '0')
        self.assertTrue(any('No visible processes match' in item.value for item in self.app.info))
        self.assertFalse(any(item.label == 'Process' for item in self.app.selectbox))
        self.assertFalse(self.app.exception)

    def test_BB08_cpu_warning_below_at_and_above_threshold(self):
        for value, expected in [(89.9, False), (90.0, True), (90.1, True)]:
            with self.subTest(cpu=value):
                self.system['cpu_percent'] = value
                self.app = AppTest.from_file(str(ROOT / 'dashboard.py'), default_timeout=20)
                self.open('Analysis')
                self.assertEqual(self.pressure_warning(), expected)
                self.assertEqual(widget(self.app.metric, 'CPU · threshold 90%').value,
                                 'High' if expected else 'Below')

    def test_BB09_memory_warning_below_at_and_above_threshold(self):
        for value, expected in [(84.9, False), (85.0, True), (85.1, True)]:
            with self.subTest(memory=value):
                self.system['memory_percent'] = value
                self.app = AppTest.from_file(str(ROOT / 'dashboard.py'), default_timeout=20)
                self.open('Analysis')
                self.assertEqual(self.pressure_warning(), expected)
                self.assertEqual(widget(self.app.metric, 'Memory · threshold 85%').value,
                                 'High' if expected else 'Below')

    def test_BB10_pressure_and_zombie_warnings_across_views(self):
        self.system['cpu_percent'] = 90.0
        self.processes[0]['status'] = 'zombie'
        self.open()
        for page in ('Overview', 'Processes', 'Analysis', 'Diagnostics'):
            widget(self.app.radio, 'Workspace view').set_value(page).run()
            self.assertTrue(self.pressure_warning())
            self.assertTrue(any('1 zombie' in item.value for item in self.app.warning))
            self.assertFalse(self.app.exception)

    def test_BB11_warning_identifies_largest_consumer(self):
        self.system['cpu_percent'] = 95.0
        self.system['memory_percent'] = 87.0
        self.open('Analysis')
        text = '\n'.join(item.value for item in self.app.markdown)
        self.assertIn('System CPU usage is 95.0%. Start by reviewing Gamma-worker (PID 302).', text)
        self.assertIn('System memory usage is 87.0%. Start by reviewing Gamma-worker (PID 302).', text)
        self.action.assert_not_called()

    def test_BB12_each_confirmed_action_dispatches_once(self):
        for action in ('suspend', 'resume', 'terminate'):
            with self.subTest(action=action):
                self.app = AppTest.from_file(str(ROOT / 'dashboard.py'), default_timeout=20)
                self.action.reset_mock()
                self.review(action)
                self.action.assert_not_called()
                widget(self.app.text_input, 'Type the target PID to confirm').set_value('300')
                widget(self.app.button, 'Confirm action').click().run()
                self.action.assert_called_once_with(300, 123.0, action)
                self.assertTrue(any('Action request sent' in item.value for item in self.app.info))
                self.app.run()
                self.action.assert_called_once()
                self.assertFalse(self.app.exception)

    def test_BB13_blank_wrong_and_nonnumeric_confirmations(self):
        self.review('terminate')
        for value in ('', '301', 'abc', '-1'):
            widget(self.app.text_input, 'Type the target PID to confirm').set_value(value)
            widget(self.app.button, 'Confirm action').click().run()
            self.assertTrue(any('PID does not match' in item.value for item in self.app.error))
            self.action.assert_not_called()
        widget(self.app.button, 'Cancel').click().run()
        self.assertFalse(any(item.label == 'Confirm action' for item in self.app.button))
        self.action.assert_not_called()

    def test_BB14_os_denial_is_visible(self):
        self.review('suspend')
        self.action.side_effect = ProcessControlError('The operating system denied access.')
        widget(self.app.text_input, 'Type the target PID to confirm').set_value('300')
        widget(self.app.button, 'Confirm action').click().run()
        self.assertTrue(any('denied access' in item.value for item in self.app.info))
        self.assertFalse(self.app.exception)

    def test_BB15_refresh_pause_and_resume(self):
        self.open()
        widget(self.app.selectbox, 'Refresh interval').set_value(1)
        widget(self.app.button, 'Apply settings').click().run()
        self.system['cpu_percent'] = 42.0
        time.sleep(1.1)
        self.app.run()
        self.assertEqual(widget(self.app.metric, 'CPU').value, '42.0%')
        widget(self.app.toggle, 'Pause collection').set_value(True).run()
        self.system['cpu_percent'] = 55.0
        time.sleep(1.1)
        self.app.run()
        self.assertEqual(widget(self.app.metric, 'CPU').value, '42.0%')
        self.assertTrue(any('Paused' in item.value for item in self.app.markdown))
        widget(self.app.toggle, 'Pause collection').set_value(False).run()
        self.assertEqual(widget(self.app.metric, 'CPU').value, '55.0%')
        self.assertFalse(self.app.exception)


if __name__ == '__main__':
    unittest.main()
