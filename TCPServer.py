import socket
import time
import cv2
import numpy as np

TCP_IP = '127.0.0.1'
TCP_PORT = 2317
BUFFER_SIZE = 1500

depthMat = cv2.imread('./Boiler1.png', cv2.IMREAD_UNCHANGED)
b = np.packbits(depthMat, axis=-1)
print len(b)



# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates the socket
# print ('socket created')
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so it can be recreated
# s.bind((TCP_IP, TCP_PORT)) #binds the socket to certain address using IP and Port#
# print ('socket bind')


# prog_start = time.time()
# while (time.time() - prog_start  < 5):
#     s.listen(1) #look out for 1 connection
#     print ('socket listen')
#     conn, addr = s.accept()
#     print ('connection accepted')

#     time_start = time.time()
#     for i in range(0,3):
#       conn.send('abcde')

#     conn.close()
#     print ('conn closed')

# print ('program exited')