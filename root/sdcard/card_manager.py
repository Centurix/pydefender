import uos
from micropython import const
from .helpers import Helpers
from machine import (
    SDCard,
    Pin,
    disable_irq,
    enable_irq,
    Timer
)

SLOT = const(2)
PIN_MOSI = const(23)
PIN_MISO = const(19)
PIN_SCK = const(18)
PIN_CS = const(5)
PIN_CD = const(4)
DEBOUNCE_TIME = const(100)  # 100 milliseconds


class CardManager:
    """
    High level auto-mounting SD Card manager
    """
    def __init__(self, directory="/sd"):
        self._card = None
        self._directory = directory

        if Helpers.exists(self._directory) and \
                not Helpers.is_dir(self._directory):
            raise Exception("Cannot mount {}".format(self._directory))

        if not Helpers.exists(self._directory):
            uos.mkdir(self._directory)

        # Setup and IRQ on the CD line to auto-mount/dismount the sdcard
        pin = Pin(PIN_CD, Pin.IN, Pin.PULL_UP)
        pin.irq(
            trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,
            handler=self._card_state_change
        )
        # These are for debouncing the card detect signal
        self._debounce_timer = None
        self._debounce = False

        self._card_state_change(pin)

    def is_card_present(self):
        return bool(self._card is not None)

    def _remove_debounce(self, test):
        self._debounce = False

    def _init_card(self):
        try:
            if self._card is None:
                self._card = SDCard(
                    slot=SLOT,
                    mosi=PIN_MOSI,
                    miso=PIN_MISO,
                    sck=PIN_SCK,
                    cs=PIN_CS
                )
        except Exception:
            raise Exception("Card reader not present")

        return self._card

    def _deinit_card(self):
        self._card.deinit()
        self._card = None

    def _card_state_change(self, pin):
        """
        Need to debounce this
        :param pin:
        :return:
        """
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

        if pin.value():  # No card present
            if self._card:  # Card may not be present on boot
                enable_irq(irq_state)
                uos.umount(self._directory)
                irq_state = disable_irq()
                self._deinit_card()
        else:
            try:
                card = self._init_card()
                enable_irq(irq_state)
                uos.mount(card, self._directory)
                irq_state = disable_irq()
            except OSError:  # Mount issue, probably EPERM
                pass

        enable_irq(irq_state)
