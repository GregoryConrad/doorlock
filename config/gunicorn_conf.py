# DO NOT EDIT THIS FILE UNLESS YOU KNOW WHAT YOU ARE DOING
# See https://docs.gunicorn.org/en/stable/settings.html#settings

import multiprocessing
import config.doorlock as doorlock

bind = f"0.0.0.0:{doorlock.server_port}"
workers = multiprocessing.cpu_count() * 2 + 1
certfile = doorlock.certfile
keyfile = doorlock.keyfile
