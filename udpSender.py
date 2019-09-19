# Source: https://pymotw.com/2/socket/udp.html

import socket, sys, time
from threading import Thread

host = sys.argv[1]
textport = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)

in_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
in_server_address = ('localhost', port + 1)
in_s.bind(in_server_address)

def listener(s, port):
    while 1:
      buf, address = s.recvfrom(port + 1)
      if len(buf):
         print ("Received %s bytes from %s: %s " % (len(buf), address, buf.decode('utf-8') ))


thread = Thread(target = listener, args = (in_s, port, ))
thread.start()

while 1:
    print ("Enter data to transmit: ENTER to quit")
    data = sys.stdin.readline().strip()
    if not len(data):
        break
#    s.sendall(data.encode('utf-8'))
    for x in range(10):
      s.sendto((data + str(x)).encode('utf-8'), server_address)
    
    
    

s.shutdown(1)

