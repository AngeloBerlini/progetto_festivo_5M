"""Root run.py to expose the Flask app as `app` for gunicorn.

Render's start command uses `gunicorn run:app`, which expects a top-level
module named `run` with an `app` WSGI callable. This file imports the
app from `tuttocampo.run` so that command works without changing Render.
"""

from tuttocampo.run import app

if __name__ == '__main__':
    # Local development fallback
    app.run(debug=True)
