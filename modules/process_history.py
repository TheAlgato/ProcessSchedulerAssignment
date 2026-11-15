"""Bounded histories for process drilldown; identity protects against PID reuse."""

from collections import deque


class ProcessHistory:
    def __init__(self, limit=120):
        self.limit = limit
        self._history = {}

    def update(self, timestamp, processes):
        active = set()
        for process in processes:
            key = (process['pid'], process['created_at'])
            active.add(key)
            history = self._history.setdefault(key, deque(maxlen=self.limit))
            history.append({'recorded_at': timestamp, 'cpu_percent': process['cpu_percent'],
                            'memory_mib': process['memory_bytes'] / 1024**2})
        self._history = {key: rows for key, rows in self._history.items() if key in active}

    def for_process(self, pid, created_at):
        return list(self._history.get((pid, created_at), []))
