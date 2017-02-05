# import json
# import cv2
# import numpy as np
# import sys
# import time
# import cPickle



# img = cv2.imread('./Hopper1.bmp') #image read

# start = time.time()
# width = len(img[0])
# height = sum([len(arr) for arr in img])/width
# region1 = img[5*height/16:14*height/16, 0:width]

# img_str = cv2.imencode('.bmp', region1)[1].tostring()

# nparr = np.fromstring(img_str, np.uint8)
# img2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
# print (time.time() - start)

