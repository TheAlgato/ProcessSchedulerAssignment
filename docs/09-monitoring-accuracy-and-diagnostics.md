# 09 — Monitoring accuracy, efficiency and diagnostics

## Corrections

- System CPU now uses cumulative CPU counters owned by each monitor instance. This avoids the per-thread baseline behavior of nonblocking `psutil.cpu_percent` when Streamlit changes threads. Counter accounting excludes guest double-counting and idle/I/O-wait time; unavailable or zero intervals are not reported as measured zero usage.
- Process CPU intervals now use each process's observation time. PID plus creation time protects CPU and I/O deltas from PID reuse.
- Isolation Forest uses an automatic threshold instead of forcing 5% of profiles to be outliers. Constant profiles and floating-point threshold noise are handled explicitly.
- Forecast validation separates training targets from the first held-out feature time to avoid temporal leakage. A forest must beat persistence on each resource's held-out error before it is used. Evaluation errors are shown, and unvalidated baseline estimates are labelled honestly.

## Efficiency

Forecast work is bounded to 2,000 recent readings and evaluated at most once per minute. Long offline gaps start a new recording segment for prediction. The dashboard appends to its in-memory history instead of reading up to 20,000 SQLite rows on every refresh. Process trend storage is bounded to 120 readings per visible process, with exited identities removed. SQLite enables WAL and serialized schema migration; existing data is preserved.

## Added functionality

- Network upload/download rates and disk read/write rates, measured from actual elapsed counter changes.
- Per-logical-core CPU, available memory and swap information.
- Process-level read/write rates and an inspector showing CPU and resident-memory trends.
- Diagnostics view with collection/analysis duration and downloadable JSON snapshot.
- Forecast method, evaluation timestamp and held-out error display.
- Disk-capacity and swap-pressure recommendations.

## Verification and limits

20 automated tests passed across the suite and the added database migration check. They cover CPU accounting, first readings and counter resets, PID reuse, bounded process histories, prediction reuse, identical anomaly profiles, forecast baseline selection, persistence, preservation of original database rows during migration, and the existing setup/chart behaviors. A live macOS dashboard check exercised Diagnostics, process inspection and Analysis. One observed cycle collected and analyzed 403 visible processes in approximately 68 ms; this is an observation on this machine, not a performance guarantee.

Anomaly detection remains a cross-process comparison. Forecast validation uses a limited chronological holdout, not a promise of future accuracy. Multiple browser sessions still collect independently; a single session is recommended. CPU observations have sampling and OS scheduling limits. Windows and Linux require live platform verification, and permissions can restrict available counters. Process-level network statistics are not implemented.

## API references consulted

- [psutil API documentation](https://psutil.readthedocs.io/stable/)
- [Scikit-learn IsolationForest documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
