# 02 — Analyze and forecast

Isolation Forest compares CPU and memory profiles across the current snapshot. An outlier is a statistical observation, not a diagnosis or a comparison against the process's own history. At least 20 processes with usable CPU and memory data are required.

The predictor trains a random forest on historical observations paired with readings approximately five minutes later. It requires at least 20 valid pairs and rejects pairs with a gap larger than the horizon plus 30 seconds. Predictions are estimates, not guarantees; current CPU and memory alone cannot capture all causes of future load. No predictions are fabricated while data is insufficient.

Recommendations combine high-usage thresholds and model results. They suggest investigation and never stop or modify a process.
