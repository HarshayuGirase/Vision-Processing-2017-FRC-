import socket
import cv2
import numpy as np
import time
import select
import math
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from Tkinter import *


host = '' #bind to any interface...                     


master = Tk()
w1 = Scale(master, from_=0, to=255, orient=HORIZONTAL)
w1.pack()
w2 = Scale(master, from_=0, to=255, orient=HORIZONTAL)
w2.pack()
w3 = Scale(master, from_=0, to=255, orient=HORIZONTAL)
w3.pack()
w4 = Scale(master, from_=0, to=255, orient=HORIZONTAL)
w4.pack()
w5 = Scale(master, from_=0, to=255, orient=HORIZONTAL)
w5.pack()
w6 = Scale(master, from_=0, to=255, orient=HORIZONTAL)
w6.pack()
w1.set(83)
w2.set(255)
w3.set(50)
w4.set(255)
w5.set(240)
w6.set(255)



HEIGHT = 480
WIDTH = 640

RUNTIME = 40 #seconds of how long program should run

COLORIMAGEARRAY = []
start_time = time.clock()
print 'Program has started.'

#TCP_IP = '10.23.67.71'
TCP_IP = '192.168.1.2'
TCP_PORT = 2374
BUFFER_SIZE = 9999

print 'Trying to connect...'
hasConnectedToPogace = False
timeouttoconnect = time.time()
while(hasConnectedToPogace==False and time.time()-timeouttoconnect<120): #try connecting to pogace for 120 seconds...
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so it can be recreated
		s.connect((TCP_IP, TCP_PORT))
		s.setblocking(0)
		hasConnectedToPogace = True
	except:
		hasConnectedToPogace = False









#in form hbound, sbound, vbound
s.send('change hsv;83;255;50;255;240;255!')
plt.ion()
plt.show()

try:
	startframetime = time.time()
	count = 0
	while(time.time() - startframetime < RUNTIME):

		centersTuple = ()
		s.send('color image')
		count = count+1
		colorimagestring = ''
		while(len(colorimagestring)<HEIGHT*WIDTH and time.time() - startframetime < RUNTIME):
			ready = select.select([s], [], [], 0.01)
			if ready[0]:
				data = s.recv(BUFFER_SIZE)
				colorimagestring = colorimagestring + data

		print 'received color image'
		print count

		timeslidermoves = time.time()
		while (time.time() - timeslidermoves < 3):
			master.update()
		
		s.send('change hsv;' + str(w1.get()) + ';' + str(w2.get()) + ';' + str(w3.get()) + ';' + str(w4.get()) + ';' + str(w5.get()) + ';' + str(w6.get()) + '!')
		#s.send('change hsv;83;255;50;255;240;255!')		
		try:
			if len(colorimagestring)==HEIGHT*WIDTH:
				backtoarray = np.fromstring(colorimagestring, dtype=np.uint8).reshape(480,640)

				cv2.imwrite('./lastimage.png', backtoarray)
				lastimage = mpimg.imread('./lastimage.png')
				plt.imshow(lastimage)
				plt.draw()
				plt.pause(0.000001)

			else:
				print 'fucked up'
		except Exception as ex:
			print ex


except Exception as ex:
	print ex
	 
s.send('end') #closes socket gracefully :D
s.close()

 
print
print 'Program done running :D'
