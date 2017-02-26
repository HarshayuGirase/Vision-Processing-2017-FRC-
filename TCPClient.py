import socket
import cv2
import numpy as np
import sys
import time
import select

IMAGEARRAY = []
start_time = time.clock()
print 'Program has started.'

TCP_IP = '192.168.1.37'
TCP_PORT = 2371
BUFFER_SIZE = 9999

print 'Trying to connect...'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so it can be recreated
s.connect((TCP_IP, TCP_PORT))
s.setblocking(0)

startframetime = time.time()
count = 0
while(time.time() - startframetime < 10):
	s.send('Gimme latest image')
	count = count+1
	imageasstring = ''

	while(len(imageasstring)<614400 and time.time()-startframetime<10):
		ready = select.select([s], [], [], 0.01)
		if ready[0]:
			data = s.recv(BUFFER_SIZE)
			imageasstring = imageasstring + data

	print 'received image'
	try:
		if len(imageasstring)==614400:
			backtoarray = np.fromstring(imageasstring, np.int16).reshape(480, 640)
			IMAGEARRAY.append(backtoarray)
			print count
		else:
			print 'fucked up'
	except:
		print 'fucked up2'
	
s.close()

print (time.clock() - start_time)

for i in range(0,len(IMAGEARRAY)):
	cv2.imwrite('/Users/harshayugirase/Desktop/LiveFeed/image' + str(i) + '.png', IMAGEARRAY[i])

print 'Program done running :D'