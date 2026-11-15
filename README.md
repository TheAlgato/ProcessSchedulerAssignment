# ProcessScope - Real-Time Process Monitoring Dashboard

CSE316 Operating Systems, CA3, Project 13.

Monitor live process states, CPU usage, and memory consumption. Inspect individual processes, identify resource pressure, and explicitly suspend, resume, or terminate a process owned by your account. Anomaly detection and forecasts remain additional analysis tools.

## Easy setup and start

First install Python 3.10 or newer from [python.org](https://www.python.org/downloads/). On Windows, enable Python on PATH during installation. Download or clone this project onto each computer; don't copy the `os` virtual environment between computers.

1. On **Windows**, double-click `Start Windows.bat`. On **macOS**, double-click `Start macOS.command`. On Linux, run `python3 setup.py` in the project folder. If macOS blocks a downloaded launcher, open Terminal in the folder and run `python3 setup.py`.
2. Answer the prompts one by one. The launcher asks before creating an `os` environment, installing missing packages from the internet, and starting the dashboard. When the packages already exist, installation is skipped.
3. In your browser, start from the welcome page and follow setup. Choose whether to allow monitoring, then whether to save history locally or keep it only for the current session. The app does not collect process data before you allow it. The dashboard starts in black; enable **Light appearance** in the sidebar if preferred.
4. Leave the dashboard open to collect samples. Use Overview, Processes, Analysis, and Diagnostics to navigate. Search, filtering and sorting are above the process table. The sidebar contains appearance, refresh interval, history window, and **Pause collection**. Its arrow collapses or reopens the controls. Refresh defaults to 2 seconds and can be set to 1, 5, 10, 30, or 60 seconds. Use **Stop monitoring and restart guide** to stop that session, or close the tab and press Ctrl+C in the launcher window to stop the server.

Resource history separates CPU, memory and disk capacity into aligned charts. Enable **Focus on changes** to see smaller variations, or drag to zoom. Collection settings take effect after **Apply settings**. Analysis includes a flagged-process watchlist, recommendations and forecast readiness; independent validation details appear when enough history exists.

If you have an `os` folder copied from another operating system, rename or remove that folder and run the launcher to create a fresh environment. The launcher does not install Python itself. If setup cannot download packages, check your internet connection and run it again.

For a manual setup, run `python3 -m venv os`, then `os/bin/python -m pip install -r requirements.txt` and `os/bin/python -m streamlit run dashboard.py`. On Windows, use `py -m venv os` and `os\Scripts\python.exe` in place of `os/bin/python`. To collect without the dashboard, run `python app.py --interval 5`; the terminal collector saves history directly and does not show the dashboard's consent guide.

## How it works

1. **Monitoring:** psutil reads CPU, memory, process state, thread count and available cumulative process disk I/O. System disk utilization is filesystem capacity used, not I/O throughput. Process CPU can exceed 100% when multiple cores are used; new processes lack a previous CPU baseline. OS permissions can limit visibility or make I/O unavailable.
2. **Storage:** if you choose local history, each system observation and its visible processes are saved together in `data/performance_history.db`. The database grows over time. If you choose session-only history, system observations remain in memory and disappear when the session ends; existing database files are not erased. Timestamps are UTC. One dashboard session is recommended to avoid duplicate sampling.
3. **Analysis:** Isolation Forest finds unusual CPU and memory profiles relative to other processes in the current snapshot. It uses an automatic threshold rather than requiring a fixed percentage of outliers. An anomaly is not proof of a fault. At least 20 usable processes are needed.
4. **Forecast:** a Random Forest regressor learns from observations approximately five minutes apart. At least 20 pairs are needed. A chronological evaluation, with training targets kept before test features, compares it against a persistence baseline (the current value). The forest is selected per resource only where measured error is lower; otherwise the baseline is used. With too little separated history for evaluation, the baseline is explicitly labelled as unvalidated. Offline gaps are excluded. Re-evaluation happens at most once per minute, using at most 2,000 recent records. The dashboard shows the forecast timestamp and validation errors. Estimates are not guarantees.
5. **Recommendations:** CPU at 90%, memory at 85%, filesystem capacity at 90%, and swap at 85% trigger investigation advice. CPU and memory pressure, plus zombie processes, appear as warnings across views. Users decide whether to act.
6. **Management:** controls start disabled. Enable them in the sidebar, select a process in Processes, select Suspend, Resume, or Terminate, and click Review action. The confirmation fixes the process identity and action; type the displayed PID and confirm. The backend rechecks PID and creation time, blocks PID 0/1, the dashboard and its ancestors, and other accounts’ processes. It uses the account’s OS permissions without elevation. A successful request does not guarantee termination. On Windows, Terminate forcibly ends the target. The last 50 action outcomes are available for CSV download in the session.

The dashboard is intended for local use; do not expose it to untrusted networks. It does not provide process-level network statistics because those are not reliably available across platforms.

## Diagnostics and process inspection

The **Diagnostics** view shows system network upload/download rates, disk read/write rates, CPU usage by logical core, available memory, swap usage and the measured collection/analysis time. Rates use counter changes divided by actual elapsed time. Missing counters, counter resets and first readings are shown as unavailable. System CPU uses instance-owned cumulative counters so dashboard thread changes do not reset its baseline.

The **Processes** view includes per-process disk transfer rates and an inspector for CPU and resident-memory trends. Each visible process keeps up to 120 session readings, keyed by PID and creation time; exited process histories are removed. The diagnostic JSON download captures the current system/process snapshot and forecast details. Session-only mode keeps this in memory until the session ends; downloading a report saves a copy at your request.

SQLite schema additions preserve existing rows. Additional diagnostic values are stored as JSON alongside the original columns. WAL mode allows readers to coexist with a writer, and connections close after each operation. The dashboard loads history once at initialization and appends new samples in memory rather than rereading all rows on each refresh.

## Test and understand the stages

Run `python -m unittest discover -s tests -v`. The explanations in [docs/01-monitoring.md](docs/01-monitoring.md), [docs/02-analysis.md](docs/02-analysis.md), and [docs/03-dashboard.md](docs/03-dashboard.md) describe each stage and its limitations. `modules/` contains collection and analysis, `database/` handles persistence, and `dashboard.py` presents the results.

Windows compatibility is based on the cross-platform psutil and Python APIs; process access and disk counters depend on the account and OS. Use an account with appropriate permissions if processes are missing. Windows has not yet been verified on a Windows machine.


## Project 13 alignment and submission

The required dashboard, real process readings, process controls, and issue identification map to project 13. AI analysis is additional scope. See [the alignment review](docs/project13-alignment.md) for before-and-after findings and remaining submission tasks.

The three suggested team modules are collection and process control, analysis and storage, and dashboard and reporting. Assign one member to each module and record actual names in [the report body](docs/report-body.md).

Generate the complete report, including the current source-code appendix, with `python tools/build_project_report.py`. Open `PROJECT_REPORT.md` and fill in team details, the actual GitHub repository link, and real revision evidence before exporting it for UMS. The report follows the eight required sections and appendices A, B, and C. Rebuild it after any code change.

The ZIP does not carry Git history. Maintain at least seven genuine, clearly described revisions on GitHub, use feature branches, and merge after tests pass. Do not count the historical numbered documentation files as commits. Each student submits the integrated report individually on UMS and prepares for the presentation and viva.

The guidelines permit an AI-generated explanation in appendix A and also require students to write and understand their own implementation. Review this assisted revision with your team and instructor before submission.
