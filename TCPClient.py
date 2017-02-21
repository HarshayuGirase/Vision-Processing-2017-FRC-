import socket
import cv2
import numpy as np
import sys
import time

TCP_IP = '192.168.1.5'
TCP_PORT = 2320
BUFFER_SIZE = 1500


img = cv2.imread('./Hopper1.bmp') #image read
kernel = np.ones((3,3))
erosion = cv2.erode(img,kernel,iterations = 16) #increase if necessary 
dilation = cv2.dilate(erosion,kernel,iterations = 8)

# width = len(img[0])
# height = sum([len(arr) for arr in img])/width
# region1 = dilation[5*height/16:14*height/16, 0:width] #using region1 cuts time in by like .008 seconds (like by 40%)
# img_str = cv2.imencode('.bmp', region1)[1].tostring()

print 'before connect'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so it can be recreated
s.connect((TCP_IP, TCP_PORT))

print 'connected'

imageasstring = ''
count = 0
timeout = time.clock()

for i in range(0,410):
	data = s.recv(BUFFER_SIZE)
	count = count + 1
	imageasstring = imageasstring + data

s.close()

print count
print len(imageasstring)

backtoarray = np.fromstring(ndatastring, np.int16).reshape(480, 640)
cv2.imwrite('/Users/harshayugirase/Desktop/omfg.bmp', backtoarray)
