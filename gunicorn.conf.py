# See https://docs.gunicorn.org/en/stable/settings.html#settings

import os
import pathlib
import multiprocessing


def get_file(filename):
    return os.path.join(pathlib.Path(__file__).parent, filename)


bind = "0.0.0.0:39420"
workers = multiprocessing.cpu_count() * 2 + 1
certfile = get_file("server.crt")
keyfile = get_file("server.key")
