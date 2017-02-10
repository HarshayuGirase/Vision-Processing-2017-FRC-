import socket
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 2102
BUFFER_SIZE = 500
print TCP_IP 
print 'lol'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates the socket
print 'socket created'
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so it can be recreated
s.bind((TCP_IP, TCP_PORT)) #binds the socket to certain address using IP and Port#
print 'socket bind'


prog_start = time.time()
while (time.time() - prog_start  < 30):
    s.listen(1) #look out for 1 connection
    print 'socket listen'
    conn, addr = s.accept()
    print 'connection accepted'
    
    time_start = time.time()
    recvCount = 0
    while (time.time() - time_start < 30):
      dataRequested = conn.recv(BUFFER_SIZE)
      recvCount = recvCount + 1
      conn.send(dataRequested)

    conn.close()
    print 'conn closed'
print 'exit'