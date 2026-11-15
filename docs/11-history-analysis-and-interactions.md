# 11 — Expanded history, analysis and smoother interactions

Resource history now uses three aligned charts with separate vertical axes for CPU, memory and disk capacity. Each raw reading is retained. Focus on changes tightens each axis around the observed values; the axis labels remain percentages. Plot zoom is preserved across readings with stable chart keys and Plotly UI revision settings.

The memory ring is larger and reports installed and available memory below it. The CPU ranking shortens long process labels, retains full names and PID on hover, shows numeric usage on bars, and leaves room for labels and values.

Analysis now includes threshold-based resource pressure, the actual flagged process watchlist, recommended checks, forecast readiness based on eligible five-minute pairs, and a current-versus-forecast table. Validation errors and method selection are explained in an expandable section. An outlier is still a cross-process statistical finding, not a diagnosis.

Navigation, chart settings and process controls now run inside the live fragment, preserving the outer page and sidebar during those interactions. Collection settings are grouped behind Apply settings. Downloads use `on_click="ignore"` so clicking them does not rerun the app. Sidebar theme changes, applying collection settings, pausing, stopping and setup navigation still require normal Streamlit reruns. This reduces redraws within the current Streamlit architecture; it does not convert the application into a separate JavaScript SPA.

The minimum Streamlit version is now 1.44 to support frontend-only downloads. The launcher checks for that version and offers to update packages if necessary.

Verification: 23 automated tests passed, including data-preserving split charts, long-label identity preservation and forecast-readiness counts. A live macOS application check exercised history focus, pause, Analysis readiness and navigation. The updated layouts were also reviewed in a browser.

Reference: [Streamlit 1.44 download button behavior](https://docs.streamlit.io/1.44.0/develop/api-reference/widgets/st.download_button).
