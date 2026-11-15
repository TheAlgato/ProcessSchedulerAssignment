# 05 — Guided setup and dashboard permissions

The macOS and Windows launchers run an interactive setup. They ask before creating the local virtual environment, installing missing Python packages, and starting the dashboard. Python itself must already be installed. Virtual environments are specific to the operating system and should be recreated on a different computer.

Each new browser session starts with a short guide. The user must choose to allow process monitoring and then choose either local SQLite history or session-only system history. No process collection or database creation happens before those choices. The choice is application-level consent and does not grant operating-system permissions. The sidebar can stop monitoring and restart the guide. Existing saved history is not erased by choosing session-only mode.

The app uses the project directory for the database and drive selection even when launched from elsewhere. On Windows and macOS, actual accessible process details depend on OS permissions. Setup and monitoring must still be verified on a Windows machine.
