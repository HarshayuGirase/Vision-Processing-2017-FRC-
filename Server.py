import socket

TCP_IP = socket.gethostname()
TCP_PORT = 2774
BUFFER_SIZE = 256
print TCP_IP 
print 'lol'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates the socket
print 'socket created'
s.bind((TCP_IP, TCP_PORT)) #binds the socket to certain address using IP and Port#
print 'socket bind'
s.listen(1) #look out for 1 connection
print 'socket listen'

conn, addr = s.accept()
print 'connection accepted'

while True:
  dataRequested = conn.recv(BUFFER_SIZE)
  conn.send(dataRequested)


conn.close()
