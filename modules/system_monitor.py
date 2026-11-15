"""Instance-owned CPU baselines and portable system throughput measurements."""

import time

import psutil


def cpu_utilization(before, after):
    """Equivalent busy/total accounting to psutil, independent of calling thread."""
    if before is None or before._fields != after._fields:
        return None
    deltas = {field: max(0, getattr(after, field) - getattr(before, field)) for field in after._fields}
    total = sum(deltas.values()) - deltas.get('guest', 0) - deltas.get('guest_nice', 0)
    busy = total - deltas.get('idle', 0) - deltas.get('iowait', 0)
    return min(100.0, max(0.0, 100 * busy / total)) if total > 0 else None


def counter_rate(before, after, seconds):
    """No rate is known for a first reading, reset counter or zero interval."""
    if before is None or after is None or seconds <= 0 or after < before:
        return None
    return (after - before) / seconds


def optional_counter(function):
    try:
        return function()
    except (psutil.Error, OSError, AttributeError, NotImplementedError):
        return None


class SystemMonitor:
    def __init__(self, disk_path):
        self.disk_path = disk_path
        self._cpu = psutil.cpu_times()
        self._cores = psutil.cpu_times(percpu=True)
        self._disk = optional_counter(psutil.disk_io_counters)
        self._network = optional_counter(psutil.net_io_counters)
        self._time = time.monotonic()

    def sample(self):
        cpu = psutil.cpu_times()
        cores = psutil.cpu_times(percpu=True)
        disk = optional_counter(psutil.disk_io_counters)
        network = optional_counter(psutil.net_io_counters)
        now = time.monotonic()
        elapsed = now - self._time
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        usage = optional_counter(lambda: psutil.disk_usage(self.disk_path))
        rates = {}
        for prefix, previous, current, fields in [
            ('disk', self._disk, disk, ('read_bytes', 'write_bytes')),
            ('network', self._network, network, ('bytes_sent', 'bytes_recv')),
        ]:
            for field in fields:
                rates[f'{prefix}_{field}_per_sec'] = counter_rate(
                    getattr(previous, field, None), getattr(current, field, None), elapsed)
        result = {'cpu_percent': cpu_utilization(self._cpu, cpu),
                  'cpu_per_core': [cpu_utilization(old, new) for old, new in zip(self._cores, cores)] if len(cores) == len(self._cores) else [],
                  'memory_percent': memory.percent, 'memory_used_bytes': memory.used,
                  'memory_available_bytes': memory.available, 'memory_total_bytes': memory.total,
                  'swap_percent': swap.percent, 'swap_used_bytes': swap.used,
                  'disk_percent': usage.percent if usage else None, **rates}
        self._cpu, self._cores = cpu, cores
        self._disk, self._network, self._time = disk, network, now
        return result
