import socket, traceback, time

SERVER_IP = ''

host = '' # Bind to all interfaces
port = 7321

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

start_time = time.time()
while (time.time() - start_time < 10):
    try:
        message, address = s.recvfrom(8192)
        if(message=='SFHS Server FUCK254'):
        	SERVER_IP = address[0]
        	print 'Got SFHS Server IP Address'
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()

print SERVER_IP