import time
import multiprocessing
import math
import time
from threading import Thread, current_thread
from Queue import Queue


imageQueue = Queue()


x=0
while x<666:
	imageQueue.put('lol')
	x=x+1


def processImage():
 	idleTime = time.time()
 	continueLoop = True
 	while(time.time() - idleTime < 0.1 or not imageQueue.empty() and continueLoop==True): #exits after timeout unless thread still has data to process
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