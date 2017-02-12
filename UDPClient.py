import socket, traceback, time

host = '' # Bind to all interfaces
port = 2599

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

start_time = time.time()
while (time.time() - start_time < 10):
    try:
        message, address = s.recvfrom(8192)
        if(address[0].find('192.168.1.18') == -1):
            print ("Got data from", address)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()