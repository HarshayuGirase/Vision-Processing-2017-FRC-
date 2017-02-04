import socket
import cv2

TCP_IP = '127.0.0.1'
TCP_PORT = 2724
BUFFER_SIZE = 256


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates the socket
s.bind((TCP_IP, TCP_PORT)) #binds the socket to certain address using IP and Port#
s.listen(1) #look out for 1 connection

conn, addr = s.accept()

while True:
  dataRequested = conn.recv()
  if(dataRequested=='Request to connect.'):
  	conn.send('Yes you can connect')
  if(dataRequested=='Is Nikhil hot?'):
  	conn.send('HELL YEAH... that jawline tho')
  if(dataRequested=='lol'):
  	conn.send('lol')



conn.close()