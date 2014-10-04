import socket,select,Queue,json
from threading import Thread
from time import sleep
from urllib2 import urlopen
import sys

clients = []

def broadcast(source_socket,message,tosender=False):
    if source_socket != None:
        if tosender == True:
            source_socket.send(message)
        for i in clients:
            if i.conn is not source_socket:
                i.conn.send(message)

def GetIp():
    return json.load(urlopen('http://httpbin.org/ip'))['origin']

def process(data,source_socket):
    """Implement this. Do something useful with the received data."""

    if data[0] == "_":
        if "_CONNECT_" in data:
            print(data[9:] + " connected to the server!")
            broadcast(source_socket,"Welcome to the server " + data[9:] + "!",True)
    else:
        print(data)
        broadcast(source_socket,data,True)
    sleep(1) # emulating processing time
     
class ProcessThread(Thread):
    def __init__(self):
        super(ProcessThread, self).__init__()
        self.running = True
        self.q = Queue.Queue()
        self.client_socket = None
    def add(self, data, conn):
        self.q.put(data)
        self.client_socket = conn
    def stop(self):
        self.running = False
 
    def run(self):
        while self.running:
            try:
                # block for 1 second only:
                value = self.q.get(block=True, timeout=1)
                process(value,self.client_socket)
                self.client_socket = None
            except Queue.Empty:
                pass
                #sys.stdout.write('.')
                #sys.stdout.flush()
t = ProcessThread()
t.start()

class ClientThread(Thread):
    def __init__(self,socket):
        super(ClientThread, self).__init__()
        self.running = True
        self.conn = socket
    def stop(self):
        self.running = False 
    def run(self):
        while self.running:
            try:
                data = self.conn.recv(1024)
                if data:
                    #print data
                    t.add(data,self.conn)
            except socket.error, msg:
                print("Socket error! %s" % msg)
                pass
        self.conn.close()
    
class Server():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Create a socket object
        self.host = GetIp()
        self.port = 6119                 # Reserve a port for your service.
        self.s.bind((self.host, self.port))        # Bind to the port
        print(str(self.host) + " Listening on port : " + str(self.port)+"\r\n")
     
        self.s.listen(5)                 # Now wait for client connection.
    def main(self):  
        while True:
            try:
                conn, addr = self.s.accept()

                thread = ClientThread(conn)
                thread.start()
                clients.append(thread)
                
            except socket.error, msg:
                print("Socket error! %s" % msg)
                pass
        t.stop()
        t.join()
 
#########################################################
if __name__ == "__main__":
    server = Server()
    server.main()
