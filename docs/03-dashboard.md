# Interactive process dashboard

Run `python setup.py` from the project directory, or use the Windows or macOS launcher. The server binds to localhost. Follow the monitoring guide and choose local or session-only history.

The dashboard refreshes every two seconds by default. Choose 1, 2, 5, 10, 30, or 60 seconds in Collection and click Apply settings. Pause collection freezes the current reading. The UTC timestamp distinguishes the latest reading from a paused display.

Overview displays CPU, memory, disk capacity, process count, history, and recommendations. Processes displays actual OS process states and resource readings, search, filters, sorting, CSV export, and an inspector. Analysis shows resource pressure, unusual profiles, recommendations, and optional forecasts. Diagnostics shows transfer rates, cores, swap, and a JSON export. High CPU, memory pressure, and zombie warnings appear across views.

To manage a process, enable process controls in the sidebar, select a process in the inspector, choose an action, and click Review action. Read the fixed target and action. Type the displayed PID and click Confirm action, or Cancel. Suspending pauses execution. Resume continues it. Terminate requests termination on POSIX and forcibly ends the process on Windows, which can lose unsaved work.

The confirmation retains the reviewed PID and creation time even while the table refreshes. The backend rechecks identity and ownership and blocks the dashboard, its ancestors, and PID 0/1. Permission failures and exited processes produce messages. Successful requests still need a later status check. Recent outcomes stay in this browser session, with a maximum of 50 entries and a CSV download.

Use one browser session for a consistent history. OS permissions can limit visibility. Unavailable metrics remain blank. This app manages processes on the server computer, so keep the localhost binding and run it on the machine you intend to monitor.
