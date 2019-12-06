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
ARDUINO = "192.168.1.1"

sh = socketHandler.SocketHandler()
sh.__init__()
sh.addlistener(RECV_PORT)
sh.run()

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
        sh.socketsender(ARDUINO, SEND_PORT, a[0])
    else:
        sh.socketsender(a[1], SEND_PORT, value)



