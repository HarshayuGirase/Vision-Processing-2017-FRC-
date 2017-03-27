import socket
import time
import cv2
import numpy as np

start_time = time.clock()

TCP_IP = ''
TCP_PORT = 2359
BUFFER_SIZE = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates the socket
print ('socket created')
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so it can be recreated
s.bind((TCP_IP, TCP_PORT)) #binds the socket to certain address using IP and Port#
print ('socket bind')

s.listen(1) #look out for 1 connection
print ('socket listen')
conn, addr = s.accept()
print ('connection accepted')

conn.send('nikhils a fucking bastard pussy ass STD carrier')

conn.close()
s.close()


print (time.clock() - start_time)
print ('conn closed')
