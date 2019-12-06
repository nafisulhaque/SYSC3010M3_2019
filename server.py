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

sh = socketHandler.SocketHandler()
sh.__init__()
sh.addlistener(RECV_PORT)
sh.run()

while True:
    a = sh.getinput()
    if a is None:
        continue
    a[0] = str(a[0])
    try:
        value = databaseManager.parsejsonintocommand(a)
    except:
        log.error("json could not be parsed")

    sh.socketsender(address, SEND_PORT, value)



