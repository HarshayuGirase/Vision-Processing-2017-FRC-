import numpy as np
import cv2
import math

def getDistanceAngle(xCoordinate):
	CENTERX = 320
	angle = (xCoordinate - 320)/10
	return angle


#calibrates low goal when kinect is perpendicular to it  
def calibrateWithLowGoal(imageFileBMP, imageFilePNG):
	img = cv2.imread(imageFileBMP) #image read
	depthMat = cv2.imread(imageFilePNG, cv2.IMREAD_ANYDEPTH) #mat with all depth values associated for each pixel value
	kernel = np.ones((3,3),np.uint8)
	erosion = cv2.erode(img,kernel,iterations = 15)
	dilation = cv2.dilate(erosion,kernel,iterations = 10)
	edges = cv2.Canny(dilation,100,200) #edge detection after some noise filtering   

	(_, contours, _) = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #finds all contours
	(_, contoursParent, _) = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #finds parent contours

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
				lol = 0
			else:
				xCenterValues.append(cX)
				yCenterValues.append(cY)
				FINALCONTOURS.append(c)
		
	YCENTER = 0;
	ANGLE = 0;

	for i in range(0,len(yCenterValues)):
		width = len(edges[0])
		height = sum([len(arr) for arr in edges])/width
		if(yCenterValues[i]>250 and yCenterValues[i]<340 and cv2.contourArea(FINALCONTOURS[i])>3000): #modify contour area later
			YCENTER = yCenterValues[i]
			ANGLE = getDistanceAngle(xCenterValues[i])
	

	if (ANGLE <= 3 and ANGLE >=-3):
		if(YCENTER>320 and YCENTER <330):
			return 'CALIBRATED :D'
		else:
			if(YCENTER>330):
				return 'Please increase the angle of the kinect.'
			if(YCENTER<320):
				return 'Please decrease the angle of the kinect.'
	else:	
		return 'Please align the kinect perpendicular to the low goal to calibrate it.'

	

x = calibrateWithLowGoal('./Boiler1.bmp', './Boiler1.png')
print x