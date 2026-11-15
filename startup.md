Run these commands in your macOS Terminal from your project directory:

~~~~
python3 -m venv os
~~~~~~

Activate the virtual environment:
~~~~
source os/bin/activate
~~~~~


Install your project dependencies:
~~~~
pip install -r requirements.txt
~~~~~

Verify Python is running inside the environment:
~~~~
which python
python --version
~~~~~

You should see a path ending in:
~~~~
/ProcessScope/os/bin/python
~~~~~~~~

To deactivate later:
~~~~~
deactivate
~~~~~~~~

running in the dashboard environment, run:

~~~~
source os/bin/activate
python -m streamlit run dashboard.py
~~~~~~~