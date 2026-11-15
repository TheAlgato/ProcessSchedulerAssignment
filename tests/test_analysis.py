import unittest
from datetime import datetime, timedelta, timezone

from modules.anomaly_detector import detect_anomalies
from modules.resource_predictor import predict_resources, forecast_readiness
from modules.recommendation_engine import recommendations


class AnalysisTests(unittest.TestCase):
    def test_anomaly_needs_enough_processes(self):
        self.assertIsNone(detect_anomalies([]))

    def test_anomaly_detects_extreme_profile(self):
        data = [dict(pid=i, created_at=1, cpu_percent=1, memory_percent=1) for i in range(39)]
        data.append(dict(pid=99, created_at=1, cpu_percent=300, memory_percent=50))
        self.assertIn((99, 1), detect_anomalies(data))

    def test_forecast_requires_history_and_rejects_gaps(self):
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        data = [dict(recorded_at=(start + timedelta(seconds=i * 60)).isoformat(),
                     cpu_percent=i % 100, memory_percent=40) for i in range(30)]
        self.assertIsNone(predict_resources(data[:10]))
        forecast = predict_resources(data)
        self.assertEqual(forecast['horizon_seconds'], 300)
        self.assertGreaterEqual(forecast['training_pairs'], 20)
        self.assertTrue(0 <= forecast['cpu_percent'] <= 100)
        sparse = [dict(row, recorded_at=(start + timedelta(hours=i)).isoformat()) for i, row in enumerate(data)]
        self.assertIsNone(predict_resources(sparse))

    def test_recommendations_name_high_cpu_process(self):
        advice = recommendations({'cpu_percent': 95, 'memory_percent': 50},
                                 [{'pid': 12, 'name': 'worker', 'cpu_percent': 80}], None, None)
        self.assertIn('worker', advice[0])

    def test_forecast_reports_honest_validation_and_constant_baseline(self):
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        data = [dict(recorded_at=(start + timedelta(seconds=i * 10)).isoformat(),
                     cpu_percent=20, memory_percent=50) for i in range(180)]
        result = predict_resources(data)
        self.assertGreater(result['validation_pairs'], 0)
        self.assertEqual(result['methods'], ['Persistence baseline', 'Persistence baseline'])
        self.assertEqual(result['baseline_mae'], [0, 0])

    def test_equal_process_profiles_do_not_force_anomalies(self):
        data = [dict(pid=i, created_at=1, cpu_percent=1, memory_percent=1) for i in range(40)]
        self.assertEqual(detect_anomalies(data), set())

    def test_forecast_readiness_counts_actual_five_minute_pairs(self):
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        data = [dict(recorded_at=(start + timedelta(seconds=i * 10)).isoformat(),
                     cpu_percent=20, memory_percent=50) for i in range(50)]
        self.assertEqual(forecast_readiness(data)['valid_pairs'], 20)
        self.assertEqual(forecast_readiness(data[:20])['valid_pairs'], 0)


if __name__ == '__main__':
    unittest.main()
