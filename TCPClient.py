import socket
import cv2
import numpy as np
import sys
import time
import select


RUNTIME = 5 #seconds of how long program should run

COLORIMAGEARRAY = []
DEPTHIMAGEARRAY = []
start_time = time.clock()
print 'Program has started.'

TCP_IP = '192.168.1.20'
TCP_PORT = 2373
BUFFER_SIZE = 9999

print 'Trying to connect...'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so it can be recreated
s.connect((TCP_IP, TCP_PORT))
s.setblocking(0)

startframetime = time.time()
count = 0
while(time.time() - startframetime < RUNTIME):
	colorimagestring = ''
	while(len(colorimagestring)<307200 and time.time() - startframetime < RUNTIME):
		ready = select.select([s], [], [], 0.01)
		if ready[0]:
			data = s.recv(BUFFER_SIZE)
			colorimagestring = colorimagestring + data

	print 'received color image'
	print len(colorimagestring)
	try:
		if len(colorimagestring)==307200:
			backtoarray = np.fromstring(colorimagestring, dtype=np.uint8).reshape(480,640)
			COLORIMAGEARRAY.append(backtoarray)
			print count
		else:
			print 'fucked up'
	except:
		print 'fucked up2'


	depthimagestring = ''
	while(len(depthimagestring)<614400 and time.time() - startframetime < RUNTIME):
		ready = select.select([s], [], [], 0.01)
		if ready[0]:
			data = s.recv(BUFFER_SIZE)
			depthimagestring = depthimagestring + data

	print 'received depth image'
	print len(depthimagestring)
	try:
		if len(depthimagestring)==614400:
			backtoarray = np.fromstring(depthimagestring, dtype=np.uint16).reshape(480,640)
			DEPTHIMAGEARRAY.append(backtoarray)
			print count
		else:
			print 'fucked up'
	except:
		print 'fucked up2'

	

s.close()

print (time.clock() - start_time)

for i in range(0,len(COLORIMAGEARRAY)):
	cv2.imwrite('/Users/harshayugirase/Desktop/LiveFeed/image' + str(i) + '.bmp', COLORIMAGEARRAY[i])

for i in range(0,len(DEPTHIMAGEARRAY)):
	cv2.imwrite('/Users/harshayugirase/Desktop/LiveFeed/image' + str(i) + '.png', DEPTHIMAGEARRAY[i])

print 'Program done running :D'