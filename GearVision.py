import numpy as np
import cv2
import time
import multiprocessing


img = cv2.imread('/Users/harshayugirase/Desktop/output1.bmp', cv2.IMREAD_UNCHANGED)
img = cv2.cvtColor(np.uint16(img),cv2.COLOR_GRAY2RGB)

def getDistanceAngle(xCoordinate):
 	CENTERX = 320
 	angle = (xCoordinate - 320)/10
 	return angle

def getAngle(depthT1,depthT2):
 	yComponent = depthT2 - depthT1
 	xComponent = 209.55 #millimeter distance between two centers
 	degrees = math.degrees(math.atan2(yComponent, xComponent))
 	return degrees


def GearVision():
	kernel = np.ones((3,3))
	ret,threshold = cv2.threshold(np.uint8(img),0,60000,cv2.THRESH_BINARY)
	erosion = cv2.erode(threshold,kernel,iterations = 5) #increase if necessary 
	dilation = cv2.dilate(erosion,kernel,iterations = 5)
	start_time = time.clock()
	edges = cv2.Canny(np.uint8(dilation),4,2) #edge detection after some noise filtering   

	#cv2 version returns 2 or 3 depending on version :/
	try:
		contours,_ = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #finds all contours
		contoursParent, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #finds parent contours
	except:
		_,contours,_ = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #finds all contours
		_,contoursParent, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #finds parent contours


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
		if(True): #avoids duplicates (only get clockwise contours)
			M = cv2.moments(c)
			cX = 0
			cY = 0
			if(M["m00"]!=0):
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])

			#try to find contour area of low goal and limit size of xCenterValues and yCenterValues, so that only that range will be viewed...
			width = len(edges[0])
			height = sum([len(arr) for arr in edges])/width

			
			xCenterValues.append(cX)
			yCenterValues.append(cY)
			FINALCONTOURS.append(c)

	for i in range(0,len(FINALCONTOURS)):
		cv2.drawContours(img,FINALCONTOURS,i,(0,255,0),3) #draw the contour

	targetcentersX = []
	targetcentersY = []

	for i in range(0,len(yCenterValues)):
		width = len(edges[0])
		height = sum([len(arr) for arr in edges])/width
		if(cv2.contourArea(FINALCONTOURS[i])>300 and cv2.contourArea(FINALCONTOURS[i])<15000): #modify contour area later
			cv2.circle(img,(xCenterValues[i],yCenterValues[i]),7,(239,95,255),-1) #draw the circle where center is
			print ('X Center is: ' + str(xCenterValues[i])) #calculate the x value of the center...
			targetcentersX.append(xCenterValues[i])
			print ('Y Center is: ' + str(yCenterValues[i])) #calculate the y value of the center...
			targetcentersY.append(yCenterValues[i])
			print ('Contour Area is: ' + str(cv2.contourArea(FINALCONTOURS[i]))) 
			print ('Angle to goal: ' + str(getDistanceAngle(xCenterValues[i])))
		#	cv2.drawContours(img,FINALCONTOURS,i,(0,255,0),3) #draw the contour
			

	if(len(targetcentersX)==2): #if we get the retroreflective tape..
		print("Y Center is: " + str(sum(yCenterValues)/len(yCenterValues)))
		print("X Center is: " + str(sum(xCenterValues)/len(xCenterValues)))
	print("--- %s seconds ---" % (time.clock() - start_time))

	cv2.imwrite('/Users/harshayugirase/Desktop/output.bmp', img)
	cv2.imwrite('/Users/harshayugirase/Desktop/cannyimage.bmp', edges)
	#cv2.imwrite('/Users/harshayugirase/Desktop/threshold.bmp', threshold)

GearVision()




