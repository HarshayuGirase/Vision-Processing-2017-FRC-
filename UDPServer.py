import socket, traceback
import time
import sys

host = '' #bind to any interface...                     
port = 2444

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

print 'Successfully bound.'

start_time = time.clock()

while (time.clock() - start_time < 5):
    try:
        s.sendto("nikhils a fucking bastard pussy ass STD carrier",("10.23.67.255",port))
    except Exception as e:
         x = 0

print 'done'

