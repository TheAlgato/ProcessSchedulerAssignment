# 01 — Monitor real processes

The collector reads local process and system information using psutil and stores snapshots in SQLite. CPU measurements use two observations; new processes have no CPU baseline. Disk I/O counters may be unavailable, and inaccessible processes are skipped. No processes or system settings are changed.

Verification: run `os/bin/python app.py --interval 1 --samples 2` on macOS or Linux, or use the corresponding Python executable in the `os` environment on Windows. Inspect the resulting SQLite database with a SQLite viewer. Process access can depend on operating system permissions.
