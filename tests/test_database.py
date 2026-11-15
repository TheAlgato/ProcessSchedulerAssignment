import sqlite3
import json
from contextlib import closing
import tempfile
import unittest
from pathlib import Path

from database.db_manager import DatabaseManager


class DatabaseTests(unittest.TestCase):
    def test_upgrades_original_schema_without_losing_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'old.db'
            with closing(sqlite3.connect(path)) as connection, connection:
                connection.execute('CREATE TABLE system_samples (id INTEGER PRIMARY KEY, recorded_at TEXT NOT NULL, '
                                   'cpu_percent REAL, memory_percent REAL, memory_used_bytes INTEGER, '
                                   'memory_total_bytes INTEGER, disk_percent REAL, process_count INTEGER NOT NULL)')
                connection.execute("INSERT INTO system_samples VALUES (1, 'old reading', 10, 20, 30, 40, 50, 0)")
            DatabaseManager(path)
            with closing(sqlite3.connect(path)) as connection:
                self.assertEqual(connection.execute('SELECT recorded_at, extra_metrics FROM system_samples').fetchone(),
                                 ('old reading', '{}'))

    def test_persists_sample_and_null_process_metrics(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'history.db'
            db = DatabaseManager(path)
            system = dict(cpu_percent=12.0, memory_percent=30.0, memory_used_bytes=300,
                          memory_total_bytes=1000, disk_percent=None)
            process = dict(pid=123, name='example', status='running', created_at=1.0,
                           elapsed_seconds=5.0, cpu_percent=None, memory_percent=1.0,
                           memory_bytes=10, threads=2, read_bytes=None, write_bytes=None)
            sample_id = db.save_sample('2026-01-01T00:00:00+00:00', system, [process])
            with closing(sqlite3.connect(path)) as connection:
                self.assertEqual(connection.execute('SELECT process_count, disk_percent FROM system_samples').fetchone(), (1, None))
                self.assertEqual(connection.execute('SELECT sample_id, pid, cpu_percent, read_bytes FROM process_samples').fetchone(), (sample_id, 123, None, None))
            # Reopening an existing database preserves observations and its schema.
            DatabaseManager(path)
            with closing(sqlite3.connect(path)) as connection:
                extras = connection.execute('SELECT extra_metrics FROM system_samples').fetchone()[0]
                self.assertEqual(json.loads(extras)['cpu_percent'], 12)

    def test_failed_process_insert_rolls_back_system_sample(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'history.db'
            db = DatabaseManager(path)
            system = dict(cpu_percent=1, memory_percent=2, memory_used_bytes=3,
                          memory_total_bytes=4, disk_percent=5)
            with self.assertRaises(KeyError):
                db.save_sample('now', system, [{}])
            with closing(sqlite3.connect(path)) as connection:
                self.assertEqual(connection.execute('SELECT count(*) FROM system_samples').fetchone()[0], 0)


if __name__ == '__main__':
    unittest.main()
