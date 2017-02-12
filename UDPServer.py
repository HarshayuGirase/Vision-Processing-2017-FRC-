import socket, traceback
import time
import sys

host = socket.gethostname()                      # Bind to all interfaces
port = 8524

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

print 'Successfully bound.'

start_time = time.time()

while (time.time() - start_time < 2):
    try:
        s.sendto('I am the SFHS Server RAWR!',('192.168.1.255', port))
    except (KeyboardInterrupt, SystemExit):
        x = 0
    except:
        x = 0
        

print 'done'