import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 2797
BUFFER_SIZE = 9999
print TCP_IP 
print 'lol'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates the socket
print 'socket created'
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so it can be recreated
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
