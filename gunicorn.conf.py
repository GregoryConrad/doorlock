# See https://docs.gunicorn.org/en/stable/settings.html#settings

import multiprocessing
from doorlock_config import config


bind = f"0.0.0.0:{config['serverPort']}"
workers = multiprocessing.cpu_count() * 2 + 1
certfile = config['certfile']
keyfile = config['keyfile']
