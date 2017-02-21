import socket
import time
import cv2
import numpy as np

start_time = time.clock()

TCP_IP = ''
TCP_PORT = 2321
BUFFER_SIZE = 1500


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates the socket
print ('socket created')
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so it can be recreated
s.bind((TCP_IP, TCP_PORT)) #binds the socket to certain address using IP and Port#
print ('socket bind')


depthMat = cv2.imread('./Boiler4.png', cv2.IMREAD_UNCHANGED) #mat with all depth values associated for each pixel value
ndata = np.frombuffer(depthMat, np.int16)
ndatastring = ndata.tostring()
print len(ndatastring)


prog_start = time.time()

s.listen(1) #look out for 1 connection
print ('socket listen')
conn, addr = s.accept()
print ('connection accepted')

conn.send(ndatastring)

conn.close()



print (time.time() - start_time)
print ('conn closed')
