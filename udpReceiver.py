# Source: https://pymotw.com/2/socket/udp.html

import socket, sys, time
from threading import Thread





textport = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = ('localhost', port)
s.bind(server_address)

while True:

    print ("Waiting to receive on port %d : press Ctrl-C or Ctrl-Break to stop " % port)

    buf, address = s.recvfrom(port)
    if not len(buf):
        break
    print ("Received %s bytes from %s %s: " % (len(buf), address, buf ))
    data = buf.decode("utf-8")
    data = "ACK:" + data
    out_port = port + 1
    
    out, stuff = address
    
    out_server_address = (out, port + 1)
    print (out_server_address)
    s.sendto(data.encode('utf-8'), out_server_address)
    print("I have sent %s to %s!" % (data, address ))

s.shutdown(1)
