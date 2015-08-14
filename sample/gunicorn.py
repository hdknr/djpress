import os
import sys

# for Gunicorn to find app.wsgi:application
DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
# logs
LOGS = os.path.join(DIR, 'logs')
if not os.path.isdir(LOGS):
        os.makedirs(LOGS)

# Gunicorn Configuration
accesslog = os.path.join(LOGS, "gunicorn.access.log")
errorlog = os.path.join(LOGS, "gunicorn.error.log")
pidfile = os.path.join(LOGS, "gunicorn.pid")
bind = "unix:" + os.path.join(LOGS, "gunicorn.sock")
