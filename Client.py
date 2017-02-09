import socket
import cv2
import numpy as np
import sys
import time

TCP_IP = '192.168.1.10'
TCP_PORT = 2502
BUFFER_SIZE = 500
REQUESTEDMESSAGE = 'Is Nikhil hot?'


img = cv2.imread('./Hopper1.bmp') #image read
width = len(img[0])
height = sum([len(arr) for arr in img])/width
region1 = img[5*height/16:14*height/16, 0:width] #using region1 cuts time in by like .008 seconds (like by 40%)
img_str = cv2.imencode('.bmp', region1)[1].tostring()

print 'before connect'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so it can be recreated
s.connect((TCP_IP, TCP_PORT))

print 'connect'

print len(img_str)


print 'sent'

dataRead = 0
imageData = ''

print 'receiving'

start_time = time.time()
while(dataRead < (500000) and time.time()-start_time < 10):
	for i in range(0,len(img_str)/BUFFER_SIZE - 1):
		s.send(img_str[i*BUFFER_SIZE:(i+1)*BUFFER_SIZE])
		imageData = imageData + s.recv(BUFFER_SIZE)
		dataRead = len(imageData)
		
print 'sent'

print dataRead
print 'exit'

nparr = np.fromstring(imageData, np.uint8)
img2 = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

cv2.imwrite('/Users/harshayugirase/Desktop/XDtest1.png', img2)



s.close()

