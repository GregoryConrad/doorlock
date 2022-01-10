import threading
from gpiozero import Servo, Button

servo_pin = 17
lock_pin = 5
unlock_pin = 13

servo = Servo(servo_pin)
monitor_thread_lock = threading.Lock()


def lock():
    servo.max()


def unlock():
    servo.min()


class MonitorThread(threading.Thread):
    def __init__(self, function, pin):
        threading.Thread.__init__(self)
        self.function = function
        self.pin = pin

    def run(self):
        btn = Button(self.pin)
        while True:
            btn.wait_for_active()
            btn.wait_for_inactive()
            monitor_thread_lock.acquire()
            function()
            monitor_thread_lock.release()


if __name__ == '__main__':
    lock_monitor = MonitorThread(lock, lock_pin)
    unlock_monitor = MonitorThread(unlock, unlock_pin)
    lock_monitor.start()
    unlock_monitor.start()
