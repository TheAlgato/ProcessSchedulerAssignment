"""Store each sample atomically in a local SQLite database."""

import sqlite3
import json
from contextlib import closing
from pathlib import Path


class DatabaseManager:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute('PRAGMA journal_mode=WAL')
            db.executescript("""
                CREATE TABLE IF NOT EXISTS system_samples (
                    id INTEGER PRIMARY KEY, recorded_at TEXT NOT NULL,
                    cpu_percent REAL, memory_percent REAL, memory_used_bytes INTEGER,
                    memory_total_bytes INTEGER, disk_percent REAL, process_count INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS process_samples (
                    sample_id INTEGER NOT NULL REFERENCES system_samples(id), pid INTEGER NOT NULL,
                    name TEXT, status TEXT, created_at REAL, elapsed_seconds REAL,
                    cpu_percent REAL, memory_percent REAL, memory_bytes INTEGER,
                    threads INTEGER, read_bytes INTEGER, write_bytes INTEGER
                );
                CREATE INDEX IF NOT EXISTS process_sample_idx ON process_samples(sample_id);
            """)
            db.execute('BEGIN IMMEDIATE')
            for table in ('system_samples', 'process_samples'):
                columns = {row[1] for row in db.execute(f'PRAGMA table_info({table})')}
                if 'extra_metrics' not in columns:
                    db.execute(f"ALTER TABLE {table} ADD COLUMN extra_metrics TEXT NOT NULL DEFAULT '{{}}'")

    def save_sample(self, recorded_at, system, processes):
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute('PRAGMA foreign_keys=ON')
            cursor = db.execute(
                "INSERT INTO system_samples (recorded_at, cpu_percent, memory_percent, "
                "memory_used_bytes, memory_total_bytes, disk_percent, process_count) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (recorded_at, system['cpu_percent'], system['memory_percent'],
                 system['memory_used_bytes'], system['memory_total_bytes'], system['disk_percent'], len(processes)))
            db.execute('UPDATE system_samples SET extra_metrics=? WHERE id=?',
                       (json.dumps(system, allow_nan=False), cursor.lastrowid))
            fields = ('pid', 'name', 'status', 'created_at', 'elapsed_seconds', 'cpu_percent',
                      'memory_percent', 'memory_bytes', 'threads', 'read_bytes', 'write_bytes')
            db.executemany("INSERT INTO process_samples (sample_id, " + ', '.join(fields) + ", extra_metrics) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           [(cursor.lastrowid, *(p[field] for field in fields),
                             json.dumps({key: p.get(key) for key in ('read_bytes_per_sec', 'write_bytes_per_sec')}))
                            for p in processes])
            return cursor.lastrowid

    def system_history(self, limit=2000):
        with closing(sqlite3.connect(self.path)) as db:
            db.row_factory = sqlite3.Row
            rows = db.execute('SELECT recorded_at, cpu_percent, memory_percent, disk_percent, process_count '
                              'FROM system_samples ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
            return [dict(row) for row in reversed(rows)]
