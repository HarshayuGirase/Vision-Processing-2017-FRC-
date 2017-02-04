import socket
import cv2
import numpy as np

TCP_IP = '127.0.0.1'
TCP_PORT = 2724
BUFFER_SIZE = 256
REQUESTEDMESSAGE = 'lol'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

s.send(REQUESTEDMESSAGE)
dataReceivedFromServer = s.recv(BUFFER_SIZE)


print dataReceivedFromServer

s.close()