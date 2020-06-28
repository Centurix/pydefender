from fsm import FSM


def state_a_enter(machine):
    print("State A enter")


def state_a_loop(machine):
    machine.trigger("EVENT_B")
    # print("State A loop")


def state_a_exit(machine):
    print("State A exit")


def state_b_enter(machine):
    print("State B enter")


def state_b_loop(machine):
    machine.trigger("EVENT_C")
    # print("State B loop")


def state_b_exit(machine):
    print("State B exit")


def state_c_enter(machine):
    print("State C enter")


def state_c_loop(machine):
    machine.trigger("EVENT_A")
    # print("State C loop")


def state_c_exit(machine):
    print("State C exit")


def state_d_enter(machine):
    print("State D enter")


def state_d_loop(machine):
    print("==================================State D loop")


def state_d_exit(machine):
    print("State D exit")


def timer_callback(machine):
    print("Triggering STATE_D")
    machine.trigger("EVENT_D")


if __name__ == "__main__":
    machine = FSM({
        "STATE_A": {
            "events": {
                "EVENT_B": "STATE_B",
                "EVENT_D": "STATE_D",
                "else": "STATE_A"
            },
            "loop": state_a_loop
        },
        "STATE_B": {
            "events": {
                "EVENT_C": "STATE_C",
                "EVENT_D": "STATE_D",
                "else": "STATE_A"
            },
            "loop": state_b_loop
        },
        "STATE_C": {
            "events": {
                "EVENT_A": "STATE_A",
                "EVENT_D": "STATE_D",
                "else": "STATE_A"
            },
            "loop": state_c_loop
        },
        "STATE_D": {
            "events": {
                "EVENT_A": "STATE_A",
                "EVENT_B": "STATE_B",
                "EVENT_C": "STATE_C",
            },
            "loop": state_d_loop
        }
    })
    machine.begin("STATE_A")
    machine.periodic_timer(1, timer_callback)

    while True:
        pass
