import time
import multiprocessing
import math
import time
from threading import Thread, current_thread
from Queue import Queue
import cv2

imageQueue = Queue()

img = cv2.imread('./Boiler1.bmp') #image read
width = len(img[0])
height = sum([len(arr) for arr in img])/width
region1 = img[0:height/3, 0:width]
region2 = img[height/3:2*height/3, 0:width]
region3 = img[2*height/3:height, 0:width]

imageQueue.put(cv2.imwrite('./1_1', region1))
imageQueue.put(cv2.imwrite('./1_2', region2))
imageQueue.put(cv2.imwrite('./1_3', region3))



print imageQueue.qsize()


#method that performs erosion, dilation, and canny on an image :D
def processImage():
 	idleTime = time.time()
 	continueLoop = True
 	while(time.time() - idleTime < 0.2 or not imageQueue.empty() and continueLoop==True): #exits after timeout unless thread still has data to process
 		if(imageQueue.qsize() > 0): #unsafe method. if another thread pops data after this line and the queue is empty program will hang.
 			print imageQueue.get()
 			print current_thread()
 		if(imageQueue.empty()==True):
 			continueLoop=False

 
thread1 = Thread(target=processImage, args=())
thread2 = Thread(target=processImage, args=())
thread3 = Thread(target=processImage, args=())
#thread4 = Thread(target=recombine, args=())

thread1.start()
thread2.start()
thread3.start()
#thread4.start()

thread1.join()
thread2.join()
thread3.join()
#thread4.join()