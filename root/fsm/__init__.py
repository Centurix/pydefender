from .fsm import FSM


__all__ = [
    "FSM"
]

"""
Finite State Machine for Micropython

Usage
=====

In the example below, it defines a simple Moore machine with a dictionary
of states (STATE_A, STATE_B) defining events (EVENT_A, EVENT_B) that 
transition between each one with a backup "else" in case the event isn't
recognised.

The three elements of each state transmission are:
* enter
* loop
* exit

These entries are Python callables and the calls receive the instance
of the FSM itself.

"loop" will just keep looping again and again during the state.

There are two types of timers available:
* Periodic timer
* One-off timer

machine.periodic_timer(seconds, callback)
machine.one_off_timer(seconds, callback)

Where callback is a Python callable

Here's a working example of the FSM
===================================

# These three functions are for State A
def state_a_enter(machine):
    print("Entering state A")
    
def state_a_loop(machine):
    print("State A loop")
    machine.trigger("EVENT_B")
    
def state_a_exit(machine):
    print("Exiting state A")
    
# This function is for State B
def state_b_loop(machine):
    print("State B loop")
    machine.trigger("EVENT_A")

# Create the FSM
machine = FSM({
    "STATE_A": {
        "events": {
            "EVENT_B": "STATE_B",
            "else": "STATE_A"
        },
        "enter": state_a_enter,
        "loop": state_a_loop,
        "exit": state_a_exit
    },
    "STATE_B": {
        "events": {
            "EVENT_A": "STATE_A",
            "else": "STATE_B"
        },
        "loop": state_b_loop
    }
})
# Start the machine in State A
machine.begin("STATE_A")

# The machine runs in the background, so we loop forever
while True:
    pass

"""