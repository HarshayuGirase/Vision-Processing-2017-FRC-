import socket
import cv2
import numpy as np
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = 2797
BUFFER_SIZE = 9999
REQUESTEDMESSAGE = 'Is Nikhil hot?'

img = cv2.imread('./Hopper1.bmp') #image read
width = len(img[0])
height = sum([len(arr) for arr in img])/width
region1 = img[5*height/16:14*height/16, 0:width] #using region1 cuts time in by like .008 seconds (like by 40%)
img_str = cv2.imencode('.bmp', region1)[1].tostring()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

print len(img_str)
s.send(img_str)
dataReceived = s.recv(BUFFER_SIZE)
print len(dataReceived)


s.close()

