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
