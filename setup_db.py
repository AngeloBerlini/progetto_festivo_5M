import runpy
import os

"""Wrapper script to run the existing tuttocampo/setup_db.py

Render's default build used `python setup_db.py` from the repo root.
This wrapper executes the script by path so the same command works.
"""

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, 'tuttocampo', 'setup_db.py')

if __name__ == '__main__':
    if not os.path.exists(SCRIPT):
        raise SystemExit(f"Could not find script at {SCRIPT}")
    # Execute the existing script as __main__ (same behaviour as `python tuttocampo/setup_db.py`)
    runpy.run_path(SCRIPT, run_name='__main__')
