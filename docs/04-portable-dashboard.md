# 04 — A more versatile dashboard

The dashboard now groups system charts, process monitoring and analysis into separate tabs. It adds history windows, CPU and memory filters, sorting, and CSV downloads. The sidebar identifies the operating system and provides refresh controls. Errors reading processes or the local database are reported instead of fabricating metrics.

The README includes a Windows PowerShell setup that invokes the virtual environment directly, avoiding activation-policy changes. The project relies on cross-platform Python and psutil APIs, but actual Windows execution still needs verification on a Windows machine; available process information depends on permissions.
