import socket, traceback
import time
import sys

host = ''                      # Bind to all interfaces
port = 8526

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

print 'Successfully bound.'

start_time = time.time()

while (time.time() - start_time < 10):
    try:
        data = str.encode("foo")
        s.sendto(data,("192.168.1.255",port))
        message, address = s.recvfrom(8192)
        print address
    except Exception as e:
         x = 0


print 'done'

