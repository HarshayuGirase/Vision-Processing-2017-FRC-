import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 2713
BUFFER_SIZE = 256
REQUESTEDMESSAGE = 'Is Nikhil hot?'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

s.send(REQUESTEDMESSAGE)
dataSentFromServer = s.recv(BUFFER_SIZE)

print dataSentFromServer

s.close()