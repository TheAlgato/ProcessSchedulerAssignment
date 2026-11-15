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
