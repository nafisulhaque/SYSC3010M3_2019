# Source: https://pymotw.com/2/socket/udp.html

import socket
import sys
import time
import json
import threading
import select
import logging

# https://stackoverflow.com/questions/15727420/using-python-logging-in-multiple-modules
if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    try:
        textport = sys.argv[1]
    except:
        textport = 12345
log = logging.getLogger(__name__)


class SocketHandler:
    # https://stackoverflow.com/questions/15365406/run-class-methods-in-threads-python
    def __init__(self):
        self.inputbuffer = []
        self.inputbufferlock = threading.Lock()
        self.listeners = []
        self.listenerslock = threading.Lock()

        self.outputbuffer = []
        self.outputbufferlock = threading.Lock()

    def addlistener(self, port):
        if len(self.listeners) > 0:
            tempports = [listener[0] == port for listener in self.listeners]
            print(tempports)
            if True in tempports:
                return False
        newsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('localhost', port)
        newsocket.bind(server_address)
        newsocket.setblocking(0)
        newlistener = (port, newsocket)

        self.listenerslock.acquire()
        self.listeners.append(newlistener)
        self.listenerslock.release()
        return True

    def removelistener(self, port):
        """
        This function removes a listener from the list. If there is no port attached, nothing happens
        :param port: the port the listener is attached to
        :return: No return
        """
        listenerslock.acquire()
        if (listener[0] == port for listener in self.listeners):
            listener[1].shutdown()
            del listener
        listenerslock.release()

    def socketlistener(self):
        """
        This function is run by a thread and places all data into the input buffer.
        It hopefully doesn't really need to be threaded but I did so anyways. \o.o/
        """
        self.listenerslock.acquire()
        templisteners = [listener[1] for listener in self.listeners]
        print(templisteners)
        ready_to_read, ready_to_write, in_error = \
            select.select(templisteners, [], [], 30.0)  # 30 second timeout, should work
        for s in ready_to_read:
            buf, address = s.recvfrom(port)
            
            self.inputbufferlock.acquire()
            inputbuffer.append((buf, address))
            self.inputbufferlock.release()

        self.listenerslock.release()

        buf, address = s.recvfrom(port)

        #print ("Received %s bytes from %s %s: " % (len(buf), address, buf ))
        #print (buf.decode('utf-8'))
        print("Received %s bytes from %s %s: " % (len(buf), address, json.loads(buf.decode('utf-8'))))
        x = json.loads(buf.decode('utf-8'))
        # x = json.loads(x)
        print(type(x))
        print(x)

    def socketsender(self, host, port, data):
        port = int(port)
        if port < 1 or port > 65535:
            log.error("port number out of range in socketsender")
            return None
        port = int(port)
        target_address = (host, port)
        print(target_address)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(target_address)

        if not len(data):
            s.shutdown(1)
            return None

        print(s.sendto(data.encode('utf-8'), target_address))
        s.shutdown(1)
        return not None

    def run(self):
        t = threading.Thread(target=self.socketlistener)
        t.start()


a = SocketHandler()
#assert a.addlistener(1234)
assert a.addlistener(int(textport) + 1)
print(a.listeners)
#a.run()
print(a.inputbuffer)
while True:
    a.socketsender('localhost', textport, "Testtest")
    time.sleep(1)
    print(a.inputbuffer)










