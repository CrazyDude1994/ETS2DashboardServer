import random
import socket
import struct
from mmap import *
from threading import Thread
from command_handler import CommandHandler
from time import sleep
from ets_data_mapper import ETSData

HOST = ""
PORT = 8844
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

handler = CommandHandler()
handler.start()


class ReceiveThread(Thread):
    def __init__(self, conn, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(ReceiveThread, self).__init__(group, target, name, args, kwargs, verbose)
        self.connection = conn

    def run(self):
        while 1:
            try:
                data = self.connection.recv(1)  # recv command
                data += self.connection.recv(4)  # recv control id
                data += self.connection.recv(1)  # recv button state
                data += self.connection.recv(4)  # recv control id
            except:
                print("Failed to recv. Client probably disconnected")
                break
            if not data:
                break
            command, control_id, button_state, control_position = struct.unpack("!BiBi", data)
            handler.add_command(command, control_id, button_state, control_position)


class SendThread(Thread):
    def __init__(self, conn, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(SendThread, self).__init__(group, target, name, args, kwargs, verbose)
        self.connection = conn

    def run(self):
        data = ETSData()
        map_file = mmap(-1, 16 * 1024, "Local\SimTelemetryETS2", ACCESS_READ)
        while 1:
            try:
                map_file.seek(0)
                data.load_from_mmap(map_file)
                self.connection.send(
                    struct.pack("!2?f2i2f", data.truck.engine_enabled, data.truck.trailer_attached, data.truck.speed,
                                data.truck.gear_info.gear, data.truck.gear_info.gears,
                                data.truck.engine_info.engine_rpm, data.truck.engine_info.engine_rpm_max))
            except:
                print("Failed to send. Client probably disconnected")
                break
            sleep(0.02)


while 1:
    conn, addr = s.accept()
    print 'Connected by', addr
    ReceiveThread(conn).start()
    SendThread(conn).start()
