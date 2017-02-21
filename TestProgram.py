import cv2
import numpy as np
import sys
import time



depthMat = cv2.imread('./Boiler1.png', cv2.IMREAD_UNCHANGED) #mat with all depth values associated for each pixel value


ndata = np.frombuffer(depthMat, np.int16)
ndatastring = ndata.tostring()

print len(ndatastring)
backtoarray = np.fromstring(ndatastring, np.int16).reshape(480, 640)

