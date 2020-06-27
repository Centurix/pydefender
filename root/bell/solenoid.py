from machine import Pin
from time import sleep


class Solenoid:
    def __init__(self, pin):
        self._pin = Pin(pin, Pin.OUT)

    def ding(self):
        self._pin.on()
        sleep(0.01)
        self._pin.off()
