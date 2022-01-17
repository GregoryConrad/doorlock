# This is an example to base your configuration off of.
# DO NOT USE THIS FILE AS IS; IT WILL NOT WORK!!!

from pathlib import Path
from datetime import timedelta
from os import urandom
from base64 import b64encode, b64decode


def get_config_file(filename):
    return Path(__file__).parent / filename


def get_key(filename):
    # Create the key if it does not yet exist
    if not get_config_file(filename).is_file():
        with open(get_config_file(filename), 'w') as key_file:
            key_file.write(b64encode(urandom(64)).decode('utf-8'))

    # Return the key
    with open(get_config_file(filename), 'r') as key_file:
        return key_file.read()


# Controller module configuration (required)
servo_pin = 12  # self explanatory
servo_lock_position = 'max'  # min, mid, or max
servo_unlock_position = 'min'  # min, mid, or max
# Some servos even after "detached" still do not freely rotate when powered on
# This pin is to toggle a switch (like a transistor/relay) that controls power to the servo
servo_power_control_pin = None  # pin (or None for this feature to be disabled)
# What to do when the pi (specifically, the controller module) starts up
on_startup = 'unlock'  # lock, unlock, or nothing (start the servo detached)
ipc_address = ('localhost', 39421)  # you probably don't need to change
# Don't change the following unless you know what you are doing
ipc_key = b64decode(get_key('ipc_key.txt'))  # key to authenticate ipc

# Server module configuration (if you are running the web server)
authorized_emails = {
    'gregorysconrad@gmail.com',
}  # set of Google accounts that can control the lock
# Note: you need to be root or have permission to bind to ports less than 1024
# Thus, I'd recommend keeping this port as-is and just port forward to it
server_port = 39420  # port the web server runs on
certfile = "/etc/letsencrypt/live/example.com/fullchain.pem"  # certfile for HTTPS
keyfile = "/etc/letsencrypt/live/example.com/privkey.pem"  # keyfile for HTTPS
session_lifetime = timedelta(days=365)  # how long cookie sessions should last
# Don't change the following unless you know what you are doing
session_sign_key = get_key('session_sign_key.txt')  # key to sign cookies

# Manual module configuration (if you are using the manual override buttons)
lock_button_pin = 5
unlock_button_pin = 13

# NFC module configuration (if you are using an NFC reader)
# TODO
