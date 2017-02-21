import socket
import numpy as np
from cStringIO import StringIO
import cv2

def startClient(server_address,image):
    if not isinstance(image,np.ndarray):
        print 'not a valid numpy image' 
        return
    client_socket=socket.socket()
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #so it can be recreated
    port=7560
    try:
        client_socket.connect((server_address, port))
        print 'Connected to %s on port %s' % (server_address, port)
    except socket.error,e:
        print 'Connection to %s on port %s failed: %s' % (server_address, port, e)
        return

    f = StringIO()
    np.savez_compressed(f,frame=image)
    f.seek(0)
    out = f.read()
    client_socket.sendall(out)
    client_socket.shutdown(1)
    client_socket.close()
    print 'image sent'

    

depthMat = cv2.imread('/Users/harshayugirase/Desktop/output.bmp', cv2.IMREAD_UNCHANGED)
startClient('127.0.0.1', depthMat)