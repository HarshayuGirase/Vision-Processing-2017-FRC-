import numpy as np
import cv2
import time
import multiprocessing
import math


#depthMat = cv2.imread('/Users/harshayugirase/Desktop/LiveFeed/image5.png', cv2.IMREAD_UNCHANGED) #mat with all depth values associated for each pixel value
depthMat = cv2.imread('./Boiler3.png', cv2.IMREAD_UNCHANGED)
img = cv2.cvtColor(np.uint16(depthMat),cv2.COLOR_GRAY2RGB) 


def getDistanceAngle(xCoordinate):
	CENTERX = 320
	angle = (xCoordinate - 320)/10
	return angle

def lowGoalCovered():
	kernel = np.ones((3,3))
	ret,threshold = cv2.threshold(np.uint8(img),0,60000,cv2.THRESH_BINARY)
	erosion = cv2.erode(threshold,kernel,iterations = 16) #increase if necessary 
	dilation = cv2.dilate(erosion,kernel,iterations = 8)
	start_time = time.clock()
	edges = cv2.Canny(np.uint8(dilation),4,2) #edge detection after some noise filtering   

	#cv2 version returns 2 or 3 depending on version :/
	try:
		contours,_ = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #finds all contours
		contoursParent, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #finds parent contours
	except:
		_,contours,_ = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #finds all contours
		_,contoursParent, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #finds parent contours


	#cv2.drawContours(img,contours,4,(0,255,0),3)
	xCenterValues = []; yCenterValues = []
	FINALCONTOURS = []

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
				contours.pop(x)
				x=x-1

	for c in contours: # compute the center of the contour
		M = cv2.moments(c)
		
		cX = 0
		cY = 0
		if(M["m00"]!=0):
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])


		#try to find contour area of low goal and limit size of xCenterValues and yCenterValues, so that only that range will be viewed...
		width = len(edges[0])
		height = sum([len(arr) for arr in edges])/width


		if(cY>height/2):
			if cY in yCenterValues:
				nikhil = 'ugly'
			else:
				xCenterValues.append(cX)
				yCenterValues.append(cY)
				FINALCONTOURS.append(c)

	for i in range(0,len(yCenterValues)):
		width = len(edges[0])
		height = sum([len(arr) for arr in edges])/width
		if(yCenterValues[i]>0 and yCenterValues[i]<400 and cv2.contourArea(FINALCONTOURS[i])>4000): #modify contour area later
			cv2.circle(img,(xCenterValues[i],yCenterValues[i]),7,(239,95,255),-1) #draw the circle where center is
			print ('X Center is: ' + str(xCenterValues[i])) #calculate the x value of the center...
			print ('Y Center is: ' + str(yCenterValues[i])) #calculate the y value of the center...
			print ('Contour Area is: ' + str(cv2.contourArea(FINALCONTOURS[i]))) 
			print ('Angle to goal: ' + str(getDistanceAngle(xCenterValues[i])))

			try:
				print ('Distance to Goal is: ' + str(depthMat[xCenterValues[i]][yCenterValues[i]]/25.4) + ' inches')
			except:
				try:
					print 'ONE IS OUT OF BOUNDS*'
					print ('Distance to Goal is: ' + str(depthMat[yCenterValues[i]][xCenterValues[i]]/25.4) + ' inches') #inverted
					print
				except:
					distance = 999999 #cannot get distance :/ 

			cv2.drawContours(img,FINALCONTOURS,i,(0,255,0),3) #draw the contour

	print("--- %s seconds ---" % (time.clock() - start_time))

	cv2.imwrite('/Users/harshayugirase/Desktop/output.bmp', img)
	cv2.imwrite('/Users/harshayugirase/Desktop/cannyimage.bmp', edges)
	cv2.imwrite('/Users/harshayugirase/Desktop/dilated.bmp', dilation)

	
lowGoalCovered()