# Source: https://pymotw.com/2/socket/udp.html

import socket
import sys
import time
import json
import threading
import select

# https://stackoverflow.com/questions/15727420/using-python-logging-in-multiple-modules
if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    textport = sys.argv[1]
log = logging.getLogger(__name__)

a = threading.Lock()



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
        if (listener[0] == port for listener in self.listeners):
            return False
        newsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('localhost', port)
        newsocket.bind(server_address)
        newsocket.setblocking(0)
        newlistener = (port, newsocket)

        self.listenerslock.aquire()
        self.listeners.append(newlistener)
        self.listenerslock.release()
        return True

    def removelistener(self, port):
        """
        This function removes a listener from the list. If there is no port attached, nothing happens
        :param port: the port the listener is attached to
        :return: No return
        """
        listenerslock.aquire()
        if (listener[0] == port for listener in self.listeners):
            listener[1].shutdown()
            del listener
        listenerslock.release()

    def socketlistener(self):
        """
        This function is run by a thread and places all data into the input buffer.
        It hopefully doesn't really need to be threaded but I did so anyways. \o.o/
        """
        self.listenerslock.aquire()
        ready_to_read, ready_to_write, in_error = \
            select.select([listener[1] for listener in self.listeners], [], [], 30.0)  # 30 second timeout, should work
        for s in ready_to_read:
            buf, address = s.recvfrom(port)
            
            self.inputbufferlock.acquire()
            inputbuffer.append((buf, address))
            self.inputbufferlock.release()

        self.listenerslock.release()

        buf, address = s.recvfrom(port)

        #print ("Received %s bytes from %s %s: " % (len(buf), address, buf ))
        #print (buf.decode('utf-8'))
        print("Received %s bytes from %s %s: " % (len(buf), address,json.loads(buf.decode('utf-8'))))
        ready_to_read, ready_to_write, in_error = \
            select.select(
                potential_readers,
                potential_writers,
                potential_errs,
                timeout)
        x = json.loads(buf.decode('utf-8'))
        #x = json.loads(x)
        print(type(x))
        print(x)

    def run(self):
        t = threading.Thread(target=self.socketlistener, )

    
    i = i - 1
s.shutdown(1)