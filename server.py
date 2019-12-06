"""
This file handles all server functions.

This file should be run on the server. It uses databaseManager and socketHandler.
The ip address of the arduino controller may be provided to relay packets to.


Written by Dorian Wang
"""
import databaseManager
import socketHandler
import sys
import time
import datetime
import logging

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

RECV_PORT = 1001
SEND_PORT = 1002
try:
    ARDUINO = sys.argv[0]
except IndexError:
    ARDUINO = "192.168.1.1"

# socketHandler setup
sh = socketHandler.SocketHandler()
sh.__init__()
sh.addlistener(RECV_PORT)  # one listener now, more can be added later
sh.run()  # start listeners

#
while True:
    time.sleep(0.2)
    a = sh.getinput()
    if a is None:
        continue
    a[0] = str(a[0])
    try:
        value = databaseManager.parsejsonintocommand(a[0])
        if value is not None:
            value = json.dumps(value)
    except:
        log.error("json could not be parsed")

    if value is None:
        try:
            sh.socketsender(ARDUINO, SEND_PORT, a[0])
        except:
            log.error("Could not pass to ARDUINO")
            pass
            # normally can't happen
    else:
        sh.socketsender(a[1], SEND_PORT, value)



