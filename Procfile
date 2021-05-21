web: gunicorn terminal.wsgi --log-file -
worker: celery -A terminal worker --beat -S django --l info