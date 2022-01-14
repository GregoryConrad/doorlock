from gpiozero import Button
from config.doorlock import config
from modules.controller import lock, unlock
from time import sleep

if __name__ == "__main__":
    lock_btn = Button(config['lockPin'])
    lock_btn.when_released = lock
    unlock_btn = Button(config['unlockPin'])
    unlock_btn.when_released = unlock

    while True:
        sleep(1000000)
