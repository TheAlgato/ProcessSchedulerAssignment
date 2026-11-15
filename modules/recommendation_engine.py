"""Explain resource pressure without modifying running processes."""


def recommendations(system, processes, anomalies, prediction):
    advice = []
    for metric, threshold, label in [('cpu_percent', 90, 'CPU'), ('memory_percent', 85, 'memory')]:
        value = system.get(metric)
        if value is not None and value >= threshold:
            candidates = [p for p in processes if p.get(metric) is not None]
            top = max(candidates, key=lambda p: p[metric], default=None)
            suffix = f" Start by reviewing {top['name']} (PID {top['pid']})." if top else ''
            advice.append(f"System {label} usage is {value:.1f}%.{suffix}")
    if anomalies:
        advice.append(f'{len(anomalies)} process(es) have unusual resource profiles compared with other processes. Investigate whether their workloads are expected.')
    if system.get('disk_percent') is not None and system['disk_percent'] >= 90:
        advice.append('The monitored filesystem is at least 90% full. Review large files and available space before starting disk-heavy work.')
    if system.get('swap_percent') is not None and system['swap_percent'] >= 85:
        advice.append('Swap usage is at least 85%. Review memory-intensive applications and watch available memory.')
    if prediction and (prediction['cpu_percent'] >= 90 or prediction['memory_percent'] >= 85):
        advice.append('The five-minute estimate suggests possible resource pressure; continue monitoring before taking action.')
    if not advice:
        advice.append('No high utilization threshold is currently exceeded. Continue monitoring for changes.')
    return advice
