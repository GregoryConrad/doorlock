from gpiozero import Button
from config.doorlock import lock_button_pin, unlock_button_pin
from modules.controller import lock, unlock
from time import sleep

if __name__ == "__main__":
    lock_btn = Button(lock_button_pin)
    lock_btn.when_released = lock
    unlock_btn = Button(unlock_button_pin)
    unlock_btn.when_released = unlock

    while True:
        sleep(1000000)
