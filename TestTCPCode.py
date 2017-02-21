import socket
import numpy as np
from cStringIO import StringIO
import cv2

def startServer():
    port=7561
    server_socket=socket.socket() 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so it can be recreated
    server_socket.bind(('',port))
    server_socket.listen(1)
    print 'waiting for a connection...'
    client_connection,client_address=server_socket.accept()
    print 'connected to ',client_address[0]
    ultimate_buffer=''
    while True:
        receiving_buffer = client_connection.recv(1024)
        if not receiving_buffer: break
        ultimate_buffer+= receiving_buffer
        print '-',
    final_image=np.load(StringIO(ultimate_buffer))['frame']
    client_connection.close()
    server_socket.close()
    print '\nframe received'
    cv2.imwrite('/Users/harshayugirase/Desktop/hellyeah!.bmp', final_image)
    print type(final_image)
    print 'program finished running fully!!'


startServer()
