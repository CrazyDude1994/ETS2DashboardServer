import socket
import struct
from DriverController import *


def handle_command(command, control_id, button_state, control_position):
    if COMMANDS[command] == "BUTTON_PRESS":
        joystick.set_button_pressed(control_id, button_state)
    elif COMMANDS[command] == "SLIDER_MOVE":
        joystick.set_slider_position(control_id, control_position)

HOST = ''
PORT = 8844
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

joystick = Joystick(1)

COMMANDS = ("BUTTON_PRESS", "SLIDER_MOVE")

while 1:
    conn, addr = s.accept()
    print 'Connected by', addr
    while 1:
        data = conn.recv(1)  # recv command
        data += conn.recv(4)  # recv control id
        data += conn.recv(1)  # recv button state
        data += conn.recv(4)  # recv control id
        if not data:
            break
        command, control_id, button_state, control_position = struct.unpack("!BiBi", data)
        handle_command(command, control_id, button_state, control_position)
        print(command, control_id, button_state, control_position)
    conn.close()
