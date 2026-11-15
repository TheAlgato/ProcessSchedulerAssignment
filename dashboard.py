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
