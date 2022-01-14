from time import sleep
from multiprocessing.connection import Listener, Client
from gpiozero import Servo, OutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
from config.doorlock import ipc_address, ipc_key, servo_pin, on_startup, servo_lock_position, servo_unlock_position, servo_power_control_pin


def lock():
    with Client(ipc_address, authkey=ipc_key) as conn:
        conn.send('lock')


def unlock():
    with Client(ipc_address, authkey=ipc_key) as conn:
        conn.send('unlock')


if __name__ == '__main__':
    servo = Servo(servo_pin, pin_factory=PiGPIOFactory(), initial_value=None)
    servo_mapping = {
        'lock': servo_lock_position,
        'unlock': servo_unlock_position,
    }

    def move_servo(command):
        if command not in servo_mapping:
            return

        if servo_power_control_pin is not None:
            with OutputDevice(servo_power_control_pin) as servo_switch:
                servo_switch.on()
                getattr(servo, servo_mapping[command])()
                sleep(1)
                servo_switch.off()
        else:
            getattr(servo, servo_mapping[command])()
            sleep(1)
            servo.detach()

    move_servo(on_startup)

    with Listener(ipc_address, authkey=ipc_key) as ipc_listener:
        while True:
            with ipc_listener.accept() as conn:
                move_servo(conn.recv())
