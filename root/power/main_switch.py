from micropython import const
from machine import (
    Pin,
    disable_irq,
    enable_irq,
    Timer
)


DEBOUNCE_TIME = const(100)  # 100 milliseconds


class MainSwitch:
    def __init__(self, pin, on_callback=None, off_callback=None):
        self._pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self._pin.irq(
            trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,
            handler=self._power_state_change_callback
        )
        self._current_state = self._pin.value()
        self._power_on_callback = on_callback
        self._power_off_callback = off_callback
        self._debounce_timer = None
        self._debounce = False

    def state(self):
        return self.is_on()

    def is_on(self):
        return self._pin.value()

    def is_off(self):
        return not self._pin.value()

    def _remove_debounce(self, test):
        self._debounce = False

    def _power_state_change_callback(self, pin):
        if self._debounce:
            return

        self._debounce = True
        self._debounce_timer = Timer(-1)
        self._debounce_timer.init(
            period=DEBOUNCE_TIME,
            mode=Timer.ONE_SHOT,
            callback=self._remove_debounce
        )

        irq_state = disable_irq()
        value = pin.value()

        if not self._current_state and value:
            if self._power_off_callback is not None:
                self._power_off_callback(pin)
        elif self._current_state and not value:
            if self._power_on_callback is not None:
                self._power_on_callback(pin)

        self._current_state = value
        # Clear the interrupt queue?
        enable_irq(irq_state)

    def on_power_on(self, callback):
        self._power_on_callback = callback

    def on_power_off(self, callback):
        self._power_off_callback = callback
