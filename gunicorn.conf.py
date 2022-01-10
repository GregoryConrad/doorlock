# See https://docs.gunicorn.org/en/stable/settings.html#settings

import multiprocessing
from doorlock_config import config as doorlock_config


bind = f"0.0.0.0:{doorlock_config['serverPort']}"
workers = multiprocessing.cpu_count() * 2 + 1
certfile = doorlock_config['certfile']
keyfile = doorlock_config['keyfile']
