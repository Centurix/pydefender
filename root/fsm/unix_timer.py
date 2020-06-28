import _thread
from time import sleep


class UnixTimer:
    """
    Emulate a timer for the Unix port
    """
    ONE_SHOT = 1
    PERIODIC = 2

    def __init__(self, id=-1):
        self._id = id
        self._timer_thread = None
        self._callback = None

    def _one_off(self):
        sleep(self._period // 1000)
        self._callback(self)

    def _periodic(self):
        print("Periodic timer!")
        while True:
            sleep(self._period // 1000)
            self._callback(self)

    def init(self, period, mode, callback):
        self._callback = callback
        self._period = period

        if mode == UnixTimer.ONE_SHOT:
            self._timer_thread = _thread.start_new_thread(
                self._one_off,
                ()
            )
        else:
            self._timer_thread = _thread.start_new_thread(
                self._periodic,
                ()
            )
