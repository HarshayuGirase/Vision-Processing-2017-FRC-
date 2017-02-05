# import json
# import cv2
# import numpy as np
# import sys
# import time



# img = cv2.imread('./Hopper1.bmp') #image read

# start = time.time()
# width = len(img[0])
# height = sum([len(arr) for arr in img])/width
# region1 = img[5*height/16:14*height/16, 0:width]

# img_str = cv2.imencode('.bmp', region1)[1].tostring()

# nparr = np.fromstring(img_str, np.uint8)
# img2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
# print (time.time() - start)

import socket
import select
import sys
import time
import atexit
from Queue import Queue
from threading import Thread
 
#network related variables
PORT = 2380 # Game host port
BROADCAST_PORT = 472 # Broadcast port
BROADCAST_IP = '' 
LOCAL_IP = ''

#timouts for respective interval timers
KEEP_ALIVE_TIMEOUT = 2
NAME_BROADCAST_TIMEOUT = 1

#thread communication queues
broadcastQueue = Queue()
networkRealTimeQueue = Queue()
networkQueue = Queue()

#change this to the relevant team name when the script is loaded to the yun
ROBOT_NAME = "ChangeThisToTheTeamName"


#loging wrapper function    
def logWrite(strng):
	log.write("[" + str(time.time()) + "]" +strng +"\n")
	print strng
	
#Error log file, overwtite file from last reset
logFile = "./elog_" + str(time.time()) + ".txt"
try:
	log = open(logFile, "w")
except Exception as f:
	print "Uhhh... check that your hard drive isn't on fire!"   
	sys.exit(1)
else:
	logWrite("log File" + logFile)

    
#threaded function that listens for broadcasts from host.
def broadcastListener():
        
	bCastSock =socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	bCastSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	bCastSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	try:
		bCastSock.bind((BROADCAST_IP, BROADCAST_PORT))
	except socket.error as msg:
		bCastSock.close()
		logWrite('Broadcast bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1] +"\n")
		sys.exit(1)
			
	lastKeepAlive = time.time()
	while True:   
		readReady = select.select([bCastSock], [], [], 0.02)
		if readReady[0]: 
			data, sender =  bCastSock.recvfrom(1500) 
            #check that the datagram is a alive packet
			if data == sender[0]:
				lastKeepAlive = time.time()
				broadcastQueue.put(sender)
		time.sleep(.05)
        
#serial communication thread
def serialComthread():
	print ''
			
def networkComThread():
	#create socket to recieve from host
	netSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	netSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		netSock.bind((LOCAL_IP, PORT))
	except socket.error as msg:
		logWrite('Broadcast bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
		sys.exit(1)
	
	#main thead loop
	while True:
		#wait for data from broadcast listener thread
		logWrite("Waiting for host.")
		host = broadcastQueue.get(True)
		
		#run loop while we continue to get broadcast packets from the host
		fKeepAlive = True
		keepAliveTimer = time.time()
		nameBroadcastTimer = time.time()
		logWrite("Found Host.")
		while fKeepAlive:
			if not broadcastQueue.empty():
				while not broadcastQueue.empty():
					qPop = broadcastQueue.get()
				keepAliveTimer = time.time() 
			#if we haven't recieved a keep alive packet in a while kill the connection
			if time.time() - keepAliveTimer > KEEP_ALIVE_TIMEOUT:
				fKeepAlive = False
				logWrite("Connection Died due to timeout")
				break
				
			#check for data from host and pass it to the serial thread
			ready = select.select([netSock], [], [], 0.005)
			if ready[0]:
				bridgeData, senderAddr = netSock.recvfrom(1024)
				if bridgeData:
					if senderAddr[0] == host[0]:
						print 'hi'		
			#check serial queue and pass to the host if data is available
			if not networkQueue.empty():
				print 'fml'	
			
			#broadcast name on interval
			if time.time() - nameBroadcastTimer > NAME_BROADCAST_TIMEOUT:
				nameBroadcastTimer = time.time()
				netSock.sendto('ROB:' + ROBOT_NAME,(host[0], PORT))
				logWrite("Sent robot name.")
				
#cleanup function
def cleanup():
	logWrite('cleanup')
	
#Main program start
broadcastThread = Thread(target=broadcastListener, args=())
networkThread = Thread(target=networkComThread, args=())


broadcastThread.start()
networkThread.start()

atexit.register(cleanup)

while True:
	if not broadcastThread.isAlive():
		broadcastThread.run()
		logWrite("Restarting broadcast listener thread")
	if not networkThread.isAlive():
		networkThread.run()
		logWrite("Restarting network thread")
		
	time.sleep(1)