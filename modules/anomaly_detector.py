"""Identify unusual process resource profiles within the current snapshot."""

import numpy as np
from sklearn.ensemble import IsolationForest


def detect_anomalies(processes, minimum_samples=20):
    """Return PID/creation-time keys flagged as outliers, or None if insufficient data.

    Scores compare processes in this snapshot; they do not establish a process's
    historical baseline and should not be interpreted as proof of malfunction.
    """
    usable = [p for p in processes if p['cpu_percent'] is not None and p['memory_percent'] is not None]
    if len(usable) < minimum_samples:
        return None
    features = np.array([[np.log1p(max(0, p['cpu_percent'])),
                          np.log1p(max(0, p['memory_percent']))] for p in usable])
    if not np.isfinite(features).all():
        return None
    # An automatic threshold avoids labelling a fixed 5% of every snapshot.
    if np.all(np.ptp(features, axis=0) < 1e-12):
        return set()
    model = IsolationForest(n_estimators=60, contamination='auto', random_state=42, n_jobs=1).fit(features)
    # A tiny tolerance prevents floating-point noise at the threshold from
    # labelling otherwise identical resource profiles as anomalies.
    scores = model.decision_function(features)
    return {(p['pid'], p['created_at']) for p, score in zip(usable, scores) if score < -1e-6}
