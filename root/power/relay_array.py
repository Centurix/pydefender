from machine import Pin


class RelayArray:
    def __init__(self, pins):
        self._relay_pins = pins
        self._pins = list()
        for index in self._relay_pins:
            self._pins.append(Pin(index, Pin.OUT))

    def on(self, index):
        if index < len(self._relay_pins):
            self._pins[index].on()

    def off(self, index):
        if index < len(self._relay_pins):
            self._pins[index].off()

    def toggle(self, index):
        if index < len(self._relay_pins):
            if self._pins[index].value == 0:
                self._pins[index].on()
            else:
                self._pins[index].off()

    def state(self, index):
        if index < len(self._relay_pins):
            return self._pins[index].value != 0
