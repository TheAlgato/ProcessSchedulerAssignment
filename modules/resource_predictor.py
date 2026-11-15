"""Bounded, chronological forecasting with a measured persistence baseline."""

import time

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def _training_pairs(history, horizon_seconds):
    if len(history) < 2:
        return None
    df = pd.DataFrame(history[-2000:]).copy()
    df['recorded_at'] = pd.to_datetime(df['recorded_at'], utc=True, errors='coerce')
    for field in ('cpu_percent', 'memory_percent'):
        df[field] = pd.to_numeric(df[field], errors='coerce')
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=['recorded_at', 'cpu_percent', 'memory_percent'])
    df = df.sort_values('recorded_at').drop_duplicates('recorded_at', keep='last')
    df = df[df['cpu_percent'].between(0, 100) & df['memory_percent'].between(0, 100)]
    if len(df) < 2:
        return None
    times = np.array([value.timestamp() for value in df['recorded_at']], dtype=float)
    # Keep only the latest continuous recording segment. Offline gaps must not
    # become training examples for a nominal five-minute forecast.
    cadence = float(np.median(np.diff(times)))
    gaps = np.flatnonzero(np.diff(times) > max(90, cadence * 3))
    if len(gaps):
        df = df.iloc[gaps[-1] + 1:]
        times = times[gaps[-1] + 1:]
    targets = np.searchsorted(times, times + horizon_seconds)
    indices = np.flatnonzero(targets < len(times))
    indices = indices[(times[targets[indices]] - times[indices]) <= horizon_seconds + 30]
    return df, times, indices, targets


def forecast_readiness(history):
    prepared = _training_pairs(history, 300)
    return {'valid_pairs': len(prepared[2]) if prepared is not None else 0}


def predict_resources(history, horizon_seconds=300, min_pairs=20):
    prepared = _training_pairs(history, horizon_seconds)
    if prepared is None:
        return None
    df, times, indices, targets = prepared
    values = df[['cpu_percent', 'memory_percent']].to_numpy(dtype=float)
    if len(indices) < min_pairs:
        return None
    # Purge training pairs whose target occurs at/after the first test feature.
    # Merely splitting adjacent pairs would leak future measurements into training.
    test_size = max(5, len(indices) // 5)
    test = indices[-test_size:]
    train = indices[times[targets[indices]] < times[test[0]]]
    predicted = values[-1].copy()
    methods = ['Persistence baseline', 'Persistence baseline']
    model_mae = baseline_mae = None
    if len(train) >= min_pairs:
        model = RandomForestRegressor(n_estimators=60, min_samples_leaf=3, random_state=42, n_jobs=1)
        model.fit(values[train], values[targets[train]])
        model_mae = np.abs(model.predict(values[test]) - values[targets[test]]).mean(axis=0)
        baseline_mae = np.abs(values[test] - values[targets[test]]).mean(axis=0)
        use_model = model_mae < baseline_mae
        if use_model.any():
            model.fit(values[indices], values[targets[indices]])
            candidate = model.predict(values[-1:])[0]
            predicted[use_model] = candidate[use_model]
            methods = ['Random Forest' if use else 'Persistence baseline' for use in use_model]
    predicted = np.clip(predicted, 0, 100)
    return {'cpu_percent': float(predicted[0]), 'memory_percent': float(predicted[1]),
            'training_pairs': len(indices), 'horizon_seconds': horizon_seconds,
            'methods': methods, 'validation_pairs': len(test) if model_mae is not None else 0,
            'model_mae': model_mae.tolist() if model_mae is not None else None,
            'baseline_mae': baseline_mae.tolist() if baseline_mae is not None else None,
            'based_on': df.iloc[-1]['recorded_at'].isoformat()}


class ResourcePredictor:
    """Re-evaluate at most once a minute rather than on every UI sample."""
    def __init__(self):
        self._checked_at = None
        self._result = None

    def predict(self, history):
        now = time.monotonic()
        if self._checked_at is None or now - self._checked_at >= 60:
            self._result = predict_resources(history)
            self._checked_at = now
        return self._result
