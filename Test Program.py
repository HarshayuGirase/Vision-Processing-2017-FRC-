import json
import cv2
import numpy as np
import sys

img = cv2.imread('./Boiler1.bmp') #image read
img_str = cv2.imencode('.bmp', img)[1].tostring()


nparr = np.fromstring(img_str, np.uint8)
img2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

print img2