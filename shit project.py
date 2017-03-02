import socket
import cv2
import numpy as np
import sys
import time
import select

TCP_IP = '192.168.1.103'
TCP_PORT = 6789
BUFFER_SIZE = 1500

print 'Trying to connect...'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so it can be recreated
s.connect((TCP_IP, TCP_PORT))

s.send('nilay pachauri is such a babe lol <3')

s.close()