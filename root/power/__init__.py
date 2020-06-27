from micropython import const
from .relay_array import RelayArray
from .main_switch import MainSwitch

"""
Provide support for the relay array board for powering
everything. Also provide power control for the Raspberry PI
itself by instructing it to power down safely.

Also includes the detection for the main switch throw. This will
fire an event back when the switch changes state.

Events are like:

def power_on(pin):
    print("Powered on")

def power_off(pin):
    print("Powered off")

switch.on_power_on(power_on)  # Set the event handler for on/off
switch.on_power_off(power_off)
"""

MAIN_SWITCH_PIN = const(25)
RELAY_ARRAY_PINS = [2, 4, 5, 12]

relays = RelayArray(RELAY_ARRAY_PINS)
switch = MainSwitch(MAIN_SWITCH_PIN)


__all__ = [
    "relays",
    "switch"
]
