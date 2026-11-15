# 06 — Introducing Mira

Mira gives the performance analyzer a new visual identity: a soft, light dashboard with clear metric cards, a live indicator, and subtle motion. Motion respects the operating system's reduced-motion preference. The design uses locally available system fonts and works without downloading visual assets.

The Overview adds a memory utilization ring and a chart of the seven visible processes with the highest CPU use, alongside the existing historical resource chart. AI insights compares current usage with the five-minute estimate when sufficient history exists. All charts use actual measurements or clearly labelled estimates; no example data is substituted for missing readings.

The guided consent flow, optional local history, process filters, CSV downloads and stop control remain available. A process can use more than 100% CPU across multiple cores, and process visibility and disk I/O vary with operating system permissions.

Database connections now close after each operation, preventing them from accumulating during live refreshes.
