#!/usr/bin/env python
# server.py
 
import socket
import select
import Queue
from threading import Thread
from time import sleep
from random import randint
import sys

def process(value):
    """
    Implement this. Do something useful with the received data.
    """
    if value[0] != "_":
        print(value)
    else:
        if "CONNECT" in value:
            print(value[8:] + " connected!")
        else if "DISCONNECT" in value:
            print(value[11:] + " disconnected!")
    #sleep(randint(1,9))    # emulating processing time
    sleep(1)
def AwaitInput(string,origin):
    print(string)
    thing = str(raw_input())
    if thing != '':
        return str(thing)
    return str(origin)
class ProcessThread(Thread):
    def __init__(self):
        super(ProcessThread, self).__init__()
        self.running = True
        self.q = Queue.Queue()
 
    def add(self, data):
        self.q.put(data)
 
    def stop(self):
        self.running = False
 
    def run(self):
        q = self.q
        while self.running:
            try:
                # block for 1 second only:
                value = q.get(block=True, timeout=1)
                process(value)
            except Queue.Empty:
                sys.stdout.write('.')
                sys.stdout.flush()
        if not q.empty():
            print("Elements left in the queue:")
            while not q.empty():
                print(q.get())

class Server(object):
    def __init__(self):
        self.host = AwaitInput("Enter your ip",'')
        self.t = ProcessThread()
        self.t.start()
        self.s = socket.socket()        # Create a socket object
        self.port = 6119                # Reserve a port for your service.
        self.s.bind((self.host, self.port))        # Bind to the port
        print("Listening on port ... " + str(self.port))
        self.running = True
        self.clients = []
        self.s.listen(5)                 # Now wait for client connection.
    def run(self):
        try:
            client, addr = self.s.accept()
            ready = select.select([client,],[], [],2)
            if ready[0]:
                data = client.recv(4096)
                #print data
                self.t.add(data)
        except KeyboardInterrupt:
            print
            print("Stop.")
            self.running = False
        except socket.error, msg:
            print("Socket error! %s" % msg)
            self.running = False
    def main(self):
        while True:
            if self.running == True:
                self.run()
            else:
                self.cleanup()
        self.cleanup()
    def cleanup(self):
        self.t.stop()
        self.t.join()
 
#########################################################
 
if __name__ == "__main__":
    server = Server()
    server.main()
