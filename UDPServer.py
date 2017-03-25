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

s.sendto("SFHS:+32:71",("10.23.67.255",port))
s.sendto("SFHS:-69:69",("10.23.67.255",port))
#s.sendto("ccc",("10.23.67.255",port))

#s.sendto("ddd",("10.23.67.255",port))
#s.sendto("eee",("10.23.67.255",port))
##s.sendto("fff",("10.23.67.255",port))
#s.sendto("ggg",("10.23.67.255",port))


print 'done'

