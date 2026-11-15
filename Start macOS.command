#!/bin/bash
cd "$(dirname "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3.10 or newer is required. Install Python from https://www.python.org/downloads/ and try again."
  read -r -p "Press Enter to close."
  exit 1
fi
python3 setup.py
read -r -p "Press Enter to close."
