import socket,select,Queue,json
from threading import Thread
from time import sleep
from urllib2 import urlopen
import sys

def GetIp():
    return json.load(urlopen('http://httpbin.org/ip'))['origin']


class ReplyThread(Thread):
    def __init__(self,server):
        super(ReplyThread, self).__init__()
        self.running = True
        self.q = Queue.Queue()
        self.server = server
    def add(self, data):
        self.q.put(data)
    def stop(self):
        self.running = False
    def run(self):
        while self.running:
            if not self.q.empty():
                value = self.q.get(block=True, timeout=1)
                self.server.broadcast(value,None)
                    
class ProcessThread(Thread):
    def __init__(self,server):
        super(ProcessThread, self).__init__()
        self.running = True
        self.q = Queue.Queue()
        self.client_socket = None
        self.server = server
    def add(self, data, conn):
        self.q.put(data)
        self.client_socket = conn
    def stop(self):
        self.running = False
    def run(self):
        while self.running:
            if not self.q.empty():
                value = self.q.get(block=True, timeout=1)
                self.server.process(value,self.client_socket)
                self.client_socket = None

class ClientThread(Thread):
    def __init__(self,server,socket):
        super(ClientThread, self).__init__()
        self.running = True
        self.conn = socket
        self.server = server
    def stop(self):
        self.running = False 
    def run(self):
        while self.running:
            try:
                data = self.conn.recv(1024)
                if data:
                    self.server.process_thread.add(data,self.conn)
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


        self.process_thread = ProcessThread(self)
        self.reply_thread = ReplyThread(self)
        self.process_thread.start()
        self.reply_thread.start()
        
        self.s.listen(5)                 # Now wait for client connection.

        self.clients = []

    def broadcast(self,message,source_socket=None,tosender=False):
        if tosender == True and source_socket != None:
            source_socket.send(message)
        for i in self.clients:
            if i.conn is not source_socket:
                i.conn.send(message)
                
    def process(self,data,source_socket):
        if data[0] == "_":
            if "_CONNECT_" in data:
                print(data[9:] + " connected to the server!")
                self.reply_thread.add("Welcome to the server " + data[9:] + "!")
        else:
            print(data)
            self.reply_thread.add(data)
        sleep(1) # emulating processing time
        
    def main(self):  
        while True:
            try:
                conn, addr = self.s.accept()

                thread = ClientThread(self,conn)
                thread.start()
                self.clients.append(thread)
                
            except socket.error, msg:
                print("Socket error! %s" % msg)
                pass
        self.process_thread.stop()
        self.process_thread.join()
        self.reply_thread.stop()
        self.reply_thread.join()
 
#########################################################
if __name__ == "__main__":
    server = Server()
    server.main()
