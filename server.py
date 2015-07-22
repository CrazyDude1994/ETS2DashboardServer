import socket
import struct
from mmap import *
from threading import Thread
#from command_handler import CommandHandler
from time import sleep
from ets_data_mapper import ETSData, TruckEncoder
from json import dumps, loads

HOST = ""
PORT = 8845
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

#handler = CommandHandler()
#handler.start()


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
            #handler.add_command(command, control_id, button_state, control_position)


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
                json_data = dumps(data, cls=TruckEncoder)
                self.connection.send(struct.pack("!i", len(json_data)))
                self.connection.send(json_data)
            except Exception as e:
                print("Failed to send. Client probably disconnected.[{0}]".format(e.message))
                break
            sleep(0.02)


while 1:
    conn, addr = s.accept()
    print 'Connected by', addr
    ReceiveThread(conn).start()
    SendThread(conn).start()
