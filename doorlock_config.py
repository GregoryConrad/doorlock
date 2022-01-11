import os
import json

config = {}
config_filename = "doorlock.json"


def get_file(filename):
    return os.path.join(os.getcwd(), filename)


def refresh_config():
    global config
    with open(get_file(config_filename), 'r') as config_file:
        for key, value in json.load(config_file).items():
            config[key] = value


def update_config(new_config):
    with open(get_file(config_filename), 'w') as config_file:
        json.dump(new_config, config_file, indent=4)
    refresh_config()


refresh_config()
