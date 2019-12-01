# Source: https://pymotw.com/2/socket/udp.html

import socket
import sys
import time
import json


if __name__ == "__main__":
    host = sys.argv[1]
    textport = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def sendJSON(socket, hostname, port, inputdict):
    port = int(port)
    server_address = (hostname, port)
    if isinstance(inputdict, dict) is not True:
        return None
    # print ("Enter data to transmit: ENTER to quit")
    data = json.dumps(inputdict).strip()
    if not len(data):
        return None
    socket.sendto(data.encode('utf-8'), server_address)
    # s.sendto(struct.pack("i", data), server_address)


s.shutdown(1)

