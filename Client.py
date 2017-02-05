import socket

TCP_IP = '192.168.1.12'
TCP_PORT = 2776
BUFFER_SIZE = 256
REQUESTEDMESSAGE = 'Is Nikhil hot?'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'before'
s.connect((TCP_IP, TCP_PORT))
print 'hi'

s.send(REQUESTEDMESSAGE)
dataSentFromServer = s.recv(BUFFER_SIZE)

print dataSentFromServer

s.close()

