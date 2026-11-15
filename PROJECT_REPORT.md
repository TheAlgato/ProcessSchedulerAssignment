# Real-Time Process Monitoring Dashboard

CSE316 Operating Systems, CA3, Project 13  
Application: ProcessScope  
Institution: Lovely Professional University

Team members and registration numbers: [Enter actual details, maximum three students]  
Section and faculty: [Enter actual details]  
GitHub repository name and URL: [Enter the team's actual repository]  
Submission date: [Enter actual submission date]

## 1. Project overview

ProcessScope displays real-time operating-system process states, CPU utilization, and memory consumption in a graphical dashboard. Administrators can inspect processes and explicitly suspend, resume, or terminate processes owned by the account running the application. Warnings and recommendations help users investigate resource pressure and zombie processes.

The dashboard runs locally. Its monitoring module reads actual OS counters through psutil. It refreshes every two seconds by default, with selectable intervals from one to sixty seconds. A timestamp and paused indicator show the age of each displayed observation. This is periodic real-time monitoring, not a hard real-time system with guaranteed deadlines.

The required scope is monitoring, process management, and issue identification. Existing anomaly detection, resource forecasts, network diagnostics, disk metrics, and exports remain additional functionality. The app does not replace an operating-system administrator or automatically terminate workloads.

## 2. Module-wise breakdown

Assign one team member to each module and replace the entries below with actual responsibilities.

| Module | Responsibility and code | Assigned member |
| --- | --- | --- |
| Collection and process management | `modules/process_monitor.py`, `modules/system_monitor.py`, and `modules/process_control.py`. Read process and system counters, derive interval CPU and transfer rates, and apply confirmed OS process actions. | [Member 1] |
| Analysis and storage | `modules/anomaly_detector.py`, `modules/resource_predictor.py`, `modules/recommendation_engine.py`, `modules/process_history.py`, and `database/db_manager.py`. Maintain history, detect resource pressure and unusual profiles, and produce optional forecasts. | [Member 2] |
| Dashboard, visualization, and reporting | `dashboard.py`, `visualization/`, launchers, `tools/build_project_report.py`, and documentation. Present readings and controls, export results, and integrate and document the application. | [Member 3] |

The modules form one integrated application. Tests cover their observable behavior and their dashboard integration.

## 3. Functionalities

### Live monitoring

The process table includes PID, name, actual OS state, CPU percentage, memory percentage, resident memory in MiB, threads, age, and available disk I/O. CPU is computed from changes in cumulative user and system time divided by elapsed monotonic time. A process using multiple cores can exceed 100%. Newly observed processes need a second sample for CPU usage.

System readings include CPU utilization, memory usage and capacity, filesystem capacity, per-core CPU, swap, and supported network and disk transfer rates. Process identity consists of PID and creation time so that a reused PID does not inherit the previous process's trend.

Users can search by name or PID, filter high usage or unusual profiles, sort the table, inspect up to 120 recent process readings, and export CSV or JSON snapshots. Collection can be paused. History can remain in memory or be stored in SQLite.

### Process management

Controls start disabled. To act, enable controls, select a process, choose Suspend, Resume, or Terminate, and review the action. The confirmation retains the selected identity and action independently of subsequent live-table or selection changes. The user must type the displayed PID before sending the request. Cancel or a mismatched PID sends no request.

The control module rechecks PID and creation time, running state, ownership, and protected processes. It blocks PID 0/1, the dashboard and its ancestors, other accounts' processes, and exited or zombie targets. The operating system can still deny access, and the app reports the failure without attempting elevation. Suspending stops execution until resumed. On POSIX, Terminate sends a termination request. On Windows it forces the process to end. A sent request does not prove that the process exited, so users check the next reading.

The most recent 50 action outcomes stay in the browser session and can be downloaded as CSV. This session log is not a permanent or tamper-proof audit record.

### Issue identification and additional analysis

CPU usage at or above 90% and memory usage at or above 85% produce visible warnings on all workspace views. Visible zombie processes also produce a warning. Recommendations name the largest visible CPU or memory consumer when system pressure is high. Disk capacity at 90% and swap at 85% produce investigation advice in Overview and Analysis.

Isolation Forest detects unusual CPU and memory profiles relative to other processes in the same snapshot. It requires at least 20 usable processes. An unusual profile alone does not establish a fault.

The optional five-minute forecast uses historical pairs and compares a Random Forest model with a persistence baseline. Independent validation requires enough time-separated history. With insufficient evaluation history, the forecast identifies its baseline as unvalidated. Forecasts do not trigger process actions.

## 4. Technology used

Programming language: Python 3.10 or newer. The revised package was tested with Python 3.12.

Libraries and tools:

- psutil for operating-system counters and process-control APIs.
- Streamlit for the graphical dashboard, forms, session state, and periodic refresh.
- pandas and NumPy for tabular data and numerical operations.
- Plotly for resource charts.
- scikit-learn for optional anomaly detection and forecasting.
- SQLite through Python's standard library for local history.
- unittest, unittest.mock, and Streamlit AppTest for automated verification.
- Git and GitHub for revision tracking, to be maintained by the team.

`requirements.txt` defines installation requirements. `requirements-tested.txt` records the exact package versions used in this verification environment. Windows and Linux behavior still needs verification on those operating systems.

## 5. Flow diagram

```text
Start local dashboard
        |
Allow monitoring -> Choose history storage -> Open dashboard
        |
Read process and system counters from the operating system
        |
Compute interval CPU and I/O rates
        |
Save chosen history -> Evaluate pressure and optional analysis
        |
Display states, CPU, memory, warnings, charts, and timestamp
        |
        +---- Refresh interval elapsed? ---- Yes ---- Read next sample
        |
        +---- Process management enabled?
                         |
                    Select process
                         |
                    Review fixed target and action
                         |
                    Type matching PID and confirm
                         |
                    Recheck identity, ownership, and protections
                         |
                +--------+---------+
                |                  |
             Allowed          Blocked or exited
                |                  |
        Send OS action       Show failure reason
                |                  |
                +------ Log outcome ------+
                         |
                    Read next sample
```

Cancel and a mismatched confirmation never send a process-control request. OS permission errors are reported as failed outcomes.

## 6. Revision tracking on GitHub

Repository name: [Enter actual repository name]  
GitHub link: [Enter actual repository URL]

The supplied ZIP does not contain `.git` history. No commit count, repository ownership, or branch-merge history can be verified from that archive. The numbered files under `docs/` describe development stages and are not evidence of Git commits.

The guidelines require at least seven genuine revisions with clear commit messages, feature branches, testing, and merges into the main branch. Record actual work below. Do not invent commit hashes or rewrite dates to imply past development.

| Revision | Actual commit hash | Change and validation | Feature branch or merge |
| --- | --- | --- | --- |
| 1 | [Actual hash] | [Actual change and check] | [Actual branch] |
| 2 | [Actual hash] | [Actual change and check] | [Actual branch] |
| 3 | [Actual hash] | [Actual change and check] | [Actual branch] |
| 4 | [Actual hash] | [Actual change and check] | [Actual branch] |
| 5 | [Actual hash] | [Actual change and check] | [Actual branch] |
| 6 | [Actual hash] | [Actual change and check] | [Actual branch] |
| 7 | [Actual hash] | [Actual change and check] | [Actual branch] |

Run `python -m unittest discover -s tests -v` before merging a feature. Use `git log --oneline --all --graph` and actual GitHub commit and pull-request links as revision evidence. Each student uploads the complete integrated report individually on UMS and takes part in the presentation and viva.

## 7. Conclusion and future scope

The revised application implements project 13's required dashboard, live process and resource monitoring, explicit process management, and prompt issue identification. The primary alignment change is the addition of process controls to a previously read-only analyzer, together with project-specific naming and documentation.

The requirement-by-requirement review and black box acceptance matrix are recorded in `docs/black-box-testing.md` and included as supplemental Appendix D. On 15 November 2026, all 15 new interface acceptance tests passed. The full suite passed 50 of 51 tests, with the real-process lifecycle test skipped under sandbox restrictions. A separate local process-control run outside the sandbox passed all 7 tests, including the real disposable-process lifecycle; its evidence is in `docs/verification/2026-11-15-process-control-local.log`. Controlled-input dashboard tests do not prove live OS measurement accuracy or automatic browser refresh; the remaining live-machine acceptance cases in Appendix D must be completed on the presentation machine. The older `docs/project13-alignment.md` preserves the 13 November review.

Future work can include configurable alert thresholds, history retention limits, durable authenticated action auditing, and platform-specific validation. Remote administration would require a separate authentication and deployment design. The current localhost binding is part of the application's local-use scope.

Before submission, fill in the real team and repository details, add revision evidence, review the implementation with the team, capture actual local screenshots, and export the completed report to the format accepted by the instructor.

## 8. References

1. Lovely Professional University. CSE316 Operating Systems, Academic Task 3 project guidelines, supplied PDF `A1358141926_31_2026_CSE316 CA3 Project.pdf`. Submission and report requirements appear on pages 1-3. Project 13 appears on page 6.
2. psutil API reference. https://psutil.io/api/ . Process identity, counters, suspend, resume, terminate, and permissions.
3. Streamlit execution flow. https://docs.streamlit.io/develop/api-reference/execution-flow/st.fragment . Periodic dashboard fragments.
4. Streamlit application testing. https://docs.streamlit.io/develop/api-reference/app-testing . AppTest.
5. Python documentation, sqlite3. https://docs.python.org/3/library/sqlite3.html . Local database persistence.
6. scikit-learn documentation. https://scikit-learn.org/stable/ . Isolation Forest and Random Forest estimators.
7. Plotly Python documentation. https://plotly.com/python/ . Interactive resource charts.

## Appendix A. AI-generated project elaboration and breakdown

This appendix provides the AI-assisted project explanation requested by the guidelines. The team must review it against the implemented behavior and understand the implementation for the viva. The guidelines also require student-written implementation and prohibit copying AI-generated code. Confirm the acceptable use of this assisted revision with the instructor.

### Project goals, expected outcomes, and scope

Build a local graphical process monitor that answers three questions: what is running, which processes consume resources, and which process needs attention or a deliberate management action? The expected result is an integrated dashboard that updates real process states, CPU, and memory, handles unavailable readings, and confirms user-selected process actions. The required outcome does not depend on an AI forecast.

### Module functionalities and examples

The collection and management module measures actual process and system counters. For example, a worker consuming one full CPU core approaches 100% process CPU. If the user pauses that worker through Suspend, a subsequent observation can show a stopped state. Resume allows execution to continue. The identity check prevents a different process from receiving the action after PID reuse.

The analysis and storage module preserves chosen history, identifies pressure, and explains investigation steps. For example, system memory at 87% exceeds the 85% threshold and prompts a review of the largest visible memory consumer. Optional statistical analysis supplements these direct checks.

The dashboard module turns those results into searchable tables, charts, warnings, process inspection, and confirmed controls. For example, reviewing Suspend for PID 300 and later selecting PID 301 does not change the target of the pending confirmation. Exports support documentation and debugging.

### Technology recommendations

Use the existing Python, psutil, Streamlit, and SQLite implementation for the required local monitoring workflow. Retain pandas and Plotly for presentation. Treat scikit-learn analysis as additional functionality, because the assigned problem requires process monitoring and management rather than machine-learning predictions.

### Execution plan

1. Assign actual team members to the three integrated modules and create the GitHub repository.
2. Verify process states, CPU baselines, memory values, and permission behavior on the intended machine.
3. Integrate collection with history and display the timestamp and refresh state.
4. Test process controls on a temporary worker, including cancellation, exited targets, and permission errors.
5. Review visible resource warnings and the corresponding recommendations.
6. Run the automated checks, merge tested feature branches, and retain at least seven real revisions.
7. Rebuild this report from current code, fill in actual evidence, and prepare a demonstration and viva explanation.

## Appendix B. Problem statement

Project 13: Real-Time Process Monitoring Dashboard

"Create a graphical dashboard that displays real-time information about process states, CPU usage, and memory consumption. The tool should allow administrators to manage processes efficiently and identify potential issues promptly."

## Appendix C. Complete project source

Rebuild this appendix after code changes with `python tools/build_project_report.py`.

### .gitignore

````text
.venv/
venv/
os/
__pycache__/
*.py[cod]
data/*.db
data/*.db-*
.pytest_cache/
````

### .streamlit/config.toml

````toml
[server]
address = "localhost"

[theme]
base = "dark"
primaryColor = "#85c7b8"
backgroundColor = "#000000"
secondaryBackgroundColor = "#0b0b0b"
textColor = "#ededed"
font = "sans serif"
````

### Start Windows.bat

````bat
@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 setup.py
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo Python 3.10 or newer is required. Install Python from https://www.python.org/downloads/ and enable it on PATH.
  ) else (
    python setup.py
  )
)
pause
````

### Start macOS.command

````sh
#!/bin/bash
cd "$(dirname "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3.10 or newer is required. Install Python from https://www.python.org/downloads/ and try again."
  read -r -p "Press Enter to close."
  exit 1
fi
python3 setup.py
read -r -p "Press Enter to close."
````

### app.py

````python
"""Run the first-stage collector from a terminal."""

import argparse
import json
import os
import math
import time
from datetime import datetime, timezone
from pathlib import Path

from database.db_manager import DatabaseManager
from modules.process_monitor import ProcessMonitor
from modules.system_monitor import SystemMonitor


def main():
    parser = argparse.ArgumentParser(description="Collect local OS performance samples")
    parser.add_argument('--interval', type=float, default=5, help='Seconds between samples (default: 5)')
    parser.add_argument('--samples', type=int, default=None, help='Stop after this many samples')
    parser.add_argument('--db', default='data/performance_history.db', help='SQLite database path')
    parser.add_argument('--disk-path', default=Path.cwd().anchor or os.path.abspath(os.sep),
                        help='Filesystem path whose disk capacity is monitored')
    args = parser.parse_args()
    if not math.isfinite(args.interval) or args.interval <= 0 or (args.samples is not None and args.samples < 1):
        parser.error('interval must be positive and samples must be at least 1')
    db = DatabaseManager(args.db)
    processes = ProcessMonitor()
    system = SystemMonitor(args.disk_path)
    # Establish baselines so the first persisted CPU sample has a real interval.
    processes.sample()
    count = 0
    try:
        while args.samples is None or count < args.samples:
            time.sleep(args.interval)
            timestamp = datetime.now(timezone.utc).isoformat()
            snapshot = processes.sample()
            metrics = system.sample()
            db.save_sample(timestamp, metrics, snapshot)
            print(json.dumps({'recorded_at': timestamp, **metrics, 'process_count': len(snapshot)}), flush=True)
            count += 1
    except KeyboardInterrupt:
        print('\nMonitoring stopped.')


if __name__ == '__main__':
    main()
````

### dashboard.py

````python
"""Local Streamlit dashboard. Run with: python -m streamlit run dashboard.py."""

import os
import platform
import sqlite3
import time
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st

from database.db_manager import DatabaseManager
from modules.anomaly_detector import detect_anomalies
from modules.process_monitor import ProcessMonitor
from modules.process_control import ProcessControlError, control_process
from modules.recommendation_engine import recommendations
from modules.resource_predictor import ResourcePredictor, forecast_readiness
from modules.process_history import ProcessHistory
from modules.system_monitor import SystemMonitor
from visualization.charts import forecast_chart, history_chart, memory_chart, top_process_chart

PROJECT_DIR = Path(__file__).resolve().parent
st.set_page_config(page_title='ProcessScope · Real-Time Process Monitoring Dashboard', page_icon='◉', layout='wide', initial_sidebar_state='expanded')
if 'setup_step' not in st.session_state:
    st.session_state.setup_step = 'welcome'
ready = st.session_state.setup_step == 'ready'
if ready:
    with st.sidebar:
        st.markdown('<div class="brand"><div class="brand-symbol">≋</div><div><div class="brand-name">ProcessScope</div><div class="brand-subtitle">Local performance monitor</div></div></div>', unsafe_allow_html=True)
        light_mode = st.toggle('Light appearance', value=False)
else:
    light_mode = False
dark_mode = not light_mode
st.markdown('<style>' + (PROJECT_DIR / 'visualization' / 'dashboard.css').read_text() + '</style>', unsafe_allow_html=True)
if light_mode:
    st.markdown('<style>:root { --bg:#f7f8fa; --surface:#fff; --text:#17242b; --muted:#647580; --line:#e1e7eb; --side:#eef2f4; --accent:#087f78; color-scheme:light; }</style>', unsafe_allow_html=True)

if not ready:
    st.session_state.pop('manage_enabled', None)
    st.markdown('<style>[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"] { display:none; }</style>', unsafe_allow_html=True)
    step = st.session_state.setup_step
    st.markdown('<div class="welcome-top"><span class="welcome-logo">≋</span><span>ProcessScope</span><span class="welcome-local">LOCAL WORKSPACE</span></div>', unsafe_allow_html=True)
    _, center, _ = st.columns([1, 3, 1])
    with center:
        if step == 'welcome':
            st.markdown('''<div class="welcome-intro"><div class="welcome-kicker">SYSTEM PERFORMANCE</div>
            <h1>See what your<br>computer is doing.</h1>
            <p>CPU, memory, processes, and disk activity.<br>One workspace, running on your machine.</p></div>''', unsafe_allow_html=True)
            if st.button('Set up monitoring →', type='primary', use_container_width=True):
                st.session_state.setup_step = 'monitor'
                st.rerun()
            st.markdown('<div class="welcome-footnote">Choose what to collect before anything starts.</div>', unsafe_allow_html=True)
            st.markdown('''<div class="welcome-features">
            <div><span>01</span><section><strong>Live activity</strong><p>System readings and a searchable process monitor.</p></section></div>
            <div><span>02</span><section><strong>A closer look</strong><p>Process history, transfer rates, and per-core CPU usage.</p></section></div>
            <div><span>03</span><section><strong>Performance analysis</strong><p>Unusual resource profiles and estimates from recorded history.</p></section></div>
            </div>''', unsafe_allow_html=True)
        elif step == 'monitor':
            st.markdown('<div class="setup-label">SETUP / 1 OF 3</div>', unsafe_allow_html=True)
            st.header('Allow local monitoring')
            st.write('ProcessScope reads CPU, memory, disk and network activity, along with available process names and resource usage.')
            st.caption('Monitoring reads activity. Optional process controls require a separate confirmation for each action and use your account’s permissions.')
            if st.button('Allow monitoring', type='primary', use_container_width=True):
                st.session_state.setup_step = 'history'
                st.rerun()
            if st.button('Back'):
                st.session_state.setup_step = 'welcome'
                st.rerun()
        elif step == 'history':
            st.markdown('<div class="setup-label">SETUP / 2 OF 3</div>', unsafe_allow_html=True)
            st.header('Choose your history')
            st.write('Save system and process readings locally to keep a record between sessions, or keep system history in memory for this session.')
            st.caption('Saved readings go to the project’s data folder. Session-only mode leaves existing saved history untouched.')
            if st.button('Save history locally', type='primary', use_container_width=True):
                st.session_state.save_history = True
                st.session_state.setup_step = 'tutorial'
                st.rerun()
            if st.button('Use session only', use_container_width=True):
                st.session_state.save_history = False
                st.session_state.setup_step = 'tutorial'
                st.rerun()
            if st.button('Back'):
                st.session_state.setup_step = 'monitor'
                st.rerun()
        else:
            st.markdown('<div class="setup-label">SETUP / 3 OF 3</div>', unsafe_allow_html=True)
            st.header('Ready to start')
            st.write('Overview shows resource use. Processes lets you inspect programs and manage them after enabling process controls. Analysis explains unusual profiles and forecasts. Diagnostics covers transfers, cores, and swap.')
            st.caption('Use the sidebar to pause collection or change the refresh interval. Forecasts appear once enough history is available.')
            if st.button('Open dashboard', type='primary', use_container_width=True):
                st.session_state.setup_step = 'ready'
                st.rerun()
            if st.button('Back'):
                st.session_state.setup_step = 'history'
                st.rerun()
    st.markdown('<div class="welcome-bottom">Windows · macOS · Linux<span>Readings depend on system permissions.</span></div>', unsafe_allow_html=True)
    st.stop()

with st.sidebar:
    st.header('Collection')
    with st.form('collection_settings'):
        interval = st.selectbox('Refresh interval', [1, 2, 5, 10, 30, 60], index=1, format_func=lambda x: f'{x} seconds')
        history_minutes = st.selectbox('History window', [15, 30, 60, 180, 1440], index=2,
                                       format_func=lambda x: f'{x} minutes' if x < 60 else ('1 hour' if x == 60 else f'{x // 60} hours'))
        st.form_submit_button('Apply settings')
    paused = st.toggle('Pause collection', value=False)
    manage_enabled = st.toggle('Enable process controls', value=False, key='manage_enabled',
                               help='Suspend, resume, or terminate a process owned by this account. Each action requires confirmation.')
    if not manage_enabled:
        st.session_state.pop('pending_action', None)
    st.divider()
    st.header('This device')
    st.caption(f'{platform.system()} · {platform.machine()}')
    st.caption('Local process monitoring and management. OS permissions apply to every action.')
    st.caption('History: ' + ('saved locally' if st.session_state.save_history else 'this session only'))
    if st.button('Stop monitoring and restart guide'):
        for key in ('collector', 'system_collector', 'db', 'session_history', 'save_history', 'last_snapshot', 'predictor', 'process_history', 'pending_action', 'action_notice', 'action_history'):
            st.session_state.pop(key, None)
        st.session_state.setup_step = 'welcome'
        st.rerun()

if 'collector' not in st.session_state:
    try:
        collector = ProcessMonitor()
        system_collector = SystemMonitor(PROJECT_DIR.anchor or os.path.abspath(os.sep))
        collector.sample()
        db = DatabaseManager(PROJECT_DIR / 'data' / 'performance_history.db') if st.session_state.save_history else None
        st.session_state.collector = collector
        st.session_state.system_collector = system_collector
        st.session_state.db = db
        st.session_state.session_history = db.system_history(limit=20000) if db else []
        st.session_state.predictor = ResourcePredictor()
        st.session_state.process_history = ProcessHistory()
    except (OSError, sqlite3.Error) as error:
        st.error(f'Unable to start monitoring: {error}. Check operating system permissions and restart the dashboard.')
        st.stop()


def process_table(processes, anomalies, search, process_filter, sort_by):
    rows = []
    for p in processes:
        if search.casefold() not in f"{p['name']} {p['pid']}".casefold():
            continue
        unusual = anomalies is not None and (p['pid'], p['created_at']) in anomalies
        if process_filter == 'Unusual only' and not unusual:
            continue
        if process_filter == 'High CPU (≥ 20%)' and (p['cpu_percent'] is None or p['cpu_percent'] < 20):
            continue
        if process_filter == 'High memory (≥ 5%)' and (p['memory_percent'] is None or p['memory_percent'] < 5):
            continue
        state = 'Unavailable' if anomalies is None or p['cpu_percent'] is None else ('Unusual' if unusual else 'Typical')
        rows.append({'PID': p['pid'], 'Name': p['name'], 'Status': p['status'], 'CPU %': p['cpu_percent'],
                     'Memory %': p['memory_percent'], 'RAM (MiB)': p['memory_bytes'] / 1024**2,
                     'Threads': p['threads'], 'Age (s)': p['elapsed_seconds'],
                     'Read bytes': p['read_bytes'], 'Write bytes': p['write_bytes'], 'Anomaly': state})
        rows[-1]['Read MiB/s'] = p.get('read_bytes_per_sec') / 1024**2 if p.get('read_bytes_per_sec') is not None else None
        rows[-1]['Write MiB/s'] = p.get('write_bytes_per_sec') / 1024**2 if p.get('write_bytes_per_sec') is not None else None
    frame = pd.DataFrame(rows)
    if not frame.empty:
        column = {'CPU': 'CPU %', 'Memory': 'Memory %', 'Name': 'Name', 'PID': 'PID'}[sort_by]
        frame = frame.sort_values(column, ascending=sort_by in ('Name', 'PID'), na_position='last')
    return frame


st.markdown('<div class="workspace-title">Real-Time Process Monitoring Dashboard</div><div class="workspace-description">Live process states, CPU and memory usage, and process controls.</div>', unsafe_allow_html=True)


def process_controls(selected_process):
    """Keep the reviewed target fixed while live snapshots and selections change."""
    st.subheader('Manage a process')
    notice = st.session_state.get('action_notice')
    if notice:
        st.info(notice)
    if not manage_enabled:
        st.caption('Enable process controls in the sidebar to suspend, resume, or terminate a selected process.')
        return
    st.caption('Actions affect programs on this computer. Suspending pauses execution; terminating may discard unsaved work. On Windows, Terminate forces the process to end.')
    if selected_process is not None:
        action = st.selectbox('Action', ['suspend', 'resume', 'terminate'], format_func=str.capitalize)
        if st.button('Review action'):
            st.session_state.pending_action = {**selected_process, 'action': action}
            st.session_state.pop('confirm_pid', None)
    pending = st.session_state.get('pending_action')
    if pending:
        st.write(f"Confirm {pending['action']} for {pending['name']} (PID {pending['pid']}).")
        with st.form('confirm_process_action'):
            confirmation = st.text_input('Type the target PID to confirm', key='confirm_pid')
            apply_action = st.form_submit_button('Confirm action', type='primary')
            cancel_action = st.form_submit_button('Cancel')
        if cancel_action:
            st.session_state.pop('pending_action', None)
            st.rerun()
        if apply_action:
            if confirmation.strip() != str(pending['pid']):
                st.error('The PID does not match. No action was sent.')
            else:
                try:
                    message = control_process(pending['pid'], pending['created_at'], pending['action'])
                    outcome = 'Request sent'
                except ProcessControlError as error:
                    message, outcome = str(error), 'Blocked or failed'
                events = st.session_state.setdefault('action_history', [])
                events.append({'recorded_at': datetime.now(timezone.utc).isoformat(),
                               'pid': pending['pid'], 'created_at': pending['created_at'],
                               'name': pending['name'], 'action': pending['action'],
                               'outcome': outcome, 'message': message})
                del events[:-50]
                st.session_state.action_notice = message
                st.session_state.pop('pending_action', None)
                st.session_state.pop('last_snapshot', None)
                st.rerun()
    if st.session_state.get('action_history'):
        with st.expander('Recent process actions'):
            events = pd.DataFrame(st.session_state.action_history)
            st.dataframe(events, hide_index=True, use_container_width=True)
            st.download_button('Download action log as CSV', events.to_csv(index=False).encode('utf-8'),
                               'process_actions.csv', 'text/csv', on_click='ignore')


def usage(value):
    return f'{value:.1f}%' if value is not None else 'Warming up'


def rate(value):
    return f'{value / 1024**2:.2f} MiB/s' if value is not None else 'Unavailable'


@st.fragment(run_every=None if paused else interval)
def live_view():
    page = st.radio('Workspace view', ['Overview', 'Processes', 'Analysis', 'Diagnostics'],
                    horizontal=True, label_visibility='collapsed', key='workspace_view')
    try:
        previous = st.session_state.get('last_snapshot')
        # Widget changes also rerun the page. Reuse the latest sample until its
        # interval expires so filters and theme changes do not collect extra rows.
        if previous is None or (not paused and time.monotonic() - previous['sampled_at'] >= interval):
            started = time.monotonic()
            processes = st.session_state.collector.sample()
            system = st.session_state.system_collector.sample()
            stamp = datetime.now(timezone.utc).isoformat()
            if st.session_state.db is not None:
                st.session_state.db.save_sample(stamp, system, processes)
            history = st.session_state.session_history
            history.append({'recorded_at': stamp, 'cpu_percent': system['cpu_percent'],
                            'memory_percent': system['memory_percent'], 'disk_percent': system['disk_percent'],
                            'process_count': len(processes)})
            del history[:-20000]
            st.session_state.process_history.update(stamp, processes)
            previous = {'sampled_at': started, 'processes': processes, 'system': system,
                        'stamp': stamp, 'history': history, 'anomalies': detect_anomalies(processes),
                        'prediction': st.session_state.predictor.predict(history)}
            previous['collection_ms'] = (time.monotonic() - started) * 1000
            st.session_state.last_snapshot = previous
        processes, system, stamp, history = (previous[k] for k in ('processes', 'system', 'stamp', 'history'))
        anomalies, prediction = previous['anomalies'], previous['prediction']
    except (OSError, sqlite3.Error) as error:
        st.error(f'Unable to collect or save a sample: {error}. Check permissions and restart the dashboard.')
        return
    a, b, c, d = st.columns(4)
    a.metric('CPU', usage(system['cpu_percent']))
    b.metric('RAM', f"{system['memory_percent']:.1f}%", help='Percentage of total system memory in use.')
    c.metric('DISK', f"{system['disk_percent']:.1f}%" if system['disk_percent'] is not None else 'Unavailable',
             help='Used capacity of the drive containing the project, not disk activity.')
    d.metric('PROCESSES', len(processes))
    updated = datetime.fromisoformat(stamp).strftime('%H:%M:%S UTC')
    state = 'Paused' if paused else f'Collecting every {interval}s'
    dot = 'status-dot paused' if paused else 'status-dot'
    st.markdown(f'<div class="status-line"><span class="{dot}"></span>{state} · Last reading {updated}</div>', unsafe_allow_html=True)
    if ((system['cpu_percent'] is not None and system['cpu_percent'] >= 90)
            or system['memory_percent'] >= 85):
        st.warning('High resource usage detected. Open Analysis to review the processes using the most CPU or memory.')
    zombies = sum(p['status'] == 'zombie' for p in processes)
    if zombies:
        st.warning(f'{zombies} zombie process(es) detected. Their parent processes need to collect the exit status.')

    if page == 'Overview':
        st.subheader('Resource history')
        st.markdown('<div class="section-note">CPU, memory, and disk capacity over the selected period.</div>', unsafe_allow_html=True)
        frame = pd.DataFrame(history)
        if not frame.empty:
            frame['recorded_at'] = pd.to_datetime(frame['recorded_at'], utc=True)
            shown = frame[frame['recorded_at'] >= pd.Timestamp.now(tz='UTC') - pd.Timedelta(minutes=history_minutes)]
            focus = st.toggle('Focus on changes', value=False,
                              help='Tighten each vertical axis around the recorded values. Axes remain labelled in percent.')
            st.plotly_chart(history_chart(shown, dark=dark_mode, focus=focus), use_container_width=True,
                            theme=None, key='resource_history_chart', config={'displaylogo': False, 'scrollZoom': False})
            st.caption(f'{len(shown):,} raw readings in this window. Each resource has its own labelled axis. Drag to zoom; double-click to reset.')
            st.download_button('Download displayed history as CSV', shown.to_csv(index=False).encode('utf-8'),
                               'resource_history.csv', 'text/csv', on_click='ignore')
        st.caption('The history window controls the chart and download; forecasts use the available history.')
        left, right = st.columns([1, 2])
        with left:
            st.subheader('Memory allocation')
            st.plotly_chart(memory_chart(system['memory_percent'], dark=dark_mode), use_container_width=True, theme=None, key='memory_ring')
            st.caption(f"{system['memory_total_bytes'] / 1024**3:.1f} GiB total · {system.get('memory_available_bytes', 0) / 1024**3:.1f} GiB available")
        with right:
            st.subheader('Highest CPU usage')
            top_chart = top_process_chart(processes, 'cpu_percent', dark=dark_mode)
            if top_chart is not None:
                st.plotly_chart(top_chart, use_container_width=True, theme=None, key='top_cpu_chart')
            else:
                st.info('Waiting for process CPU measurements.')
            st.caption('Top visible processes. A process can use more than 100% across cores.')
        st.subheader('Observations')
        st.markdown('<div class="section-note">Suggestions based on the latest sample.</div>', unsafe_allow_html=True)
        for item in recommendations(system, processes, anomalies, prediction):
            st.write('• ' + item)

    if page == 'Processes':
        st.subheader('Running processes')
        search_col, filter_col, sort_col = st.columns([2, 2, 1])
        search = search_col.text_input('Search', placeholder='Process name or PID')
        process_filter = filter_col.selectbox('Show', ['All', 'Unusual only', 'High CPU (≥ 20%)', 'High memory (≥ 5%)'])
        sort_by = sort_col.selectbox('Sort by', ['CPU', 'Memory', 'Name', 'PID'])
        table = process_table(processes, anomalies, search, process_filter, sort_by)
        st.caption(f'{len(table)} of {len(processes)} visible processes match the current filters. Click a column heading to sort.')
        if not table.empty:
            st.dataframe(table, hide_index=True, use_container_width=True,
                         column_config={'CPU %': st.column_config.NumberColumn(format='%.1f%%'),
                                        'Memory %': st.column_config.NumberColumn(format='%.1f%%'),
                                        'RAM (MiB)': st.column_config.NumberColumn(format='%.1f')})
            st.download_button('Download filtered processes as CSV', table.to_csv(index=False).encode('utf-8'),
                               'process_snapshot.csv', 'text/csv', on_click='ignore')
        else:
            st.info('No visible processes match these filters.')
        st.caption('CPU can exceed 100% across cores. Disk counters are cumulative bytes; blank means unavailable. OS permissions can hide processes or metrics.')
        selected_process = None
        if processes:
            st.subheader('Inspect a process')
            choices = {(p['pid'], p['created_at']): p for p in processes}
            selected = st.selectbox('Process', sorted(choices), index=None, placeholder='Select a process',
                                    format_func=lambda key: f"{choices[key]['name']} · PID {key[0]}")
            selected_process = choices.get(selected)
            readings = st.session_state.process_history.for_process(*selected) if selected else []
            if len(readings) >= 2:
                trend = pd.DataFrame(readings).set_index('recorded_at')
                col1, col2 = st.columns(2)
                with col1:
                    st.caption('Process CPU (%)')
                    st.line_chart(trend[['cpu_percent']])
                with col2:
                    st.caption('Resident memory (MiB)')
                    st.line_chart(trend[['memory_mib']])
            else:
                st.caption('Collect another sample to see this process’s trend.')
            st.caption('Up to 120 samples from this browser session. PID and creation time identify the process.')
        process_controls(selected_process)

    if page == 'Analysis':
        st.subheader('Current resource pressure')
        st.caption('Thresholds describe the latest sample. A high reading or a statistical outlier alone does not establish a fault.')
        cpu_col, ram_col, anomaly_col = st.columns(3)
        cpu_col.metric('CPU · threshold 90%', 'Unavailable' if system['cpu_percent'] is None else ('High' if system['cpu_percent'] >= 90 else 'Below'))
        ram_col.metric('Memory · threshold 85%', 'High' if system['memory_percent'] >= 85 else 'Below')
        anomaly_col.metric('Unusual profiles', str(len(anomalies)) if anomalies is not None else 'Not ready')
        st.subheader('Processes to review')
        if anomalies is None:
            st.info('Waiting for at least 20 processes with usable CPU and memory readings.')
        elif not anomalies:
            st.success('No unusual profiles detected in the current snapshot.')
        else:
            unusual = process_table(processes, anomalies, '', 'Unusual only', 'CPU')
            st.dataframe(unusual[['Name', 'PID', 'CPU %', 'Memory %', 'RAM (MiB)', 'Status']],
                         hide_index=True, use_container_width=True, key='anomaly_watchlist',
                         column_config={'CPU %': st.column_config.NumberColumn(format='%.1f%%'),
                                        'Memory %': st.column_config.NumberColumn(format='%.1f%%'),
                                        'RAM (MiB)': st.column_config.NumberColumn(format='%.1f')})
        st.caption('Isolation Forest compares resource profiles across visible processes, not against each process’s personal history.')
        st.subheader('Recommended checks')
        for item in recommendations(system, processes, anomalies, prediction):
            st.write('• ' + item)
        st.divider()
        st.subheader('Five-minute outlook')
        if prediction is None:
            readiness = forecast_readiness(history)
            st.progress(min(readiness['valid_pairs'] / 20, 1),
                        text=f"{min(readiness['valid_pairs'], 20)} of 20 minimum five-minute sample pairs available")
            st.write('Keep monitoring to build the forecast history. Each pair needs a reading and another reading approximately five minutes later.')
            st.caption('Long recording gaps are excluded. Forecast evaluation runs at most once per minute. More separated history is needed for an independent model evaluation.')
        else:
            rows = []
            for i, (name, field) in enumerate([('CPU', 'cpu_percent'), ('Memory', 'memory_percent')]):
                current = system[field]
                rows.append({'Resource': name, 'Current (%)': current,
                             'Estimated in 5 min (%)': prediction[field],
                             'Change (percentage points)': prediction[field] - current if current is not None else None,
                             'Selected method': prediction['methods'][i]})
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True, key='forecast_summary')
            st.plotly_chart(forecast_chart(system, prediction, dark=dark_mode), use_container_width=True,
                            theme=None, key='forecast_chart')
            st.caption(f"Estimate evaluated from {prediction['based_on']} · {prediction['training_pairs']} historical pairs · Updates at most once a minute.")
            if prediction['model_mae'] is not None:
                with st.expander('How reliable is this estimate?'):
                    st.write('The forest is compared with a baseline that carries the current value forward. Each resource uses the method with lower measured error.')
                    st.dataframe(pd.DataFrame({'Resource': ['CPU', 'Memory'],
                                              'Forest error (percentage points)': prediction['model_mae'],
                                              'Baseline error (percentage points)': prediction['baseline_mae']}), hide_index=True)
                    st.caption(f"Mean absolute error on {prediction['validation_pairs']} chronological held-out pairs. These are historical errors, not a confidence interval or guarantee of future accuracy.")
            else:
                st.info('The estimate currently carries the latest reading forward. Independent model validation needs more separated history.')

    if page == 'Diagnostics':
        st.subheader('Network throughput')
        a, b = st.columns(2)
        a.metric('Upload', rate(system.get('network_bytes_sent_per_sec')))
        b.metric('Download', rate(system.get('network_bytes_recv_per_sec')))
        st.caption('System-wide counter changes over the sample interval, including loopback where reported by the OS.')
        st.subheader('Disk activity')
        a, b = st.columns(2)
        a.metric('Read', rate(system.get('disk_read_bytes_per_sec')))
        b.metric('Write', rate(system.get('disk_write_bytes_per_sec')))
        st.caption('System-wide I/O rates; these differ from the filesystem capacity shown in the overview.')
        st.subheader('CPU by logical core')
        cores = system.get('cpu_per_core', [])
        if cores:
            st.bar_chart(pd.DataFrame({'Usage (%)': cores}, index=[f'Core {i}' for i in range(len(cores))]))
        else:
            st.caption('Per-core measurements are not available yet.')
        st.subheader('Memory and collection health')
        st.write(f"Available memory: {system.get('memory_available_bytes', 0) / 1024**3:.2f} GiB")
        st.write(f"Swap usage: {system.get('swap_percent', 0):.1f}%")
        st.write(f"Collection, storage and analysis: {previous['collection_ms']:.0f} ms for {len(processes)} visible processes")
        st.caption('This duration is measured elapsed work, not a prediction of responsiveness on other computers.')
        report = {'recorded_at': stamp, 'system': system, 'processes': processes,
                  'forecast': prediction, 'collection_ms': previous['collection_ms']}
        st.download_button('Download diagnostic snapshot (JSON)', json.dumps(report, indent=2, allow_nan=False),
                           'processscope_diagnostics.json', 'application/json', on_click='ignore')


live_view()
````

### database/__init__.py

````python
"""Local persistence for monitoring samples."""
````

### database/db_manager.py

````python
"""Store each sample atomically in a local SQLite database."""

import sqlite3
import json
from contextlib import closing
from pathlib import Path


class DatabaseManager:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute('PRAGMA journal_mode=WAL')
            db.executescript("""
                CREATE TABLE IF NOT EXISTS system_samples (
                    id INTEGER PRIMARY KEY, recorded_at TEXT NOT NULL,
                    cpu_percent REAL, memory_percent REAL, memory_used_bytes INTEGER,
                    memory_total_bytes INTEGER, disk_percent REAL, process_count INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS process_samples (
                    sample_id INTEGER NOT NULL REFERENCES system_samples(id), pid INTEGER NOT NULL,
                    name TEXT, status TEXT, created_at REAL, elapsed_seconds REAL,
                    cpu_percent REAL, memory_percent REAL, memory_bytes INTEGER,
                    threads INTEGER, read_bytes INTEGER, write_bytes INTEGER
                );
                CREATE INDEX IF NOT EXISTS process_sample_idx ON process_samples(sample_id);
            """)
            db.execute('BEGIN IMMEDIATE')
            for table in ('system_samples', 'process_samples'):
                columns = {row[1] for row in db.execute(f'PRAGMA table_info({table})')}
                if 'extra_metrics' not in columns:
                    db.execute(f"ALTER TABLE {table} ADD COLUMN extra_metrics TEXT NOT NULL DEFAULT '{{}}'")

    def save_sample(self, recorded_at, system, processes):
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute('PRAGMA foreign_keys=ON')
            cursor = db.execute(
                "INSERT INTO system_samples (recorded_at, cpu_percent, memory_percent, "
                "memory_used_bytes, memory_total_bytes, disk_percent, process_count) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (recorded_at, system['cpu_percent'], system['memory_percent'],
                 system['memory_used_bytes'], system['memory_total_bytes'], system['disk_percent'], len(processes)))
            db.execute('UPDATE system_samples SET extra_metrics=? WHERE id=?',
                       (json.dumps(system, allow_nan=False), cursor.lastrowid))
            fields = ('pid', 'name', 'status', 'created_at', 'elapsed_seconds', 'cpu_percent',
                      'memory_percent', 'memory_bytes', 'threads', 'read_bytes', 'write_bytes')
            db.executemany("INSERT INTO process_samples (sample_id, " + ', '.join(fields) + ", extra_metrics) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           [(cursor.lastrowid, *(p[field] for field in fields),
                             json.dumps({key: p.get(key) for key in ('read_bytes_per_sec', 'write_bytes_per_sec')}))
                            for p in processes])
            return cursor.lastrowid

    def system_history(self, limit=2000):
        with closing(sqlite3.connect(self.path)) as db:
            db.row_factory = sqlite3.Row
            rows = db.execute('SELECT recorded_at, cpu_percent, memory_percent, disk_percent, process_count '
                              'FROM system_samples ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
            return [dict(row) for row in reversed(rows)]
````

### models/__init__.py

````python
"""Reserved for future analysis models."""
````

### modules/__init__.py

````python
"""System and process monitoring components."""
````

### modules/anomaly_detector.py

````python
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
````

### modules/process_control.py

````python
"""Apply explicit local process actions using the current account's OS permissions."""

import math
import os

import psutil


class ProcessControlError(Exception):
    """An action could not be applied to the selected process."""


def control_process(pid, created_at, action):
    """Recheck identity and protected processes before sending one OS request.

    psutil's control methods also check PID reuse immediately before signalling.
    A return value confirms that the request was sent, not that a process exited.
    """
    if action not in ('suspend', 'resume', 'terminate'):
        raise ProcessControlError('Choose Suspend, Resume, or Terminate.')
    if (type(pid) is not int or pid <= 1 or isinstance(created_at, bool)
            or not isinstance(created_at, (int, float)) or not math.isfinite(created_at)
            or created_at <= 0):
        raise ProcessControlError('This process identity is invalid or protected. Select a current process.')
    try:
        current = psutil.Process(os.getpid())
        protected = {current.pid, *(parent.pid for parent in current.parents())}
        if pid in protected:
            raise ProcessControlError('The dashboard and its parent processes are protected.')
        target = psutil.Process(pid)
        if target.create_time() != created_at or not target.is_running():
            raise ProcessControlError('The selected process has exited or its PID was reused. Select it again.')
        if target.status() in (psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD):
            raise ProcessControlError('This process has already exited. Wait for its parent to collect its exit status.')
        # Do not allow managing another account's processes through this app.
        if target.username() != current.username():
            raise ProcessControlError('Only processes owned by the dashboard account can be managed.')
        getattr(target, action)()
    except psutil.NoSuchProcess as error:
        raise ProcessControlError('The selected process has exited. Refresh and select a current process.') from error
    except psutil.AccessDenied as error:
        raise ProcessControlError('The operating system denied access. No permission override was attempted.') from error
    except (psutil.Error, OSError, NotImplementedError) as error:
        raise ProcessControlError(f'The operating system could not apply this action: {error}') from error
    return f'{action.capitalize()} request sent to PID {pid}. Check its status in the next reading.'
````

### modules/process_history.py

````python
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
````

### modules/process_monitor.py

````python
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
````

### modules/recommendation_engine.py

````python
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
````

### modules/resource_predictor.py

````python
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
````

### modules/system_monitor.py

````python
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
````

### requirements-tested.txt

````text
altair==6.3.0
anyio==4.16.0
attrs==26.1.0
certifi==2026.10.23
charset-normalizer==3.5.2
click==8.5.1
cloudpickle==3.1.2
h11==0.16.0
idna==3.20
itsdangerous==2.2.0
Jinja2==3.1.6
joblib==1.6.0
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
MarkupSafe==3.0.4
narwhals==2.28.0
numpy==2.5.4
packaging==26.3
pandas==3.1.1
pillow==13.0.0
plotly==7.1.0
protobuf==7.36.2
psutil==7.2.2
pyarrow==26.0.1
pydeck==0.9.3
python-dateutil==4.0.0
python-multipart==0.0.33
referencing==0.37.0
requests==2.34.2
rpds-py==2026.9.1
scikit-learn==1.9.1
scipy==1.18.1
starlette==1.10.0
streamlit==1.67.0
threadpoolctl==3.8.0
typing_extensions==4.16.0
tzdata==2026.6
urllib3==2.8.0
uvicorn==0.54.0
websockets==17.4
````

### requirements.txt

````text
psutil>=5.9,<8
numpy>=1.26
pandas>=2.2
scikit-learn>=1.4
streamlit>=1.44
plotly>=5.20
````

### setup.py

````python
"""Interactive, cross-platform launcher using only the Python standard library."""

import os
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV = ROOT / 'os'
ENV_PYTHON = ENV / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')


def confirm(question):
    while True:
        answer = input(f'{question} [y/n]: ').strip().lower()
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        print('Please enter y or n.')


def main():
    print('\nProcessScope — guided setup\n')
    if sys.version_info < (3, 10):
        print('Python 3.10 or newer is required. Install it from python.org and try again.')
        return 1
    if not ENV_PYTHON.exists():
        if ENV.exists():
            print(f'The environment at {ENV} is not usable on this computer. Rename or remove it, then run setup again. Virtual environments cannot be copied between operating systems.')
            return 1
        if not confirm(f'Create a local Python environment at {ENV}?'):
            print('Setup stopped; no environment was created.')
            return 0
        venv.create(ENV, with_pip=True)

    check = subprocess.run([str(ENV_PYTHON), '-c',
                            'import psutil, numpy, pandas, sklearn, streamlit, plotly; '
                            'from importlib.metadata import version; '
                            'assert tuple(map(int, version("streamlit").split(".")[:2])) >= (1, 44)'],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if check.returncode:
        print('Some required packages are missing or need updating. Installing them requires an internet connection.')
        if not confirm('Install the required packages into the local environment?'):
            print('Setup stopped; packages were not installed.')
            return 0
        subprocess.run([str(ENV_PYTHON), '-m', 'pip', 'install', '-r', str(ROOT / 'requirements.txt')],
                       cwd=ROOT, check=True)
        subprocess.run([str(ENV_PYTHON), '-c',
                        'import psutil, numpy, pandas, sklearn, streamlit, plotly'], cwd=ROOT, check=True)
    else:
        print('The required packages are available.')
    if not confirm('Start the local dashboard and open the guide in your browser?'):
        print('Setup complete. Run this launcher again whenever you are ready.')
        return 0
    print('\nFollow the guide in your browser. Stop the dashboard with Ctrl+C in this window.\n')
    return subprocess.call([str(ENV_PYTHON), '-m', 'streamlit', 'run', str(ROOT / 'dashboard.py'),
                            '--server.address', 'localhost'], cwd=ROOT)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, subprocess.CalledProcessError) as error:
        print(f'Setup could not complete: {error}. Check your Python installation and internet connection, then try again.')
        sys.exit(1)
    except KeyboardInterrupt:
        print('\nStopped.')
        sys.exit(0)
````

### tests/test_analysis.py

````python
import unittest
from datetime import datetime, timedelta, timezone

from modules.anomaly_detector import detect_anomalies
from modules.resource_predictor import predict_resources, forecast_readiness
from modules.recommendation_engine import recommendations


class AnalysisTests(unittest.TestCase):
    def test_anomaly_needs_enough_processes(self):
        self.assertIsNone(detect_anomalies([]))

    def test_anomaly_detects_extreme_profile(self):
        data = [dict(pid=i, created_at=1, cpu_percent=1, memory_percent=1) for i in range(39)]
        data.append(dict(pid=99, created_at=1, cpu_percent=300, memory_percent=50))
        self.assertIn((99, 1), detect_anomalies(data))

    def test_forecast_requires_history_and_rejects_gaps(self):
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        data = [dict(recorded_at=(start + timedelta(seconds=i * 60)).isoformat(),
                     cpu_percent=i % 100, memory_percent=40) for i in range(30)]
        self.assertIsNone(predict_resources(data[:10]))
        forecast = predict_resources(data)
        self.assertEqual(forecast['horizon_seconds'], 300)
        self.assertGreaterEqual(forecast['training_pairs'], 20)
        self.assertTrue(0 <= forecast['cpu_percent'] <= 100)
        sparse = [dict(row, recorded_at=(start + timedelta(hours=i)).isoformat()) for i, row in enumerate(data)]
        self.assertIsNone(predict_resources(sparse))

    def test_recommendations_name_high_cpu_process(self):
        advice = recommendations({'cpu_percent': 95, 'memory_percent': 50},
                                 [{'pid': 12, 'name': 'worker', 'cpu_percent': 80}], None, None)
        self.assertIn('worker', advice[0])

    def test_forecast_reports_honest_validation_and_constant_baseline(self):
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        data = [dict(recorded_at=(start + timedelta(seconds=i * 10)).isoformat(),
                     cpu_percent=20, memory_percent=50) for i in range(180)]
        result = predict_resources(data)
        self.assertGreater(result['validation_pairs'], 0)
        self.assertEqual(result['methods'], ['Persistence baseline', 'Persistence baseline'])
        self.assertEqual(result['baseline_mae'], [0, 0])

    def test_equal_process_profiles_do_not_force_anomalies(self):
        data = [dict(pid=i, created_at=1, cpu_percent=1, memory_percent=1) for i in range(40)]
        self.assertEqual(detect_anomalies(data), set())

    def test_forecast_readiness_counts_actual_five_minute_pairs(self):
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        data = [dict(recorded_at=(start + timedelta(seconds=i * 10)).isoformat(),
                     cpu_percent=20, memory_percent=50) for i in range(50)]
        self.assertEqual(forecast_readiness(data)['valid_pairs'], 20)
        self.assertEqual(forecast_readiness(data[:20])['valid_pairs'], 0)


if __name__ == '__main__':
    unittest.main()
````

### tests/test_black_box_requirements.py

````python
"""Requirement-driven UI checks using controlled OS inputs, not live OS evidence.

Run: python -m unittest discover -s tests -p test_black_box_requirements.py -v
Only the OS collection/action boundary is substituted. Assertions use displayed
widgets, tables and messages; no application helper functions are called.
"""

from pathlib import Path
from copy import deepcopy
import time
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from modules.process_control import ProcessControlError


ROOT = Path(__file__).resolve().parents[1]


def widget(elements, label):
    return next(element for element in elements if element.label == label)


class BlackBoxRequirementTests(unittest.TestCase):
    def setUp(self):
        base = dict(created_at=123.0, status='sleeping', threads=1,
                    elapsed_seconds=10, read_bytes=None, write_bytes=None,
                    read_bytes_per_sec=None, write_bytes_per_sec=None)
        self.processes = [
            dict(base, pid=300, name='Alpha-worker', cpu_percent=19.9,
                 memory_percent=4.9, memory_bytes=1048576),
            dict(base, pid=301, name='Beta-worker', cpu_percent=20.0,
                 memory_percent=5.0, memory_bytes=2097152),
            dict(base, pid=302, name='Gamma-worker', cpu_percent=145.0,
                 memory_percent=6.0, memory_bytes=3145728),
        ]
        self.system = dict(cpu_percent=20.0, memory_percent=30.0,
                           memory_total_bytes=1024**3, disk_percent=40.0)
        for name, value in (
            ('modules.process_monitor.ProcessMonitor.sample', self.processes),
            ('modules.system_monitor.SystemMonitor.sample', self.system),
        ):
            patcher = patch(name, side_effect=lambda source=value: deepcopy(source))
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = patch('modules.process_control.control_process',
                        return_value='Action request sent to selected PID.')
        self.action = patcher.start()
        self.addCleanup(patcher.stop)
        self.app = AppTest.from_file(str(ROOT / 'dashboard.py'), default_timeout=20)

    def open(self, page='Overview'):
        self.app.run()
        for label in ('Set up monitoring →', 'Allow monitoring',
                      'Use session only', 'Open dashboard'):
            widget(self.app.button, label).click().run()
        if page != 'Overview':
            widget(self.app.radio, 'Workspace view').set_value(page).run()
        self.assertFalse(self.app.exception)

    def table(self):
        return next(item.value for item in self.app.dataframe
                    if 'PID' in item.value.columns and 'Status' in item.value.columns)

    def pressure_warning(self):
        return any('High resource usage' in item.value for item in self.app.warning)

    def review(self, action):
        self.open('Processes')
        widget(self.app.toggle, 'Enable process controls').set_value(True).run()
        widget(self.app.selectbox, 'Process').set_value((300, 123.0)).run()
        widget(self.app.selectbox, 'Action').set_value(action).run()
        widget(self.app.button, 'Review action').click().run()

    def test_BB01_dashboard_and_all_workspace_views(self):
        self.open()
        self.assertEqual(widget(self.app.selectbox, 'Refresh interval').value, 2)
        self.assertFalse(widget(self.app.toggle, 'Enable process controls').value)
        for page in ('Overview', 'Processes', 'Analysis', 'Diagnostics'):
            widget(self.app.radio, 'Workspace view').set_value(page).run()
            self.assertFalse(self.app.exception, page)
            self.assertEqual(widget(self.app.metric, 'CPU').value, '20.0%')
            self.assertEqual(widget(self.app.metric, 'RAM').value, '30.0%')

    def test_BB02_process_identity_state_cpu_and_memory(self):
        self.processes[0]['status'] = 'stopped'
        self.open('Processes')
        row = self.table().set_index('PID').loc[300]
        self.assertEqual(row['Name'], 'Alpha-worker')
        self.assertEqual(row['Status'], 'stopped')
        self.assertAlmostEqual(row['CPU %'], 19.9)
        self.assertAlmostEqual(row['Memory %'], 4.9)
        self.assertEqual(row['RAM (MiB)'], 1.0)
        self.assertEqual(self.table().set_index('PID').loc[302, 'CPU %'], 145.0)

    def test_BB03_search_name_pid_and_no_match(self):
        self.open('Processes')
        for query, expected in [('ALPHA', [300]), ('301', [301])]:
            widget(self.app.text_input, 'Search').set_value(query).run()
            self.assertEqual(self.table()['PID'].tolist(), expected)
        widget(self.app.text_input, 'Search').set_value('no-such-process').run()
        self.assertTrue(any('No visible processes match' in item.value for item in self.app.info))
        self.assertFalse(self.app.exception)

    def test_BB04_usage_filter_boundaries(self):
        self.open('Processes')
        for label in ('High CPU (≥ 20%)', 'High memory (≥ 5%)'):
            widget(self.app.selectbox, 'Show').set_value(label).run()
            self.assertEqual(set(self.table()['PID']), {301, 302})

    def test_BB05_sorting(self):
        self.open('Processes')
        for label, expected in [('CPU', [302, 301, 300]), ('Memory', [302, 301, 300]),
                                ('Name', [300, 301, 302]), ('PID', [300, 301, 302])]:
            widget(self.app.selectbox, 'Sort by').set_value(label).run()
            self.assertEqual(self.table()['PID'].tolist(), expected)

    def test_BB06_unavailable_cpu_and_io(self):
        self.system['cpu_percent'] = None
        self.processes[0]['cpu_percent'] = None
        self.open('Processes')
        self.assertEqual(widget(self.app.metric, 'CPU').value, 'Warming up')
        import pandas as pd
        self.assertTrue(pd.isna(self.table().set_index('PID').loc[300, 'CPU %']))
        self.assertTrue(self.table()['Read MiB/s'].isna().all())
        self.assertFalse(self.app.exception)

    def test_BB07_empty_process_snapshot(self):
        self.processes.clear()
        self.open('Processes')
        self.assertEqual(widget(self.app.metric, 'PROCESSES').value, '0')
        self.assertTrue(any('No visible processes match' in item.value for item in self.app.info))
        self.assertFalse(any(item.label == 'Process' for item in self.app.selectbox))
        self.assertFalse(self.app.exception)

    def test_BB08_cpu_warning_below_at_and_above_threshold(self):
        for value, expected in [(89.9, False), (90.0, True), (90.1, True)]:
            with self.subTest(cpu=value):
                self.system['cpu_percent'] = value
                self.app = AppTest.from_file(str(ROOT / 'dashboard.py'), default_timeout=20)
                self.open('Analysis')
                self.assertEqual(self.pressure_warning(), expected)
                self.assertEqual(widget(self.app.metric, 'CPU · threshold 90%').value,
                                 'High' if expected else 'Below')

    def test_BB09_memory_warning_below_at_and_above_threshold(self):
        for value, expected in [(84.9, False), (85.0, True), (85.1, True)]:
            with self.subTest(memory=value):
                self.system['memory_percent'] = value
                self.app = AppTest.from_file(str(ROOT / 'dashboard.py'), default_timeout=20)
                self.open('Analysis')
                self.assertEqual(self.pressure_warning(), expected)
                self.assertEqual(widget(self.app.metric, 'Memory · threshold 85%').value,
                                 'High' if expected else 'Below')

    def test_BB10_pressure_and_zombie_warnings_across_views(self):
        self.system['cpu_percent'] = 90.0
        self.processes[0]['status'] = 'zombie'
        self.open()
        for page in ('Overview', 'Processes', 'Analysis', 'Diagnostics'):
            widget(self.app.radio, 'Workspace view').set_value(page).run()
            self.assertTrue(self.pressure_warning())
            self.assertTrue(any('1 zombie' in item.value for item in self.app.warning))
            self.assertFalse(self.app.exception)

    def test_BB11_warning_identifies_largest_consumer(self):
        self.system['cpu_percent'] = 95.0
        self.system['memory_percent'] = 87.0
        self.open('Analysis')
        text = '\n'.join(item.value for item in self.app.markdown)
        self.assertIn('System CPU usage is 95.0%. Start by reviewing Gamma-worker (PID 302).', text)
        self.assertIn('System memory usage is 87.0%. Start by reviewing Gamma-worker (PID 302).', text)
        self.action.assert_not_called()

    def test_BB12_each_confirmed_action_dispatches_once(self):
        for action in ('suspend', 'resume', 'terminate'):
            with self.subTest(action=action):
                self.app = AppTest.from_file(str(ROOT / 'dashboard.py'), default_timeout=20)
                self.action.reset_mock()
                self.review(action)
                self.action.assert_not_called()
                widget(self.app.text_input, 'Type the target PID to confirm').set_value('300')
                widget(self.app.button, 'Confirm action').click().run()
                self.action.assert_called_once_with(300, 123.0, action)
                self.assertTrue(any('Action request sent' in item.value for item in self.app.info))
                self.app.run()
                self.action.assert_called_once()
                self.assertFalse(self.app.exception)

    def test_BB13_blank_wrong_and_nonnumeric_confirmations(self):
        self.review('terminate')
        for value in ('', '301', 'abc', '-1'):
            widget(self.app.text_input, 'Type the target PID to confirm').set_value(value)
            widget(self.app.button, 'Confirm action').click().run()
            self.assertTrue(any('PID does not match' in item.value for item in self.app.error))
            self.action.assert_not_called()
        widget(self.app.button, 'Cancel').click().run()
        self.assertFalse(any(item.label == 'Confirm action' for item in self.app.button))
        self.action.assert_not_called()

    def test_BB14_os_denial_is_visible(self):
        self.review('suspend')
        self.action.side_effect = ProcessControlError('The operating system denied access.')
        widget(self.app.text_input, 'Type the target PID to confirm').set_value('300')
        widget(self.app.button, 'Confirm action').click().run()
        self.assertTrue(any('denied access' in item.value for item in self.app.info))
        self.assertFalse(self.app.exception)

    def test_BB15_refresh_pause_and_resume(self):
        self.open()
        widget(self.app.selectbox, 'Refresh interval').set_value(1)
        widget(self.app.button, 'Apply settings').click().run()
        self.system['cpu_percent'] = 42.0
        time.sleep(1.1)
        self.app.run()
        self.assertEqual(widget(self.app.metric, 'CPU').value, '42.0%')
        widget(self.app.toggle, 'Pause collection').set_value(True).run()
        self.system['cpu_percent'] = 55.0
        time.sleep(1.1)
        self.app.run()
        self.assertEqual(widget(self.app.metric, 'CPU').value, '42.0%')
        self.assertTrue(any('Paused' in item.value for item in self.app.markdown))
        widget(self.app.toggle, 'Pause collection').set_value(False).run()
        self.assertEqual(widget(self.app.metric, 'CPU').value, '55.0%')
        self.assertFalse(self.app.exception)


if __name__ == '__main__':
    unittest.main()
````

### tests/test_charts.py

````python
import unittest

import pandas as pd

from visualization.charts import forecast_chart, history_chart, memory_chart, top_process_chart


class ChartTests(unittest.TestCase):
    def test_current_metrics_are_represented(self):
        ring = memory_chart(64)
        self.assertEqual(list(ring.data[0].values), [64, 36])
        processes = [{'name': 'worker', 'pid': 3, 'cpu_percent': 150}]
        bars = top_process_chart(processes, 'cpu_percent')
        self.assertEqual(list(bars.data[0].x), [150])
        self.assertIsNone(top_process_chart([], 'cpu_percent'))

    def test_history_and_forecast_use_input_values(self):
        history = pd.DataFrame([{'recorded_at': '2026-01-01', 'cpu_percent': 20,
                                 'memory_percent': 50, 'disk_percent': None}])
        chart = history_chart(history)
        self.assertEqual(list(chart.data[0].y), [20])
        forecast = forecast_chart({'cpu_percent': 20, 'memory_percent': 50},
                                  {'cpu_percent': 30, 'memory_percent': 60})
        self.assertEqual(list(forecast.data[0].y), [20, 50])
        self.assertEqual(list(forecast.data[1].y), [30, 60])

    def test_dark_charts_use_readable_labels(self):
        chart = memory_chart(42, dark=True)
        self.assertEqual(chart.layout.font.color, '#b6c2d7')
        self.assertEqual(chart.layout.annotations[0].font.color, '#edf1fa')

    def test_history_separates_resources_without_changing_measurements(self):
        history = pd.DataFrame([{'recorded_at': '2026-01-01', 'cpu_percent': 20,
                                 'memory_percent': 75, 'disk_percent': 30}])
        chart = history_chart(history, focus=True)
        self.assertEqual([trace.yaxis for trace in chart.data], ['y', 'y2', 'y3'])
        self.assertEqual(list(chart.data[1].y), [75])
        self.assertEqual(list(chart.layout.yaxis2.range), [72, 78])

    def test_long_process_labels_keep_full_identity_on_hover(self):
        name = 'A very long process name that should not take over the chart'
        chart = top_process_chart([{'name': name, 'pid': 12, 'cpu_percent': 130}], 'cpu_percent')
        self.assertLess(len(chart.data[0].y[0]), len(name))
        self.assertEqual(chart.data[0].customdata[0][0], name)


if __name__ == '__main__':
    unittest.main()
````

### tests/test_dashboard.py

````python
"""Exercise dashboard interactions with fixed OS readings and mocked actions."""

from pathlib import Path
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from modules.process_control import ProcessControlError


ROOT = Path(__file__).resolve().parents[1]


def widget(elements, label):
    return next(element for element in elements if element.label == label)


class DashboardTests(unittest.TestCase):
    def setUp(self):
        process = dict(pid=300, created_at=123.0, name='worker', status='sleeping',
                       cpu_percent=10.0, memory_percent=2.0, memory_bytes=1024**2,
                       threads=1, elapsed_seconds=10, read_bytes=None, write_bytes=None,
                       read_bytes_per_sec=None, write_bytes_per_sec=None)
        self.processes = [process, dict(process, pid=301, name='other-worker')]
        self.system = dict(cpu_percent=20.0, memory_percent=30.0,
                           memory_total_bytes=1024**3, disk_percent=40.0)
        for name, readings in [('modules.process_monitor.ProcessMonitor.sample', self.processes),
                               ('modules.system_monitor.SystemMonitor.sample', self.system)]:
            patcher = patch(name, return_value=readings)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = patch('modules.process_control.control_process', return_value='Suspend request sent to PID 300.')
        self.control = patcher.start()
        self.addCleanup(patcher.stop)
        self.app = AppTest.from_file(str(ROOT / 'dashboard.py'), default_timeout=20)

    def open_dashboard(self):
        self.app.session_state['setup_step'] = 'ready'
        self.app.session_state['save_history'] = False
        self.app.run()
        self.assertFalse(self.app.exception)

    def review_suspend(self):
        self.open_dashboard()
        widget(self.app.radio, 'Workspace view').set_value('Processes').run()
        widget(self.app.toggle, 'Enable process controls').set_value(True).run()
        widget(self.app.selectbox, 'Process').set_value((300, 123.0)).run()
        widget(self.app.button, 'Review action').click().run()

    def test_guide_reaches_dashboard_with_controls_off(self):
        self.app.run()
        for label in ('Set up monitoring →', 'Allow monitoring', 'Use session only', 'Open dashboard'):
            widget(self.app.button, label).click().run()
            self.assertFalse(self.app.exception)
        self.assertFalse(widget(self.app.toggle, 'Enable process controls').value)
        self.assertEqual(widget(self.app.selectbox, 'Refresh interval').value, 2)
        self.assertTrue(self.app.metric)
        for page in ('Processes', 'Analysis', 'Diagnostics', 'Overview'):
            widget(self.app.radio, 'Workspace view').set_value(page).run()
            self.assertFalse(self.app.exception, page)

    def test_review_wrong_pid_and_cancel_do_not_send_actions(self):
        self.review_suspend()
        self.control.assert_not_called()
        widget(self.app.text_input, 'Type the target PID to confirm').set_value('301')
        widget(self.app.button, 'Confirm action').click().run()
        self.assertTrue(any('PID does not match' in error.value for error in self.app.error))
        self.control.assert_not_called()
        widget(self.app.button, 'Cancel').click().run()
        self.assertNotIn('pending_action', self.app.session_state)
        self.control.assert_not_called()
        self.assertFalse(self.app.exception)

    def test_confirmation_uses_reviewed_target_after_selection_changes(self):
        self.review_suspend()
        widget(self.app.selectbox, 'Process').set_value((301, 123.0)).run()
        widget(self.app.selectbox, 'Action').set_value('resume').run()
        widget(self.app.text_input, 'Type the target PID to confirm').set_value('300')
        widget(self.app.button, 'Confirm action').click().run()
        self.assertFalse(self.app.exception)
        self.control.assert_called_once_with(300, 123.0, 'suspend')
        self.assertEqual(self.app.session_state['action_history'][-1]['outcome'], 'Request sent')
        self.assertNotIn('pending_action', self.app.session_state)
        self.app.run()
        self.control.assert_called_once()

    def test_os_denial_is_logged_and_does_not_crash_dashboard(self):
        self.review_suspend()
        self.control.side_effect = ProcessControlError('The operating system denied access.')
        widget(self.app.text_input, 'Type the target PID to confirm').set_value('300')
        widget(self.app.button, 'Confirm action').click().run()
        self.assertFalse(self.app.exception)
        self.assertEqual(self.app.session_state['action_history'][-1]['outcome'], 'Blocked or failed')
        self.assertIn('denied access', self.app.session_state['action_notice'])

    def test_disabling_controls_cancels_pending_action(self):
        self.review_suspend()
        widget(self.app.toggle, 'Enable process controls').set_value(False).run()
        self.assertNotIn('pending_action', self.app.session_state)
        self.assertFalse(any(button.label == 'Confirm action' for button in self.app.button))
        self.control.assert_not_called()

    def test_resource_pressure_and_zombies_are_visible_on_every_page(self):
        self.system['cpu_percent'] = 95.0
        self.processes[0]['status'] = 'zombie'
        self.open_dashboard()
        for page in ('Overview', 'Processes', 'Analysis', 'Diagnostics'):
            widget(self.app.radio, 'Workspace view').set_value(page).run()
            self.assertFalse(self.app.exception)
            warnings = [warning.value for warning in self.app.warning]
            self.assertTrue(any('High resource usage' in text for text in warnings))
            self.assertTrue(any('zombie' in text for text in warnings))


if __name__ == '__main__':
    unittest.main()
````

### tests/test_database.py

````python
import sqlite3
import json
from contextlib import closing
import tempfile
import unittest
from pathlib import Path

from database.db_manager import DatabaseManager


class DatabaseTests(unittest.TestCase):
    def test_upgrades_original_schema_without_losing_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'old.db'
            with closing(sqlite3.connect(path)) as connection, connection:
                connection.execute('CREATE TABLE system_samples (id INTEGER PRIMARY KEY, recorded_at TEXT NOT NULL, '
                                   'cpu_percent REAL, memory_percent REAL, memory_used_bytes INTEGER, '
                                   'memory_total_bytes INTEGER, disk_percent REAL, process_count INTEGER NOT NULL)')
                connection.execute("INSERT INTO system_samples VALUES (1, 'old reading', 10, 20, 30, 40, 50, 0)")
            DatabaseManager(path)
            with closing(sqlite3.connect(path)) as connection:
                self.assertEqual(connection.execute('SELECT recorded_at, extra_metrics FROM system_samples').fetchone(),
                                 ('old reading', '{}'))

    def test_persists_sample_and_null_process_metrics(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'history.db'
            db = DatabaseManager(path)
            system = dict(cpu_percent=12.0, memory_percent=30.0, memory_used_bytes=300,
                          memory_total_bytes=1000, disk_percent=None)
            process = dict(pid=123, name='example', status='running', created_at=1.0,
                           elapsed_seconds=5.0, cpu_percent=None, memory_percent=1.0,
                           memory_bytes=10, threads=2, read_bytes=None, write_bytes=None)
            sample_id = db.save_sample('2026-01-01T00:00:00+00:00', system, [process])
            with closing(sqlite3.connect(path)) as connection:
                self.assertEqual(connection.execute('SELECT process_count, disk_percent FROM system_samples').fetchone(), (1, None))
                self.assertEqual(connection.execute('SELECT sample_id, pid, cpu_percent, read_bytes FROM process_samples').fetchone(), (sample_id, 123, None, None))
            # Reopening an existing database preserves observations and its schema.
            DatabaseManager(path)
            with closing(sqlite3.connect(path)) as connection:
                extras = connection.execute('SELECT extra_metrics FROM system_samples').fetchone()[0]
                self.assertEqual(json.loads(extras)['cpu_percent'], 12)

    def test_failed_process_insert_rolls_back_system_sample(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'history.db'
            db = DatabaseManager(path)
            system = dict(cpu_percent=1, memory_percent=2, memory_used_bytes=3,
                          memory_total_bytes=4, disk_percent=5)
            with self.assertRaises(KeyError):
                db.save_sample('now', system, [{}])
            with closing(sqlite3.connect(path)) as connection:
                self.assertEqual(connection.execute('SELECT count(*) FROM system_samples').fetchone()[0], 0)


if __name__ == '__main__':
    unittest.main()
````

### tests/test_monitoring.py

````python
import unittest
from contextlib import nullcontext
from collections import namedtuple
from unittest.mock import Mock, patch

from modules.system_monitor import cpu_utilization, counter_rate, SystemMonitor
from modules.process_history import ProcessHistory
from modules.resource_predictor import ResourcePredictor
from modules.process_monitor import ProcessMonitor


class MonitoringTests(unittest.TestCase):
    def test_process_intervals_io_rates_and_pid_reuse(self):
        process = Mock(pid=42)
        process.oneshot.side_effect = lambda: nullcontext()
        process.create_time.side_effect = [10, 10, 11]
        process.cpu_times.side_effect = [Mock(user=n, system=0) for n in (1, 2, 4)]
        process.io_counters.side_effect = [Mock(read_bytes=n, write_bytes=n) for n in (100, 2100, 3100)]
        process.name.return_value = 'worker'
        process.status.return_value = 'running'
        process.memory_percent.return_value = 1
        process.memory_info.return_value = Mock(rss=1024)
        process.num_threads.return_value = 1
        with patch('modules.process_monitor.psutil.process_iter', return_value=[process]), \
             patch('modules.process_monitor.time.monotonic', side_effect=[1, 3, 5]):
            monitor = ProcessMonitor()
            self.assertIsNone(monitor.sample()[0]['cpu_percent'])
            reading = monitor.sample()[0]
            self.assertEqual(reading['cpu_percent'], 50)
            self.assertEqual(reading['read_bytes_per_sec'], 1000)
            reused = monitor.sample()[0]
            self.assertIsNone(reused['cpu_percent'])
            self.assertIsNone(reused['read_bytes_per_sec'])

    def test_cpu_excludes_guest_and_iowait(self):
        Times = namedtuple('Times', 'user system idle iowait guest')
        # 20 busy ticks, 60 idle ticks, 20 waiting; guest already in user.
        result = cpu_utilization(Times(0, 0, 0, 0, 0), Times(15, 5, 60, 20, 5))
        self.assertAlmostEqual(result, 20)

    def test_counter_rate_never_fabricates_reset_or_first_rates(self):
        self.assertEqual(counter_rate(100, 200, 2), 50)
        self.assertIsNone(counter_rate(None, 200, 2))
        self.assertIsNone(counter_rate(200, 100, 2))
        self.assertIsNone(counter_rate(100, 200, 0))

    def test_system_cpu_uses_owned_counters_instead_of_thread_local_percent(self):
        Times = namedtuple('Times', 'user system idle')
        before, after = Times(0, 0, 0), Times(2, 1, 7)
        with patch('modules.system_monitor.psutil.cpu_times', side_effect=[before, [before], after, [after]]), \
             patch('modules.system_monitor.psutil.cpu_percent', side_effect=AssertionError('thread dependent call')), \
             patch('modules.system_monitor.psutil.virtual_memory', return_value=Mock(percent=20, used=2, available=8, total=10)), \
             patch('modules.system_monitor.psutil.swap_memory', return_value=Mock(percent=0, used=0)), \
             patch('modules.system_monitor.psutil.disk_usage', return_value=Mock(percent=30)):
            monitor = SystemMonitor('/')
            self.assertEqual(monitor.sample()['cpu_percent'], 30)

    def test_process_history_is_bounded_and_handles_pid_reuse(self):
        history = ProcessHistory(limit=2)
        process = dict(pid=1, created_at=1, cpu_percent=10, memory_bytes=1024)
        for i in range(3):
            history.update(str(i), [process])
        self.assertEqual(len(history.for_process(1, 1)), 2)
        history.update('new', [dict(process, created_at=2)])
        self.assertEqual(history.for_process(1, 1), [])
        self.assertEqual(len(history.for_process(1, 2)), 1)

    def test_predictor_reuses_result_between_training_intervals(self):
        with patch('modules.resource_predictor.time.monotonic', side_effect=[0, 5, 65]), \
             patch('modules.resource_predictor.predict_resources', return_value={'cpu_percent': 10}) as fit:
            predictor = ResourcePredictor()
            predictor.predict([])
            predictor.predict([])
            self.assertEqual(fit.call_count, 1)
            predictor.predict([])
            self.assertEqual(fit.call_count, 2)


if __name__ == '__main__':
    unittest.main()
````

### tests/test_process_control.py

````python
import os
import subprocess
import sys
import time
import unittest
from unittest.mock import Mock, patch

import psutil

from modules.process_control import ProcessControlError, control_process


class ProcessControlTests(unittest.TestCase):
    def setUp(self):
        self.current = Mock(pid=200)
        self.current.parents.return_value = [Mock(pid=100)]
        self.current.username.return_value = 'owner'
        self.target = Mock(pid=300)
        self.target.create_time.return_value = 123.0
        self.target.is_running.return_value = True
        self.target.username.return_value = 'owner'
        self.target.status.return_value = psutil.STATUS_SLEEPING

    def run_action(self, action='suspend', created=123.0, pid=300):
        with patch('modules.process_control.psutil.Process', side_effect=[self.current, self.target]):
            return control_process(pid, created, action)

    def test_sends_only_the_requested_action(self):
        for action in ('suspend', 'resume', 'terminate'):
            self.target.reset_mock()
            self.assertIn('request sent', self.run_action(action))
            getattr(self.target, action).assert_called_once_with()
            for other in {'suspend', 'resume', 'terminate'} - {action}:
                getattr(self.target, other).assert_not_called()

    def test_stale_pid_is_never_signalled(self):
        with self.assertRaisesRegex(ProcessControlError, 'PID was reused'):
            self.run_action(created=122.0)
        self.target.suspend.assert_not_called()

    def test_protects_dashboard_ancestors_and_system_pids(self):
        for pid in (0, 1, 100, 200):
            with self.subTest(pid=pid), self.assertRaises(ProcessControlError):
                self.run_action(pid=pid)
        self.target.suspend.assert_not_called()

    def test_other_account_and_zombie_processes_are_blocked(self):
        self.target.username.return_value = 'system'
        with self.assertRaisesRegex(ProcessControlError, 'owned'):
            self.run_action()
        self.target.username.return_value = 'owner'
        self.target.status.return_value = psutil.STATUS_ZOMBIE
        with self.assertRaisesRegex(ProcessControlError, 'already exited'):
            self.run_action()
        self.target.suspend.assert_not_called()

    def test_permission_and_exit_errors_have_actionable_messages(self):
        for error, message in [(psutil.AccessDenied(300), 'denied access'),
                               (psutil.NoSuchProcess(300), 'has exited')]:
            self.target.suspend.side_effect = error
            with self.subTest(error=error), self.assertRaisesRegex(ProcessControlError, message):
                self.run_action()

    def test_rejects_unknown_actions_and_invalid_identities(self):
        for pid, created, action in [(300, 123, 'kill'), (True, 123, 'suspend'),
                                     (300, float('nan'), 'suspend'), (300, None, 'suspend')]:
            with self.subTest(pid=pid, created=created), self.assertRaises(ProcessControlError):
                control_process(pid, created, action)

    @unittest.skipIf(os.name == 'nt', 'Real process lifecycle is verified on POSIX; Windows requires a Windows run.')
    def test_real_disposable_child_can_be_suspended_resumed_and_terminated(self):
        try:
            psutil.Process().parents()
        except (psutil.Error, OSError) as error:
            self.skipTest(f'This environment blocks OS process inspection: {error}')
        # This test acts only on the child it creates, never an existing user app.
        child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])
        try:
            process = psutil.Process(child.pid)
            created = process.create_time()
            control_process(child.pid, created, 'suspend')
            deadline = time.monotonic() + 3
            while process.status() != psutil.STATUS_STOPPED and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertEqual(process.status(), psutil.STATUS_STOPPED)
            control_process(child.pid, created, 'resume')
            deadline = time.monotonic() + 3
            while process.status() == psutil.STATUS_STOPPED and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertNotEqual(process.status(), psutil.STATUS_STOPPED)
            control_process(child.pid, created, 'terminate')
            child.wait(timeout=3)
            self.assertIsNotNone(child.returncode)
        finally:
            if child.poll() is None:
                process.resume()
                child.kill()
                child.wait(timeout=3)


if __name__ == '__main__':
    unittest.main()
````

### tests/test_setup.py

````python
import unittest
from unittest.mock import Mock, patch

import setup


class SetupTests(unittest.TestCase):
    def test_declining_environment_creation_stops_setup(self):
        with patch.object(setup, 'ENV_PYTHON', Mock(exists=Mock(return_value=False))), \
             patch.object(setup, 'ENV', Mock(exists=Mock(return_value=False))), \
             patch('builtins.input', return_value='n'), patch.object(setup.venv, 'create') as create:
            self.assertEqual(setup.main(), 0)
            create.assert_not_called()

    def test_declining_install_never_starts_dashboard(self):
        with patch.object(setup, 'ENV_PYTHON', Mock(exists=Mock(return_value=True))), \
             patch.object(setup.subprocess, 'run', return_value=Mock(returncode=1)), \
             patch.object(setup.subprocess, 'call') as start, patch('builtins.input', return_value='n'):
            self.assertEqual(setup.main(), 0)
            start.assert_not_called()


if __name__ == '__main__':
    unittest.main()
````

### tools/build_project_report.py

````python
"""Build the guideline report with a source appendix from the current project."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    body = (ROOT / 'docs' / 'report-body.md').read_text(encoding='utf-8')
    sources = sorted({path for pattern in (
        '*.py', 'modules/*.py', 'models/*.py', 'database/*.py', 'visualization/*.py',
        'visualization/*.css', 'tests/*.py', 'tools/*.py', '*.bat', '*.command',
        'requirements*.txt', '.streamlit/*.toml', '.gitignore',
    ) for path in ROOT.glob(pattern) if path.is_file()})
    if not sources or ROOT / 'dashboard.py' not in sources:
        raise RuntimeError('No dashboard source found. Keep this tool in the project tools directory.')
    parts = [body.rstrip(), '\n## Appendix C. Complete project source\n',
             'Rebuild this appendix after code changes with `python tools/build_project_report.py`.\n']
    for source in sources:
        language = {'.py': 'python', '.css': 'css', '.toml': 'toml',
                    '.bat': 'bat', '.command': 'sh'}.get(source.suffix, 'text')
        parts.append(f'### {source.relative_to(ROOT).as_posix()}\n\n'
                     f'````{language}\n{source.read_text(encoding="utf-8").rstrip()}\n````\n')
    review = ROOT / 'docs' / 'black-box-testing.md'
    if review.exists():
        # Preserve the eight required sections and appendices A-C, then attach
        # the separately maintained acceptance evidence as a supplemental appendix.
        review_lines = review.read_text(encoding='utf-8').splitlines()
        appendix = '\n'.join(
            '#' + line if line.startswith('#') else line
            for line in review_lines[1:]
        ).strip()
        appendix = appendix.replace('](verification/', '](docs/verification/')
        parts.append('\n## Appendix D. Requirements and black box testing\n\n' + appendix + '\n')
    destination = ROOT / 'PROJECT_REPORT.md'
    destination.write_text('\n'.join(parts), encoding='utf-8')
    print(f'Created {destination.name} with {len(sources)} source files.')


if __name__ == '__main__':
    main()
````

### visualization/__init__.py

````python
"""Reserved for the future dashboard."""
````

### visualization/charts.py

````python
"""Small, consistent visualizations built from observed measurements."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

COLORS = {'CPU': '#138f87', 'Memory': '#5d88b5', 'Disk capacity': '#a3aeb7'}


def style_chart(fig, height=270, dark=False):
    fig.update_layout(height=height, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(family='Avenir Next, Segoe UI, sans-serif', color='#b6c2d7' if dark else '#63718b', size=12),
                      margin=dict(l=60, r=16, t=35, b=45), legend_title_text='',
                      legend=dict(orientation='h', y=1.1, x=0))
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor='#344155' if dark else '#e9edf4', zeroline=False)
    return fig


def history_chart(history, dark=False, focus=False):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=.12,
                        subplot_titles=['CPU utilization', 'Memory utilization', 'Disk capacity used'])
    for row, (label, field) in enumerate([('CPU', 'cpu_percent'), ('Memory', 'memory_percent'), ('Disk capacity', 'disk_percent')], 1):
        fig.add_trace(go.Scatter(x=history['recorded_at'], y=history[field], name=label,
                                mode='lines+markers' if len(history) < 3 else 'lines',
                                line=dict(color=COLORS[label], width=2), marker=dict(size=5),
                                connectgaps=False, hovertemplate='%{y:.2f}%<extra>'+label+'</extra>'), row=row, col=1)
        valid = history[field].dropna()
        bounds = [max(0, float(valid.min()) - 3), min(100, float(valid.max()) + 3)] if focus and len(valid) else [0, 100]
        fig.update_yaxes(range=bounds, ticksuffix='%', row=row, col=1)
    style_chart(fig, 650, dark)
    fig.update_layout(showlegend=False, hovermode='x unified',
                      uirevision='resource-history-focus' if focus else 'resource-history-full')
    fig.update_xaxes(title_text='Time (UTC)', row=3, col=1)
    fig.update_annotations(font=dict(size=12, color='#b6c2d7' if dark else '#63718b'), x=0, xanchor='left')
    return fig


def memory_chart(percent, dark=False):
    fig = go.Figure(go.Pie(labels=['Used', 'Available'], values=[percent, max(0, 100 - percent)],
                           hole=.78, sort=False, marker=dict(colors=['#57b8ae', '#344155' if dark else '#e9eef2'], line=dict(width=0)),
                           textinfo='none', hovertemplate='%{label}: %{value:.1f}%<extra></extra>'))
    fig.add_annotation(text=f'<b>{percent:.0f}%</b><br><span style="font-size:11px">in use</span>',
                       x=.5, y=.5, showarrow=False, font=dict(size=22, color='#edf1fa' if dark else '#283650'))
    fig.update_layout(showlegend=False)
    style_chart(fig, 300, dark)
    fig.update_layout(margin=dict(l=12, r=12, t=12, b=12), uirevision='memory-allocation')
    return fig


def top_process_chart(processes, metric, dark=False):
    usable = [p for p in processes if p.get(metric) is not None and p[metric] > 0]
    if not usable:
        return None
    top = sorted(usable, key=lambda p: p[metric], reverse=True)[:7]
    frame = pd.DataFrame([{'Process': f"{p['name'][:22] + '…' if len(p['name']) > 22 else p['name']} · {p['pid']}",
                           'Full name': p['name'], 'PID': p['pid'], 'Usage': p[metric]} for p in reversed(top)])
    fig = px.bar(frame, x='Usage', y='Process', orientation='h', color_discrete_sequence=['#138f87'],
                 labels={'Usage': 'Process CPU (%)', 'Process': ''}, custom_data=['Full name', 'PID'])
    fig.update_traces(hovertemplate='%{customdata[0]}<br>PID %{customdata[1]} · %{x:.2f}% CPU<extra></extra>',
                      texttemplate='%{x:.1f}%', textposition='outside', cliponaxis=False)
    fig.update_yaxes(showgrid=False, automargin=True)
    fig.update_xaxes(ticksuffix='%', gridcolor='#344155' if dark else '#e9edf4', showgrid=True)
    fig.update_xaxes(range=[0, max(frame['Usage'].max() * 1.2, 1)])
    style_chart(fig, 350, dark)
    fig.update_layout(margin=dict(l=190, r=45, t=15, b=45), uirevision='top-processes')
    return fig


def forecast_chart(system, forecast, dark=False):
    frame = pd.DataFrame([{'Resource': label, 'Time': when, 'Usage': value}
                          for label, key in [('CPU', 'cpu_percent'), ('Memory', 'memory_percent')]
                          for when, value in [('Now', system[key]), ('Estimated in 5 min', forecast[key])]])
    fig = px.bar(frame, x='Resource', y='Usage', color='Time', barmode='group',
                 color_discrete_map={'Now': '#a3aeb7', 'Estimated in 5 min': '#138f87'},
                 labels={'Usage': 'Utilization (%)'})
    fig.update_yaxes(range=[0, 100], ticksuffix='%')
    fig.update_traces(hovertemplate='%{y:.1f}%<extra>%{fullData.name}</extra>')
    return style_chart(fig, 270, dark)
````

### visualization/dashboard.css

````css
/* ProcessScope: compact monitoring workspace. No remote assets required. */
:root { --bg:#000; --surface:#0b0b0b; --text:#ededed; --muted:#a0a0a0; --line:#262626; --side:#050505; --accent:#85c7b8; color-scheme:dark; }
.stApp { background:var(--bg); color:var(--text); }
.stApp, button, input, label { font-family:'Avenir Next','Segoe UI',sans-serif; }
header[data-testid="stHeader"] { background:var(--bg); }
.block-container { max-width:1440px; padding:2.8rem 2rem 3rem; }
[data-testid="stToolbar"] { display:none; }
[data-testid="stMarkdownContainer"] p,[data-testid="stWidgetLabel"] p { color:var(--text); }
[data-testid="stCaptionContainer"] p { color:var(--muted); }
[data-baseweb="select"] div,input { background:var(--surface) !important; color:var(--text) !important; }
input::placeholder { color:var(--muted) !important; }
[data-testid="stSelectbox"] svg { color:var(--muted); }
[data-baseweb="popover"] { color:var(--text); }
[data-testid="stAlert"] { background:var(--surface); color:var(--text); border:1px solid var(--line); }
h1,h2,h3 { color:var(--text) !important; font-family:'Avenir Next','Segoe UI',sans-serif !important; font-weight:600 !important; letter-spacing:-.035em; }
h1 { font-size:1.85rem !important; }
h2 { font-size:1.15rem !important; }
h3 { font-size:1rem !important; }
[data-testid="stSidebar"] { background:var(--side); border-right:1px solid var(--line); }
[data-testid="stSidebar"] h2 { font-size:.9rem !important; letter-spacing:0; }
[data-testid="stSidebarHeader"] { visibility:visible !important; opacity:1 !important; }
[data-testid="stSidebarCollapseButton"] span,[data-testid="stSidebarCollapsedControl"] span { color:var(--muted) !important; }
.brand { display:flex; gap:10px; align-items:center; padding:0 0 25px; border-bottom:1px solid var(--line); margin-bottom:22px; }
.brand-symbol { width:30px; height:30px; border-radius:7px; background:var(--text); color:var(--bg); display:grid; place-items:center; font-family:Consolas,monospace; font-size:18px; }
.brand-name { font-weight:700; font-size:17px; color:var(--text); letter-spacing:-.04em; }
.brand-subtitle { color:var(--muted); font-size:10px; letter-spacing:.09em; text-transform:uppercase; }
.workspace-label { font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:.12em; margin:0 0 8px; }
.workspace-title { font-size:30px; letter-spacing:-.045em; font-weight:600; color:var(--text); margin:0 0 8px; }
.workspace-description { font-size:13px; color:var(--muted); margin-bottom:25px; }
[data-testid="stRadio"] > div { gap:10px 28px; width:100%; padding-bottom:0; border-bottom:1px solid var(--line); }
[data-testid="stRadio"] label { padding:10px 4px 14px; border-bottom:2px solid transparent; }
[data-testid="stRadio"] label > div > div:first-child { display:none; }
[data-testid="stRadio"] label:has(input:checked) { border-bottom-color:var(--accent); color:var(--accent); }
[data-testid="stRadio"] label:focus-within { outline:2px solid var(--accent); outline-offset:3px; }
[data-testid="stRadio"] label p { font-size:14px; font-weight:600; }
[data-testid="stMetric"] { padding:18px 16px; background:var(--surface); border:1px solid var(--line); border-radius:8px; }
[data-testid="stMetricLabel"] { color:var(--muted); font-size:12px; }
[data-testid="stMetricValue"] { color:var(--text); font-family:'SFMono-Regular',Consolas,monospace; font-size:clamp(1.15rem,2.2vw,2rem); letter-spacing:-.055em; }
[data-testid="stVerticalBlockBorderWrapper"] > div { border-color:var(--line) !important; border-radius:9px !important; background:var(--surface); }
[data-testid="stCaptionContainer"] { color:var(--muted); }
[data-testid="stAlert"] { border-radius:6px; }
.stButton button,.stDownloadButton button { border-radius:7px; font-size:12px; font-weight:600; background:var(--surface); color:var(--text); border:1px solid var(--line); min-height:38px; }
.stButton button[kind="primary"] { background:var(--text); color:var(--bg); border-color:var(--text); }
.stButton button[kind="primary"] p { color:var(--bg); }
.stButton button:hover,.stDownloadButton button:hover { border-color:var(--accent); color:var(--accent); }
.stButton button[kind="primary"]:hover { opacity:.9; color:var(--bg); }
.stButton button:focus-visible,.stDownloadButton button:focus-visible { outline:2px solid var(--accent); outline-offset:3px; }
.section-note { color:var(--muted); font-size:12px; margin-top:-6px; margin-bottom:14px; }
.status-line { display:flex; gap:8px; align-items:center; color:var(--muted); font-size:11px; margin:14px 0 24px; }
.status-dot { height:6px; width:6px; background:var(--accent); border-radius:50%; }
.status-dot.paused { background:var(--muted); }
/* Keep the last reading visible while Streamlit replaces a fragment. */
[data-stale="true"] { opacity:1 !important; }
[data-testid="stForm"] { border:0; padding:0; }
[data-testid="stRadio"] { margin-bottom:12px; }
.welcome-top { display:flex; align-items:center; gap:11px; font-weight:650; font-size:16px; letter-spacing:-.03em; padding:0 0 28px; border-bottom:1px solid var(--line); }
.welcome-logo { font-size:25px; line-height:1; }
.welcome-local { margin-left:auto; color:var(--muted); font-size:10px; font-weight:400; letter-spacing:.12em; }
.welcome-intro { padding:52px 0 24px; }
.welcome-kicker,.setup-label { color:var(--muted); font-size:10px; letter-spacing:.14em; font-weight:500; margin-bottom:22px; }
.welcome-intro h1 { font-size:clamp(32px,4.3vw,56px) !important; line-height:1.08; letter-spacing:-.055em; margin:0 0 20px; padding:0; font-weight:550 !important; }
.welcome-intro p { color:var(--muted); font-size:15px; line-height:1.75; margin:0; }
.welcome-footnote { color:var(--muted); font-size:11px; text-align:center; margin:4px 0 32px; }
.welcome-features { border-top:1px solid var(--line); }
.welcome-features > div { display:flex; align-items:baseline; gap:22px; padding:18px 0; border-bottom:1px solid var(--line); }
.welcome-features > div > span { color:var(--muted); font-size:11px; font-family:Consolas,monospace; }
.welcome-features strong { font-size:13px; font-weight:550; color:var(--text); }
.welcome-features section p { color:var(--muted); font-size:12px; line-height:1.6; margin:4px 0 0; }
.welcome-bottom { display:flex; justify-content:space-between; gap:20px; color:var(--muted); border-top:1px solid var(--line); padding-top:18px; margin-top:48px; font-size:10px; }
.setup-label { margin-top:60px; }
@media(max-width:800px) { .block-container { padding-left:1rem; padding-right:1rem; } [data-testid="stMetric"] { padding:13px 9px; } }
@media(prefers-reduced-motion:reduce) { *,*::before,*::after { animation:none !important; transition:none !important; } }
````


## Appendix D. Requirements and black box testing

Review date: 15 November 2026 (India). Application: ProcessScope.

### 1. Scope and verdict

The report structurally matches the assignment and describes functionality aligned with Project 13. Submission readiness is conditional: real team/repository evidence is missing and live OS behavior must be demonstrated on the presentation machine. A description of a feature is not evidence that the feature passed a test.

The assignment PDF was read in full (10 pages). Pages 1-4 provide the general instructions, report format and evaluation; page 6 contains Project 13. The other project statements are alternative assignments. The filename's `31` does not change the user's assigned Project 13. AI anomaly detection and forecasting are optional additions here.

The PDF is a requirements source for this review. Its embedded example AI prompt is assignment content, not a separate request to generate an implementation. This review adds verification and documentation; it does not rewrite the student's application.

### 2. Required behavior and traceability

| ID | Project 13 requirement (PDF page 6) | Acceptance condition | Evidence and limits |
| --- | --- | --- | --- |
| R1 | Graphical dashboard | Open the dashboard; see readable resource metrics and navigate views without errors. | BB01 exercises rendered Streamlit UI. Browser appearance remains a manual check. |
| R2 | Real-time information | While active, subsequent samples update displayed data; pause keeps the last reading; resume updates again. | BB15 verifies updates on explicit AppTest reruns with controlled inputs. M01 must verify browser timer scheduling and live OS sampling. |
| R3 | Process states | Process table shows PID, name and the state provided by the OS; transitions and exits appear on later readings. | BB02 checks displayed state; BB07 checks empty input. M02/M05 cover actual transitions. |
| R4 | CPU usage | Show system and per-process CPU; handle initial unavailable readings and multicore values above 100%. | BB01/02/06 check displayed values. M03 checks measurement accuracy against a native OS tool. |
| R5 | Memory consumption | Show system memory and per-process percent and resident memory with clear units. | BB01/02 check percent and MiB conversion. M04 checks live accuracy. |
| R6 | Administrators can manage processes efficiently | Select a target, request a management action, see the outcome, and observe actual OS state changes. | BB12/13/14 check confirmation/dispatch and visible denial. Existing lifecycle test and M05 cover actual OS effects. |
| R7 | Identify potential issues promptly | Show pressure/state warnings on a fresh sample and identify a process to investigate where appropriate. | BB08/09/10/11 verify warning boundaries, visibility and advice. M06 measures live detection delay. |

The assignment does not specify numeric thresholds, a fixed refresh deadline, exact management actions, remote administration, authentication, ML or a black box test section. The report's 2-second default, 90% CPU/85% memory warnings, suspend/resume/terminate workflow, confirmation rules, search/filter thresholds and local-account restriction are application-level commitments. Tests below verify those commitments without treating them as extra faculty requirements. Clarify with faculty if managing processes owned by other accounts is expected: this application explicitly blocks that even when launched by an elevated account.

### 3. General guideline compliance

| Requirement | Finding | Remaining action |
| --- | --- | --- |
| One integrated group project; at most 3 members on different modules | Three integrated modules are described. Member assignments are placeholders. | Fill actual names, registration numbers and responsibilities; do not invent members. |
| Report sections 1-8 | Overview, module breakdown, functionalities, technology, flow diagram, GitHub tracking, conclusion/future scope and references are present. | Keep these sections when exporting the final report. |
| Appendix A: detailed AI elaboration/breakdown | Goals, modules, examples, technologies and execution plan are present. | Team should review the explanation against its own work. |
| Appendix B: assigned problem statement | Correct Project 13 title and description are present. | Retain the exact assigned statement. |
| Appendix C: complete solution/code | Generated report contains the current source appendix. | Rebuild after changes; verify appendix and code agree. |
| GitHub repository and at least 7 revisions with clear messages | Repository and commit table remain placeholders; no `.git` directory exists in the supplied project folder. Numbered documentation does not establish commits. | Supply the actual repository URL, 7 or more genuine revisions and dated evidence. |
| Feature branches; merge to main after testing | Not verifiable from this archive. | Provide real branches/merge history and test evidence. |
| Individual online UMS upload before deadline | Cannot be established from project files. No exact deadline appears in the PDF. | Each student uploads the complete integrated report by the faculty's actual deadline. |
| Presentation and viva | Preparation required; not verifiable from source. | Explain the implementation, challenges and test evidence. Evaluation is 15 marks AI evaluation plus 15 presentation/viva. |
| Student-written implementation; no copied peer/internet/AI code | Authorship cannot be certified by functional tests or an archive. The PDF explicitly permits AI explanation in Appendix A while requiring students to write their implementation. | Retain truthful attribution and be able to explain personal contributions. |

No marks or unconditional compliance certificate can be inferred from passing automated tests.

### 4. Black box test design

Test oracle: the assignment's required behavior plus the report's stated user-facing behavior. Techniques: equivalence partitioning (valid/invalid search and confirmations), boundary value analysis (usage thresholds), state transitions (setup, pause, resume, review, cancel, confirm), and decision combinations (warnings across views).

`tests/test_black_box_requirements.py` drives the real dashboard through public Streamlit AppTest widgets and checks displayed metrics, tables and messages. It does not call application helper functions. OS collection and process-action adapters are substituted with controlled inputs so cases are repeatable and no existing user process receives signals. This is interface-level acceptance testing with substituted dependencies, not a fully live end-to-end black box run. The existing backend/unit tests are supporting evidence and are not relabeled as black box tests.

Preconditions: install `requirements.txt`; use session-only history; standard fixtures provide PID 300 (Alpha-worker: 19.9% CPU, 4.9% memory, 1 MiB RSS), PID 301 (Beta-worker: 20% CPU, 5% memory, 2 MiB RSS), and PID 302 (Gamma-worker: 145% CPU, 6% memory, 3 MiB RSS). Baseline system CPU is 20%, RAM is 30%.

| Case | Requirements | Inputs / user steps | Expected observable result |
| --- | --- | --- | --- |
| BB01 | R1, R4, R5 | Complete the welcome guide with session-only history; open all 4 views. | CPU 20.0%, RAM 30.0%, default interval 2 seconds; controls off; no UI exception. |
| BB02 | R3, R4, R5 | Supply a stopped Alpha-worker; open Processes. | PID/name/state preserved; 19.9% CPU, 4.9% memory and 1 MiB RSS; Gamma's 145% CPU preserved. |
| BB03 | R1 (report extension) | Search `ALPHA`, `301`, then `no-such-process`. | Case-insensitive name match returns 300; PID match returns 301; no-match message without crash. |
| BB04 | R4, R5 (report extension) | Apply high CPU and high memory filters. | Exclude 19.9%/4.9%; include exact 20%/5% boundaries and higher values. |
| BB05 | R1 (report extension) | Sort by CPU, Memory, Name, PID. | Usage sorts descending; name/PID ascending with correct row identity. |
| BB06 | R4 | Supply unavailable system/process CPU and unavailable disk I/O. | System says Warming up; process CPU and I/O remain missing, not invented zero readings; no crash. |
| BB07 | R1, R3 | Supply zero visible processes. | Process count 0; explicit empty-result message; no selectable process or crash. |
| BB08 | R7 | Supply CPU 89.9%, 90.0%, 90.1% independently. | No pressure warning below 90%; warning and High status at/above 90%. |
| BB09 | R7 | Supply RAM 84.9%, 85.0%, 85.1% independently. | No pressure warning below 85%; warning and High status at/above 85%. |
| BB10 | R7 | Supply CPU 90% and one zombie; open all views. | Pressure warning and count of one zombie on every view. |
| BB11 | R7 | Supply CPU 95%, RAM 87%; open Analysis. | Advice names Gamma-worker PID 302 as largest CPU/memory consumer; no automatic process action. |
| BB12 | R6 | For each of Suspend, Resume, Terminate: enable, select 300, review, type 300, confirm, rerun. | No request before confirmation; exactly one matching request after confirmation; visible result; rerun does not duplicate request. |
| BB13 | R6 | Review Terminate; submit blank, 301, abc, -1; then Cancel. | Every invalid confirmation shows mismatch; no request; Cancel removes confirmation. |
| BB14 | R6 | Confirm a request whose OS adapter reports access denied. | Visible denial reason and no UI exception. This does not prove real OS permission enforcement. |
| BB15 | R2 | Set 1-second interval and apply; supply 42% CPU, wait >1 second and rerun; pause; supply 55%, wait/rerun; resume. | 42% appears after refresh; remains 42% while paused with Paused indicator; resume displays 55%. |

The fixed-target, disable-controls, PID reuse, protected-process and ownership cases already in `test_dashboard.py` and `test_process_control.py` supplement this matrix. Their action mocks prove dispatch/protection logic under test inputs, not actual process execution effects.

### 5. Live machine acceptance cases (not yet executed)

Use only a disposable worker created for the test. Record OS, account, Python/package versions, observed result, screenshot/log and time for each case. Keep pending cases marked NOT RUN until evidence exists.

| Case | Steps and test input | Expected result / acceptance criterion | Status |
| --- | --- | --- | --- |
| M01 - Browser refresh | Start the dashboard normally, default 2-second interval. Observe timestamps through at least 3 updates without clicking. Pause, wait 2 intervals, resume. Repeat at 1 and 60 seconds using Apply settings. | Timestamps/data update automatically while active, remain fixed while paused, resume afterward. Record actual cadence; no hard deadline was set by faculty. | NOT RUN |
| M02 - Real process identity | Launch a temporary sleeping worker and record its PID. Search it and compare with Activity Monitor/Task Manager/ps. Allow at least two samples. | Correct PID, name and OS state. After exit it disappears on a subsequent sample without crash. State names can differ between platforms. | NOT RUN |
| M03 - Live CPU | Observe idle worker, then run a disposable CPU workload on one core. Compare similar sample windows with a native monitor. | CPU rises/falls with workload; account for per-process one-core=100% versus system-wide scaling. Record tolerance before comparison; suggested approximate tolerance is 10 percentage points for matched windows, not a faculty requirement. | NOT RUN |
| M04 - Live memory | Observe a disposable worker before/after allocating a bounded buffer, for example 32 MiB if available. Compare RSS with native monitor. | Reported resident memory increases and has correct units. Record values; allocators/OS accounting need not equal buffer size exactly. | NOT RUN |
| M05 - Actual management | Select only the temporary worker; confirm Suspend, verify stopped state independently; confirm Resume, verify it runs; confirm Terminate, verify actual exit. | Correct process receives each action. A Request sent message alone is insufficient proof of exit. Record the PID and each OS observation. | NOT RUN |
| M06 - Prompt issue detection | Observe a safe, naturally occurring threshold breach or use a controlled demonstration environment; record sample time and displayed warning time. Let pressure clear. | Warning appears on the first displayed sample satisfying 90% CPU/85% RAM; clears on a later below-threshold sample. Do not fill host RAM merely to trigger an alert. | NOT RUN |
| M07 - Exit during confirmation | Review an action for the temporary worker; end it externally before confirmation; then confirm. | Clear exited/stale target failure, no other process affected, dashboard remains usable. | NOT RUN |
| M08 - Downloads and persistence | Download filtered process CSV, history CSV, diagnostics JSON, action log; open/parse each. Separately choose local history, collect, restart with local history. | Files contain the displayed scope and correct values; saved history survives restart. Session-only choice leaves prior saved files unchanged. | NOT RUN |
| M09 - Platform and permissions | Repeat M01-M05 on every claimed deployment OS. On a suitable test machine attempt a denied/protected target through the normal UI. | Supported operations work with current account permissions; denied requests show clear failure; no elevation or unintended target action. | NOT RUN |
| M10 - Visual usability | Open in the intended browser at desktop and small window sizes; try light mode, sidebar and all views. | Labels, controls and confirmation text remain readable and reachable; no overlap/clipping. AppTest is not pixel-level browser verification. | NOT RUN |

### 6. Reproduce and record results

From the project directory:

```sh
python -m unittest discover -s tests -p test_black_box_requirements.py -v
python -m unittest discover -s tests -v
python tools/build_project_report.py
```

The execution record and exact resolved packages for this review are saved under `docs/verification/`. Earlier claims in the alignment document dated 13 November describe a different environment and must not be treated as today's results.

#### Actual results: 15 November 2026

Environment: macOS 26.6.2 arm64, Python 3.13.3. Dependencies were installed from the supplied `requirements.txt` into an isolated temporary environment. Resolved versions are preserved in [the package record](docs/verification/2026-11-15-packages.txt); the earlier `requirements-tested.txt` was preserved.

| Run | Actual outcome | Evidence |
| --- | --- | --- |
| BB01-BB15, including threshold and action subcases | All 15 test methods passed; no acceptance failure found in the exercised controlled-input behavior. | [Full test log](docs/verification/2026-11-15-unittest.log), methods prefixed `test_BB`. |
| Full suite under sandbox | 51 tests discovered: 50 passed, 1 skipped, 0 failures/errors; 9.954 seconds. Skip reason: OS process inspection was denied by the sandbox. | [Full test log](docs/verification/2026-11-15-unittest.log). |
| Process-control suite outside sandbox | 7 of 7 passed, including actual suspend, observed stopped state, resume, and terminate of the child created by the lifecycle test. No existing user program was targeted. | [Local process-control log](docs/verification/2026-11-15-process-control-local.log). |

The successful local lifecycle run resolves the sandbox skip for that backend test on this macOS machine. It does not complete M05's browser-to-OS interaction demonstration. M01-M10 remain pending manual acceptance; none is labeled passed. Windows/Linux remain untested.

The log contains Streamlit warnings about `use_container_width` deprecation and bare-mode script context. These did not fail the test run; future library compatibility and browser layout are separate from these acceptance results. No production application behavior was changed during this review.

### 7. Submission actions

1. Complete actual team, section, faculty, date and repository details in `docs/report-body.md`.
2. Replace all seven commit placeholders with genuine GitHub revision and tested-merge evidence.
3. Complete the live acceptance cases above and attach actual observations/screenshots. Do not mark planned tests as passed.
4. Rebuild `PROJECT_REPORT.md`, including its complete current code appendix, and inspect the final export.
5. Submit individually on UMS by the actual announced deadline and prepare to explain the required monitoring/management workflow in the viva.
