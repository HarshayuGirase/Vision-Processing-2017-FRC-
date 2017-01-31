import numpy as np
import cv2
import time
import multiprocessing
import math
from threading import Thread
from Queue import Queue

cannyImages = []
mainQueue = Queue()
mainQueue.put('./Boiler1.bmp')
mainQueue.put('./Boiler2.bmp')

def processImage():
	print 'lol' #just to test


#Main Program Start 
thread1 = Thread(target=processImage, args=())
thread1.start()

x=0
while x<500:
	if not thread1.isAlive():
		thread1.run()
	x=x+1

