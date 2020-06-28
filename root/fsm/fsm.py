import _thread
try:
    from machine import Timer
except ImportError:
    from .unix_timer import UnixTimer as Timer

from time import sleep
from ucollections import deque


class FSM:
    """
    Finite State Machine for MicroPython

    Could we replace the queue with the threading queue?

    State A -> State B

    states dictionary format

    {
        "STATE_A": {
            "events": {
                "EVENT_A": "STATE_A",
                "EVENT_B": "STATE_B",
                "EVENT_C": "STATE_C",
                "else": "STATE_A"
            },
            "exit": callable,
            "enter": callable,
            "loop": callable
        }
    }
    """
    def __init__(self, states):
        self._state_table = states
        self._current_state = None
        self._queue = deque((), 100)
        self._queue_lock = _thread.allocate_lock()
        self._timer = None
        self._thread = None
        self._timer_callback = None

    def trigger(self, event):
        """
        Trigger an event.
        Place the event into the queue
        """
        self._queue_lock.acquire()
        self._queue.append(event)
        self._queue_lock.release()

    def timer_callback(self, argument1=1, argument2=2):
        if self._timer_callback is not None:
            self._timer_callback(self)

    def periodic_timer(self, seconds, callback):
        self._timer_callback = callback
        self._timer = Timer(-1)  # RTOS Timer
        self._timer.init(
            period=seconds * 1000,
            mode=Timer.PERIODIC,
            callback=self.timer_callback
        )
        return self._timer

    def one_off_timer(self, seconds, callback):
        self._timer_callback = callback
        self._timer = Timer(-1)  # RTOS Timer
        self._timer.init(
            period=seconds * 1000,
            mode=Timer.ONE_SHOT,
            callback=self.timer_callback
        )
        return self._timer

    def begin(self, start_state):
        """
        Start the state machine thread
        :return:
        """
        self._current_state = start_state
        self._thread = _thread.start_new_thread(self._process_queue_items, ())

    def _process_queue_items(self):
        """
        We are in current_state, look for event and change to that state
        if the event does not exist, change to else
        :return:
        """
        while True:
            try:
                self._queue_lock.acquire()
                event = self._queue.popleft()  # Get an event
                events = self._state_table[self._current_state].get("events", dict())
                new_state = events.get(event, events.get("else", self._current_state))
                if self._current_state != new_state:
                    # State phase change, trigger exit and enter
                    exit_phase = self._state_table[self._current_state].get("exit")
                    if exit_phase is not None:
                        exit_phase(self)
                    enter_phase = self._state_table[new_state].get("enter")
                    if enter_phase is not None:
                        enter_phase(self)
                    self._current_state = new_state
            except IndexError:  # Nothing to do
                pass
            except Exception as ex:
                print("Exception {}".format(ex))
            finally:
                self._queue_lock.release()
                # Find the current state loop and iterate
                loop = self._state_table[self._current_state].get("loop")
                if loop is not None:
                    loop(self)
                sleep(0)
