import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 2772
BUFFER_SIZE = 256

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
  if(dataRequested=='Request to connect.'):
  	conn.send('Yes you can connect')
  if(dataRequested=='Is Nikhil hot?'):
  	conn.send('HELL YEAH... that jawline tho')
  if(dataRequested=='Can you send a file to me?'):
  	conn.send('fhiogpiohiohioewahfi;ohfopewfhiepowahfioepawhfgoaipewfhioaewgpaeowgiechaeiowhfoipehoaepwvioewaheopwahfoeipwahfaepoiwhfeaipgaepwogeiwfiuagdwuiqbcouwbfapewhgfp9wh')


conn.close()