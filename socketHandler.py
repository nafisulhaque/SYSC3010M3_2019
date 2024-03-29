# Source: https://pymotw.com/2/socket/udp.html
"""
This file contains the class SocketHandler, which handles both sending and receiving messages through sockets.
One SocketHandler is needed to handle all connections.

Written by Dorian Wang
"""
import socket
import sys
import time
import json
import threading
import select
import logging
import queue

# https://stackoverflow.com/questions/15727420/using-python-logging-in-multiple-modules
if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    try:
        textport = sys.argv[1]
    except:
        textport = 12345
log = logging.getLogger(__name__)


class SocketHandler:
    """
    How to use this object:
    First add listeners to different ports. Then use the run() function to start the listener thread.
    Send data by calling socketsender(). data and host should be strings, port is a int
    To get the data call getinput(). This returns a tuple, the first value is data, the second is the sending address.
    If the input buffer is empty, getinput() will return None.
    """
    # https://stackoverflow.com/questions/15365406/run-class-methods-in-threads-python
    def __init__(self):
        self.run_thread = True
        self.inputbuffer = queue.Queue()
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
        server_address = ('', port)
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
            self.listeners.remove(listener)
        listenerslock.release()

    def socketlistener(self):
        """
        This function is run by a thread and places all data into the input buffer.
        It hopefully doesn't really need to be threaded but I did so anyways. \o.o/
        """
        while self.run_thread:
            self.listenerslock.acquire()
            templisteners = [listener[1] for listener in self.listeners]
            ready_to_read, ready_to_write, in_error = \
                select.select(templisteners, [], [], 10.0)  # 10 second timeout, should work
            for s in ready_to_read:
                buf, address = s.recvfrom(8192)

                self.inputbufferlock.acquire()
                self.inputbuffer.put_nowait((buf, address))
                log.info("Received %s bytes from %s: " % (len(buf), address))
                self.inputbufferlock.release()

            self.listenerslock.release()
            time.sleep(0.1)

    def socketsender(self, host, port, data):
        port = int(port)
        if port < 1 or port > 65535:
            log.error("port number out of range in socketsender")
            return None
        port = int(port)
        target_address = (host, port)
        print(target_address)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s.bind(target_address)

        if not len(data):
            s.shutdown(1)
            return None

        print(s.sendto(data.encode('utf-8'), target_address))
        s.shutdown(1)
        return not None

    def getinput(self):
        if self.inputbuffer.empty():
            return None

        self.inputbufferlock.acquire()
        value = self.inputbuffer.get_nowait()
        self.inputbufferlock.release()

        return value

    def run(self):
        t = threading.Thread(target=self.socketlistener)
        t.start()













