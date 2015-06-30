from threading import Thread
from DriverController import *
from time import sleep

COMMANDS = ("BUTTON_PRESS", "SLIDER_MOVE")

joystick = Joystick(1)

class Command:

    def __init__(self, command, control_id, button_state, control_position):
        self.command = command
        self.control_id = control_id
        self.button_state = button_state
        self.control_position = control_position


class CommandHandler(Thread):

    commands = []

    def add_command(self, command, control_id, button_state, control_position):
        self.commands.append(Command(command, control_id, button_state, control_position))

    def run(self):
        while True:
            if len(self.commands) > 0:
                command = self.commands.pop(0)
                if COMMANDS[command.command] == "BUTTON_PRESS":
                    joystick.set_button_pressed(command.control_id, command.button_state)
                elif COMMANDS[command.command] == "SLIDER_MOVE":
                    joystick.set_slider_position(command.control_id, command.control_position)
            sleep(0.02)