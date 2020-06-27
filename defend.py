#!/usr/bin/env python3
import click
from fsm import FSM


def start_loop(machine):
    click.echo("start_loop")
    machine.trigger("event_a")


def state_a_loop(machine):
    click.echo("state_a_loop")
    machine.trigger("event_b")


def state_b_loop(machine):
    click.echo("state_b_loop")
    machine.trigger("event_c")


def state_c_loop(machine):
    click.echo("state_c_loop")
    machine.trigger("event_a")


def state_d_loop(machine):
    click.echo("state_d_loop")


def state_d(machine):
    click.echo("==========================================================")
    machine.trigger("event_d")


@click.command()
def main():
    click.echo("Starting the state machine")

    machine = FSM({
        "START": {
            "loop": start_loop,
            "events": {
                "event_a": "STATE_A",
                "event_d": "STATE_D"
            }
        },
        "STATE_A": {
            "loop": state_a_loop,
            "events": {
                "event_b": "STATE_B",
                "event_d": "STATE_D"
            }
        },
        "STATE_B": {
            "loop": state_b_loop,
            "events": {
                "event_c": "STATE_C",
                "event_d": "STATE_D"
            }
        },
        "STATE_C": {
            "loop": state_c_loop,
            "events": {
                "event_a": "STATE_A",
                "event_d": "STATE_D"
            }
        },
        "STATE_D": {
            "loop": state_d_loop
        }
    })
    machine.begin("START")
    machine.timer(5, state_d)

    while True:
        pass


if __name__ == "__main__":
    main()
