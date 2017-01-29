import numpy as np
import cv2
import time
import multiprocessing
import math
from threading import Thread
from Queue import Queue
from collections import deque

cannyImages = []
mainQueue = deque()
mainQueue.append('./Boiler1.bmp')

def processImage():
	while(len(mainQueue)>0):
		kernel = np.ones((3,3),np.uint8)
		erosion = cv2.erode(imageInput,kernel,iterations = 20)
		dilation = cv2.dilate(erosion,kernel,iterations = 8)
		edges = cv2.Canny(dilation,100,200)
		cannyImages.append(edges)

def threadImage():
	
	start_time = time.time()

	thread1 = Thread(target=processImage(), args=())
	thread2 = Thread(target=processImage(), args=())
	thread3 = Thread(target=processImage(), args=())
	thread4 = Thread(target=processImage(), args=())


	thread1.start()
	thread2.start()
	thread3.start()
	thread4.start()
	
		img = cv2.imread('./Boiler1.bmp') #image read
		width = len(img[0])
		height = sum([len(arr) for arr in img])/width

		region1 = img[0:height/4, 0:width]
		region2 = img[height/4:height/2, 0:width]
		region3 = img[height/2:(3*height/4), 0:width]
		region4 = img[(3*height/4):height, 0:width]

		mainQueue.popleft()


	combinedCannyImage = cannyImages[0]
	c = np.concatenate((combinedCannyImage , cannyImages[1]))
	d = np.concatenate((c,cannyImages[2]))
	edges = np.concatenate((d,cannyImages[3]))

	


	print("--- %s seconds ---" % (time.time() - start_time))




def withoutThreading():
	img = cv2.imread('./Hopper1.bmp') #image read
	depthMat = cv2.imread('./Hopper1.png', cv2.IMREAD_ANYDEPTH) #mat with all depth values associated for each pixel value
	start_time = time.time()
	kernel = np.ones((3,3),np.uint8)
	erosion = cv2.erode(img,kernel,iterations = 20)
	dilation = cv2.dilate(erosion,kernel,iterations = 8)
	edges = cv2.Canny(dilation,100,200) #edge detection after some noise filtering 

	print("--- %s seconds ---" % (time.time() - start_time))
 
threadImage()
#withoutThreading()