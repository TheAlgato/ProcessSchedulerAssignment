"""Run the first-stage collector from a terminal."""

import argparse
import json
import os
import math
import time
from datetime import datetime, timezone
from pathlib import Path

from database.db_manager import DatabaseManager
from modules.process_monitor import ProcessMonitor
from modules.system_monitor import SystemMonitor


def main():
    parser = argparse.ArgumentParser(description="Collect local OS performance samples")
    parser.add_argument('--interval', type=float, default=5, help='Seconds between samples (default: 5)')
    parser.add_argument('--samples', type=int, default=None, help='Stop after this many samples')
    parser.add_argument('--db', default='data/performance_history.db', help='SQLite database path')
    parser.add_argument('--disk-path', default=Path.cwd().anchor or os.path.abspath(os.sep),
                        help='Filesystem path whose disk capacity is monitored')
    args = parser.parse_args()
    if not math.isfinite(args.interval) or args.interval <= 0 or (args.samples is not None and args.samples < 1):
        parser.error('interval must be positive and samples must be at least 1')
    db = DatabaseManager(args.db)
    processes = ProcessMonitor()
    system = SystemMonitor(args.disk_path)
    # Establish baselines so the first persisted CPU sample has a real interval.
    processes.sample()
    count = 0
    try:
        while args.samples is None or count < args.samples:
            time.sleep(args.interval)
            timestamp = datetime.now(timezone.utc).isoformat()
            snapshot = processes.sample()
            metrics = system.sample()
            db.save_sample(timestamp, metrics, snapshot)
            print(json.dumps({'recorded_at': timestamp, **metrics, 'process_count': len(snapshot)}), flush=True)
            count += 1
    except KeyboardInterrupt:
        print('\nMonitoring stopped.')


if __name__ == '__main__':
    main()
