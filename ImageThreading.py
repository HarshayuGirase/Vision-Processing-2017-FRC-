import time
import multiprocessing
import numpy as np
import math
import time
from threading import Thread, current_thread
from Queue import Queue
import cv2

imageQueue = Queue()
numberProcessed = [] #integer of processed in form {1,1,2,1...}


def addToImageQueueForTesting():
	img = cv2.imread('./Boiler1.bmp') #image read
	width = len(img[0])
	height = sum([len(arr) for arr in img])/width
	region1 = img[0:height/3, 0:width]
	region2 = img[height/3:2*height/3, 0:width]
	region3 = img[2*height/3:height, 0:width]

	cv2.imwrite('./1_1.bmp', region1)
	cv2.imwrite('./1_2.bmp', region2)
	cv2.imwrite('./1_3.bmp', region3)

	imageQueue.put('./1_1.bmp')
	imageQueue.put('./1_2.bmp')
	imageQueue.put('./1_3.bmp')


	img = cv2.imread('./Boiler2.bmp') #image read
	width = len(img[0])
	height = sum([len(arr) for arr in img])/width
	region1 = img[0:height/3, 0:width]
	region2 = img[height/3:2*height/3, 0:width]
	region3 = img[2*height/3:height, 0:width]

	cv2.imwrite('./2_1.bmp', region1)
	cv2.imwrite('./2_2.bmp', region2)
	cv2.imwrite('./2_3.bmp', region3)

	imageQueue.put('./2_1.bmp')
	imageQueue.put('./2_2.bmp')
	imageQueue.put('./2_3.bmp')

	img = cv2.imread('./Boiler3.bmp') #image read
	width = len(img[0])
	height = sum([len(arr) for arr in img])/width
	region1 = img[0:height/3, 0:width]
	region2 = img[height/3:2*height/3, 0:width]
	region3 = img[2*height/3:height, 0:width]

	cv2.imwrite('./3_1.bmp', region1)
	cv2.imwrite('./3_2.bmp', region2)
	cv2.imwrite('./3_3.bmp', region3)

	imageQueue.put('./3_1.bmp')
	imageQueue.put('./3_2.bmp')
	imageQueue.put('./3_3.bmp')
addToImageQueueForTesting()





print 'helloooo world'


print imageQueue.qsize()

#method that performs erosion, dilation, and canny on an image :Db
def processImage():
 	idleTime = time.time()
 	continueLoop = True
 	while(time.time() - idleTime < 0.5 or not imageQueue.empty() and continueLoop==True): #exits after timeout unless thread still has data to process
 		if(imageQueue.qsize() > 0): 
 			filepath = imageQueue.get()
 			img = cv2.imread(filepath)
 			kernel = np.ones((3,3))
			erosion = cv2.erode(img,kernel,iterations = 16)  
			dilation = cv2.dilate(erosion,kernel,iterations = 8)
			edges = cv2.Canny(dilation,100,200) 

 			cv2.imwrite(filepath, edges) #overwrite that bmp that was passed as a canny version of bmp
 			numberProcessed.append(int(filepath[filepath.index('/')+1])) #get image number, like 1,2,3,4 etc

 		if(imageQueue.empty()==True):
 			continueLoop=False


#Method that takes canny images and combines them into one
GAME_TIME = 2 #however long you want it to run for...


def recombineImage():
	print 'started'
	startthread4 = time.time()
	currentImageIndex = 1
	while(time.time()-startthread4 < GAME_TIME):
		if(numberProcessed.count(currentImageIndex)==3):
			print 'here'
			part1 = cv2.imread('./' + str(currentImageIndex) + '_1.bmp')
			part2 = cv2.imread('./' + str(currentImageIndex) + '_2.bmp')
			part3 = cv2.imread('./' + str(currentImageIndex) + '_3.bmp') 
			combineOneTwo = np.concatenate((part1,part2), axis=0)
			finalImage = np.concatenate((combineOneTwo , part3), axis=0)
			#cv2.imwrite('./LatestImage.bmp', finalImage) #add this image to the file...
 			
			numberProcessed[:] = (value for value in numberProcessed if value != currentImageIndex) #remove all of the what is in the list  
			
			if(len(numberProcessed)==0 and currentImageIndex==3):
				print("--- %s seconds ---" % (time.time() - startthread4))

			currentImageIndex = currentImageIndex + 1







#Main Program Start

thread1 = Thread(target=processImage, args=())
thread2 = Thread(target=processImage, args=())
thread3 = Thread(target=processImage, args=())
thread4 = Thread(target=recombineImage, args=())

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()


print numberProcessed





starttime2 = time.time()
img = cv2.imread('./Boiler2.bmp') #image read
depthMat = cv2.imread('./Boiler2.png', cv2.IMREAD_ANYDEPTH) #mat with all depth values associated for each pixel value
kernel = np.ones((3,3))
erosion = cv2.erode(img,kernel,iterations = 16) #increase if necessary 
dilation = cv2.dilate(erosion,kernel,iterations = 8)
edges = cv2.Canny(dilation,100,200) #edge detection after some noise filtering   

img = cv2.imread('./Boiler1.bmp') #image read
depthMat = cv2.imread('./Boiler1.png', cv2.IMREAD_ANYDEPTH) #mat with all depth values associated for each pixel value
start_time = time.time()
kernel = np.ones((3,3))
erosion = cv2.erode(img,kernel,iterations = 16) #increase if necessary 
dilation = cv2.dilate(erosion,kernel,iterations = 8)
edges = cv2.Canny(dilation,100,200) #edge detection after some noise filtering 

img = cv2.imread('./Boiler3.bmp') #image read
depthMat = cv2.imread('./Boiler3.png', cv2.IMREAD_ANYDEPTH) #mat with all depth values associated for each pixel value
start_time = time.time()
kernel = np.ones((3,3))
erosion = cv2.erode(img,kernel,iterations = 16) #increase if necessary 
dilation = cv2.dilate(erosion,kernel,iterations = 8)
edges = cv2.Canny(dilation,100,200) #edge detection after some noise filtering   

print("--- %s seconds ---" % (time.time() - starttime2))
