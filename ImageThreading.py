import numpy as np
import cv2
import time
import multiprocessing
import math
from threading import Thread

cannyImages = []

def processImage(imageInput,name):
	kernel = np.ones((3,3),np.uint8)
	erosion = cv2.erode(imageInput,kernel,iterations = 15)
	dilation = cv2.dilate(erosion,kernel,iterations = 10)
	edges = cv2.Canny(dilation,100,200)
	cannyImages.append(edges)

def threadImage():
	img = cv2.imread('./Hopper1.bmp') #image read

	start_time = time.time()

	width = len(img[0])
	height = sum([len(arr) for arr in img])/width

	region1 = img[0:height/4, 0:width]
	region2 = img[height/4:height/2, 0:width]
	region3 = img[height/2:(3*height/4), 0:width]
	region4 = img[(3*height/4):height, 0:width]

	thread1 = Thread(target=processImage(region1,'region1'))
	thread2 = Thread(target=processImage(region2,'region2'))
	thread3 = Thread(target=processImage(region3,'region3'))
	thread4 = Thread(target=processImage(region4,'region4'))

	thread1.start()
	thread2.start()
	thread3.start()
	thread4.start()

	thread1.join()
	thread2.join()
	thread3.join()
	thread4.join()

	combinedCannyImage = cannyImages[0]
	c = np.concatenate((combinedCannyImage , cannyImages[1]))
	d = np.concatenate((c,cannyImages[2]))
	edges = np.concatenate((d,cannyImages[3]))

	cv2.imwrite('/Users/harshayugirase/Desktop/CombinedCanny.bmp',edges)


	print("--- %s seconds ---" % (time.time() - start_time))




def withoutThreading():
	img = cv2.imread('./Hopper1.bmp') #image read
	depthMat = cv2.imread('./Hopper1.png', cv2.IMREAD_ANYDEPTH) #mat with all depth values associated for each pixel value
	start_time = time.time()
	kernel = np.ones((3,3),np.uint8)
	erosion = cv2.erode(img,kernel,iterations = 15)
	dilation = cv2.dilate(erosion,kernel,iterations = 10)
	edges = cv2.Canny(dilation,100,200) #edge detection after some noise filtering 

	print("--- %s seconds ---" % (time.time() - start_time))
 
threadImage()
#withoutThreading()