import socket
import cv2
import numpy as np
import sys
import time
import select
import math


host = '' #bind to any interface...                     
udpport = 2406

udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udps.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
udps.bind((host, udpport))


def getAngle(depthT1,depthT2):
 	yComponent = depthT2 - depthT1
 	xComponent = 209.55 #millimeter distance between two centers
 	degrees = math.degrees(math.atan2(yComponent, xComponent))
 	return degrees

def getDistanceAngle(xCoordinate):
 	CENTERX = 320
 	angle = (xCoordinate - 320)/10
 	return angle

def GearVision(img):
	kernel = np.ones((3,3))
	ret,threshold = cv2.threshold(np.uint8(img),0,60000,cv2.THRESH_BINARY)
	erosion = cv2.erode(img,kernel,iterations = 6) #increase if necessary 
	dilation = cv2.dilate(erosion,kernel,iterations = 4)
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

	#next two for loops remove noise so only retroreflective targets remain
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
		if(cv2.contourArea(c,True) > 0): #avoids duplicates (only get clockwise contours)
			M = cv2.moments(c)
			cX = 0
			cY = 0
			if(M["m00"]!=0):
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])

			#try to find contour area of  gear limit size of xCenterValues and yCenterValues, so that only that range will be viewed...
			width = len(edges[0])
			height = sum([len(arr) for arr in edges])/width

			#if(cY<HEIGHT - 1*HEIGHT/5 and cY>HEIGHT/4): #LITERALLY CHANGE
			x,y,w,h = cv2.boundingRect(c)

			#print h/w
			if(h/w >= 2 and h/w < 4):
				xCenterValues.append(cX)
				yCenterValues.append(cY)
				FINALCONTOURS.append(c)


	targetcentersX = []
	targetcentersY = []

	#for i in range(0,len(FINALCONTOURS)):
		#cv2.drawContours(edges,FINALCONTOURS,i,(0,255,0),3) #draw the contour

	for i in range(0,len(yCenterValues)):
		width = len(edges[0])
		height = sum([len(arr) for arr in edges])/width
		if(cv2.contourArea(FINALCONTOURS[i])>300 and cv2.contourArea(FINALCONTOURS[i])<7000): #we know the targets area must be in this range
			cv2.circle(edges,(xCenterValues[i],yCenterValues[i]),5,(239,95,255),-1) #draw the circle where center is
			#print ('X Center is: ' + str(xCenterValues[i])) #calculate the x value of the center...
			targetcentersX.append(xCenterValues[i])
			#print ('Y Center is: ' + str(yCenterValues[i]b)) #calculate the y value of the center...
			targetcentersY.append(yCenterValues[i])
			print ('Contour Area is: ' + str(cv2.contourArea(FINALCONTOURS[i]))) 
			cv2.drawContours(img,FINALCONTOURS,i,(0,255,0),3) #draw the contour
	
	print 'Targets detected: ' + str(len(targetcentersX))
	print

	cv2.imwrite('/Users/harshayugirase/Desktop/output1.bmp', img)
	cv2.imwrite('/Users/harshayugirase/Desktop/cannyimage1.bmp', edges)
	
	if(len(targetcentersX)==2):
		return (targetcentersX, targetcentersY)
	else:
		return (69,69)
	


HEIGHT = 480
WIDTH = 640

RUNTIME = 30 #seconds of how long program should run

COLORIMAGEARRAY = []
DEPTHIMAGEARRAY = []
start_time = time.clock()
print 'Program has started.'

TCP_IP = '10.23.67.71'
#TCP_IP = '192.168.1.2'
TCP_PORT = 2374
BUFFER_SIZE = 9999

print 'Trying to connect...'
hasConnectedToPogace = False
timeouttoconnect = time.time()
while(hasConnectedToPogace==False and time.time()-timeouttoconnect<120): #try connecting to pogace for 120 seconds...
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so it can be recreated
		s.connect((TCP_IP, TCP_PORT))
		s.setblocking(0)
		hasConnectedToPogace = True
	except:
		hasConnectedToPogace = False

#in form hbound, sbound, vbound
s.send('change hsv;95;143;85;255;205;255!')

try:
	startframetime = time.time()
	count = 0
	while(time.time() - startframetime < RUNTIME):

		centersTuple = ()
		s.send('color image')
		count = count+1
		colorimagestring = ''
		while(len(colorimagestring)<HEIGHT*WIDTH and time.time() - startframetime < RUNTIME):
			ready = select.select([s], [], [], 0.01)
			if ready[0]:
				data = s.recv(BUFFER_SIZE)
				colorimagestring = colorimagestring + data

		print 'received color image'

		try:
			if len(colorimagestring)==HEIGHT*WIDTH:
				backtoarray = np.fromstring(colorimagestring, dtype=np.uint8).reshape(480,640)
				try:
					centersTuple = GearVision(backtoarray)
				except:
					fuckme = 0
				COLORIMAGEARRAY.append(backtoarray)
				print count
			else:
				print 'fucked up'
		except Exception as ex:
			print ex

		if(centersTuple[0]!=69 and centersTuple[1]!=69):
			angle = getDistanceAngle(sum(centersTuple[0])/len(centersTuple[0]))
			angle = angle + 2
			udps.open()
			udps.sendto(str(angle),("10.23.67.255",udpport))
			udps.close()
			print 'Angle is::::::: ' + str(angle)

		# #THIS FOLLOWING CODE SEGMENT IS FOR DEPTH... but i don't want depth right now....
		# if(centersTuple[0]!=69 and centersTuple[1]!=69 and 11==12):
		# 	s.send('depth image')
		# 	depthimagestring = ''
		# 	while(len(depthimagestring)<HEIGHT*WIDTH*2 and time.time() - startframetime < RUNTIME):
		# 		ready = select.select([s], [], [], 0.01)
		# 		if ready[0]:
		# 			data = s.recv(BUFFER_SIZE)
		# 			depthimagestring = depthimagestring + data
		# 	print 'received depth image...'
		# 	try:
		# 		if len(depthimagestring)==HEIGHT*WIDTH*2:
		# 			nparr = np.fromstring(depthimagestring, dtype=np.uint16) #don't reshape!!
	
		# 			centerX = sum(centersTuple[0])/len(centersTuple[0])
		# 			centerY = sum(centersTuple[1])/len(centersTuple[1])
		# 			print "depth should be " + str(nparr[ (WIDTH * (centerY+50)) + centerX] / 25.4)

		# 			file = open('./depthvalues.txt', 'w')
		# 			file.write(nparr)
		# 			file.close()
		# 			#depth1 = nparr[WIDTH*(centersTuple[1][0]-50) + centersTuple[0][0]]
		# 			#depth2 = nparr[WIDTH*(centersTuple[1][1]-50) + centersTuple[0][1]]
		# 			#print 'Pogace Angle is::::::: ' + str(getAngle(int(depth1),int(depth2)))
		# 			print count
		# 		else:
		# 			print 'fucked up'
		# 	except Exception as ex:
		# 		print ex

except Exception as ex:
	print ex
	
s.send('end')
s.close()
udps.close()



print (time.clock() - start_time)
for i in range(0,len(COLORIMAGEARRAY)):
	cv2.imwrite('/Users/harshayugirase/Desktop/LiveFeed/colorimage' + str(i) + '.bmp', COLORIMAGEARRAY[i])


#for w in range(0,len(DEPTHIMAGEARRAY)):
 #	cv2.imwrite('/Users/harshayugirase/Desktop/LiveFeed/depthimage' + str(w) + '.bmp', DEPTHIMAGEARRAY[w])
 
print
print 'Program done running :D'
