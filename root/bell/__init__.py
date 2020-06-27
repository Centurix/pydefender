from .solenoid import Solenoid
from time import sleep
from micropython import const

"""
Bell control
============

Constant below controls the pin this is connected to

Use the methods for the effect. The base bell.ding() does a single ding.

"""
PIN = const(2)


bell = Solenoid(PIN)


def ding_ding(delay=0.25):
    bell.ding()
    sleep(delay)
    bell.ding()


def telephone(delay=0.25):
    for count in range(0, 10):
        bell.ding()
        sleep(0.025)

    sleep(delay)

    for count in range(0, 10):
        bell.ding()
        sleep(0.025)


def shave_and_a_haircut(speed=1):
    bell.ding()
    sleep(0.5 * speed)
    bell.ding()
    sleep(0.25 * speed)
    bell.ding()
    sleep(0.25 * speed)
    bell.ding()
    sleep(0.5 * speed)
    bell.ding()
    sleep(1 * speed)
    bell.ding()
    sleep(0.5 * speed)
    bell.ding()


def football(speed=1):
    bell.ding()
    sleep(1 * speed)
    bell.ding()
    sleep(1 * speed)
    bell.ding()
    sleep(.5 * speed)
    bell.ding()
    sleep(.5 * speed)
    bell.ding()
    sleep(1 * speed)
    bell.ding()
    sleep(.5 * speed)
    bell.ding()
    sleep(.5 * speed)
    bell.ding()
    sleep(.5 * speed)
    bell.ding()
    sleep(1 * speed)
    bell.ding()
    sleep(.5 * speed)
    bell.ding()

__all__ = [
    "bell",
    "ding_ding",
    "telephone"
]
