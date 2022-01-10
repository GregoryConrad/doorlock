from multiprocessing.connection import Listener, Client
from gpiozero import Servo, Button
from doorlock_config import config

servo_pin = config['pins']['servo']
lock_pin = config['pins']['lockButon']
unlock_pin = config['pins']['unlockButton']
ipc_address = ('localhost', config['ipcPort'])
on_startup = config['onStartup']
servo_mapping = config['servoMapping']


def lock():
    with Client(ipc_address) as conn:
        conn.send('lock')


def unlock():
    with Client(ipc_address) as conn:
        conn.send('unlock')


if __name__ == '__main__':
    servo = Servo(servo_pin)
    lock_btn = Button(lock_pin)
    lock_btn.when_released = lock
    unlock_btn = Button(unlock_pin)
    unlock_btn.when_released = unlock

    def move_servo(command):
        getattr(servo, servo_mapping[command])()

    move_servo(on_startup)

    with Listener(ipc_address) as ipc_listener:
        while True:
            with ipc_listener.accept() as conn:
                move_servo(conn.recv())
