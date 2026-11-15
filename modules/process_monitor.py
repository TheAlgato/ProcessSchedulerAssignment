"""Collect process metrics without altering the processes being observed."""

import time

import psutil
from modules.system_monitor import counter_rate


class ProcessMonitor:
    """Measure CPU over successive snapshots, keyed by PID and creation time."""

    def __init__(self):
        self._previous = {}

    def sample(self):
        current = {}
        processes = []
        for process in psutil.process_iter():
            try:
                with process.oneshot():
                    pid = process.pid
                    created = process.create_time()
                    cpu_times = process.cpu_times()
                    cpu_total = cpu_times.user + cpu_times.system
                    now = time.monotonic()
                    key = (pid, created)
                    previous = self._previous.get(key)
                    # psutil's process convention: 100% means one fully used core.
                    cpu = None
                    if previous and now > previous[0] and cpu_total >= previous[1]:
                        cpu = 100 * (cpu_total - previous[1]) / (now - previous[0])
                    try:
                        io = process.io_counters()
                        read_bytes, write_bytes = io.read_bytes, io.write_bytes
                    except (psutil.Error, AttributeError, NotImplementedError, OSError):
                        read_bytes = write_bytes = None
                    current[key] = (now, cpu_total, read_bytes, write_bytes)
                    elapsed = now - previous[0] if previous else 0
                    processes.append({
                        "pid": pid, "name": process.name(), "status": process.status(),
                        "created_at": created, "elapsed_seconds": max(0, time.time() - created),
                        "cpu_percent": cpu, "memory_percent": process.memory_percent(),
                        "memory_bytes": process.memory_info().rss, "threads": process.num_threads(),
                        "read_bytes": read_bytes, "write_bytes": write_bytes,
                        "read_bytes_per_sec": counter_rate(previous[2] if previous else None, read_bytes, elapsed),
                        "write_bytes_per_sec": counter_rate(previous[3] if previous else None, write_bytes, elapsed),
                    })
            except (psutil.Error, OSError):
                # Processes can exit or become inaccessible between any two calls.
                continue
        self._previous = current
        return processes
