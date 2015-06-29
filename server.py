import socket
import struct


HOST = ''
PORT = 8844
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(4)
    number = struct.unpack("!i", data)[0]
    print(number)
    if not data: break
conn.close()