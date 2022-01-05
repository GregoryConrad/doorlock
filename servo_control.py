import sys
from gpiozero import Servo, Button

servo_pin = None  # TODO
lock_pin = None  # TODO
unlock_pin = None  # TODO

servo = Servo(servo_pin)

def lock():
    servo.max()


def unlock():
    servo.min()


def _generic_monitor(pin, function):
    btn = Button(pin)
    while True:
        btn.wait_for_active()
        btn.wait_for_inactive()
        function()


def lock_monitor():
    _generic_monitor(lock_pin, lock)


def unlock_monitor():
    _generic_monitor(unlock_pin, unlock)


if __name__ == '__main__':
    globals()[sys.argv[1]]()