import unittest

import pandas as pd

from visualization.charts import forecast_chart, history_chart, memory_chart, top_process_chart


class ChartTests(unittest.TestCase):
    def test_current_metrics_are_represented(self):
        ring = memory_chart(64)
        self.assertEqual(list(ring.data[0].values), [64, 36])
        processes = [{'name': 'worker', 'pid': 3, 'cpu_percent': 150}]
        bars = top_process_chart(processes, 'cpu_percent')
        self.assertEqual(list(bars.data[0].x), [150])
        self.assertIsNone(top_process_chart([], 'cpu_percent'))

    def test_history_and_forecast_use_input_values(self):
        history = pd.DataFrame([{'recorded_at': '2026-01-01', 'cpu_percent': 20,
                                 'memory_percent': 50, 'disk_percent': None}])
        chart = history_chart(history)
        self.assertEqual(list(chart.data[0].y), [20])
        forecast = forecast_chart({'cpu_percent': 20, 'memory_percent': 50},
                                  {'cpu_percent': 30, 'memory_percent': 60})
        self.assertEqual(list(forecast.data[0].y), [20, 50])
        self.assertEqual(list(forecast.data[1].y), [30, 60])

    def test_dark_charts_use_readable_labels(self):
        chart = memory_chart(42, dark=True)
        self.assertEqual(chart.layout.font.color, '#b6c2d7')
        self.assertEqual(chart.layout.annotations[0].font.color, '#edf1fa')

    def test_history_separates_resources_without_changing_measurements(self):
        history = pd.DataFrame([{'recorded_at': '2026-01-01', 'cpu_percent': 20,
                                 'memory_percent': 75, 'disk_percent': 30}])
        chart = history_chart(history, focus=True)
        self.assertEqual([trace.yaxis for trace in chart.data], ['y', 'y2', 'y3'])
        self.assertEqual(list(chart.data[1].y), [75])
        self.assertEqual(list(chart.layout.yaxis2.range), [72, 78])

    def test_long_process_labels_keep_full_identity_on_hover(self):
        name = 'A very long process name that should not take over the chart'
        chart = top_process_chart([{'name': name, 'pid': 12, 'cpu_percent': 130}], 'cpu_percent')
        self.assertLess(len(chart.data[0].y[0]), len(name))
        self.assertEqual(chart.data[0].customdata[0][0], name)


if __name__ == '__main__':
    unittest.main()
