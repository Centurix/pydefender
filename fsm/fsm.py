from threading import (
    Thread,
    Timer,
    Lock
)
from time import sleep
from collections import deque


class FSM:
    """
    Finite State Machine for MicroPython

    Could we replace the queue with the threading queue?

    State A -> State B
    """
    def __init__(self, states):
        self._state_table = states
        self._current_state = None
        self._queue = deque()
        self._queue_lock = Lock()
        self._timer = None

    def trigger(self, event):
        """
        Trigger an event.
        Place the event into the queue
        """
        self._queue_lock.acquire(blocking=True)
        self._queue.append(event)
        self._queue_lock.release()

    def timer(self, seconds, callback):
        self._timer = Timer(seconds, callback, args=[self])
        self._timer.start()
        return self._timer

    def begin(self, start_state):
        """
        Start the state machine thread
        :return:
        """
        self._current_state = start_state
        thread = Thread(target=self._process_queue_items)
        thread.start()

    def _process_queue_items(self):
        """
        We are in current_state, look for event and change to that state
        if the event does not exist, change to else
        :return:
        """
        while True:
            try:
                self._queue_lock.acquire(blocking=True)
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
            finally:
                self._queue_lock.release()
                # Find the current state loop and iterate
                loop = self._state_table[self._current_state].get("loop")
                if loop is not None:
                    loop(self)
                sleep(0)
