import numpy as np
import cv2
import time
import multiprocessing
import math


def getDistanceAngle(xCoordinate):
	CENTERX = 320
	angle = (xCoordinate - 320)/10
	return angle

def hopperCovered():
	img = cv2.imread('/Users/harshayugirase/Desktop/Depth Images 2/Hopper1.bmp') #image read
	depthMat = cv2.imread('/Users/harshayugirase/Desktop/Depth Images 2/Hopper1.png', cv2.IMREAD_ANYDEPTH) #mat with all depth values associated for each pixel value
	start_time = time.time()
	kernel = np.ones((3,3),np.uint8)
	erosion = cv2.erode(img,kernel,iterations = 15)
	dilation = cv2.dilate(erosion,kernel,iterations = 10)
	edges = cv2.Canny(dilation,100,200) #edge detection after some noise filtering 

	print("--- %s seconds ---" % (time.time() - start_time))

	(_, contours, _) = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #finds all contours
	(_, contoursParent, _) = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #finds parent contours

	#cv2.drawContours(img,contours,4,(0,255,0),3)
	xCenterValues = []; yCenterValues = []
	FINALCONTOURS = []

	#print len(contours)
	#print len(contoursParent)

	#print contoursParent[0][2][0][0] <--- test to see contours data

	for i in range(0, len(contoursParent)): #essentially only keeps the children contours
		for x in range(0, len(contours)):
			same = True
			try:
				if(len(contoursParent[i])==len(contours[x])):
					for check in range(0,len(contoursParent[i])):
						if(contoursParent[i][check][0][0]==contours[x][check][0][0] and contoursParent[i][check][0][1]==contours[x][check][0][1]):
							lolz = 0 #nothing lol
						else:
							same = False
				else:
					same = False
				break;
			except ValueError:
				print 'rip'

			if(same==True):
				#contours.pop(x)
				x=x-1

	for c in contours: # compute the center of the contour
		M = cv2.moments(c)
		cX = 0
		cY = 0
		if(M["m00"]!=0):
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
		
		width = len(edges[0])
		height = sum([len(arr) for arr in edges])/width
		if(cY<height*.666):
			if cY in yCenterValues:
				lol = 0
			else:
				xCenterValues.append(cX)
				yCenterValues.append(cY)
				FINALCONTOURS.append(c)
		
			

	for i in range(0,len(yCenterValues)):
		width = len(edges[0])
		height = sum([len(arr) for arr in edges])/width
		if(yCenterValues[i]>200 and yCenterValues[i]<300): #modify contour area later
			cv2.circle(img,(xCenterValues[i],yCenterValues[i]),3,(239,95,255),-1) #draw the circle where center is
			print ('X Center is: ' + str(xCenterValues[i])) #calculate the x value of the center...
			print ('Y Center is: ' + str(yCenterValues[i])) #calculate the y value of the center...
			print ('Contour Area is: ' + str(cv2.contourArea(FINALCONTOURS[i]))) 
			print ('Angle to goal: ' + str(getDistanceAngle(xCenterValues[i])))

			try:
				print ('Distance to Goal is: ' + str(depthMat[xCenterValues[i]][yCenterValues[i]]/25.4) + ' inches')
			except:
				nikhilishawt = 0 #nothing
			cv2.drawContours(img,FINALCONTOURS,i,(0,255,0),3) #draw the contour

	

	cv2.imwrite('/Users/harshayugirase/Desktop/output.bmp', img)
	cv2.imwrite('/Users/harshayugirase/Desktop/cannyimage.bmp', edges)

	#print cv2.getNumberOfCPUs()
	#print multiprocessing.cpu_count()


hopperCovered()