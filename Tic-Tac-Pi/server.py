import socket,select,Queue,json,resourceManager,random
from threading import Thread
from time import sleep
from urllib2 import urlopen
import sys

def GetIp():
    return json.load(urlopen('http://httpbin.org/ip'))['origin']

def removekey(dictionary, key):
    r = dict(dictionary)
    del r[key]
    return r

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
                value = self.q.get(block=True, timeout=0.3)
                self.server.broadcast(value,None)
                    
class ProcessThread(Thread):
    def __init__(self,server):
        super(ProcessThread, self).__init__()
        self.running = True
        self.q = Queue.Queue()
        self.client_thread = None
        self.server = server
    def add(self, data, clientThread):
        self.q.put(data)
        self.client_thread = clientThread
    def stop(self):
        self.running = False
    def run(self):
        while self.running:
            if not self.q.empty():
                value = self.q.get(block=True, timeout=0.3)
                self.server.process(value,self.client_thread)
                self.client_thread = None

class ClientThread(Thread):
    def __init__(self,server,socket,address):
        super(ClientThread, self).__init__()
        self.running = True
        self.conn = socket
        self.username = address
        self.address = address
        self.server = server
    def stop(self):
        self.running = False 
    def run(self):
        while self.running:
            try:
                data = self.conn.recv(1024)
                if data:
                    self.server.process_thread.add(data,self)
            except socket.error as msg:
                print("Socket error!: " + str(msg))
                self.running = False
                self.stop()
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

        self.clients = {}

    def broadcast(self,message,source_socket=None,tosender=False):
        if tosender == True and source_socket != None:
            source_socket.send(message)
        for key,value in self.clients.iteritems():
            if value.conn is not source_socket:
                value.conn.send(message)
                
    def process(self,data,client_thread):
        print(data)
        if data[0] == "_":
            if "_CONNECT_" in data:        
                address_copy = client_thread.address
                client_thread.username = str(data[9:])
                self.clients[str(data[9:])] = client_thread
                self.clients = removekey(self.clients,address_copy)

                message = "\nConnected Clients: ["
                for key,value in self.clients.iteritems():
                    message += str(key)+","
                message = message[:-1]
                message += "]\n"
                print(message)
            elif "_GETCLIENTS_" in data:
                message = ""
                for key,value in self.clients.iteritems():
                    message += str(key)+"_"
                message = message[:-1]
                self.reply_thread.add("_SENDCLIENTS_"+message)
            elif "_STARTMATCH_" in data:
                index = random.randint(0,1)
                self.reply_thread.add("_STARTMATCH_"+str(index))
            elif "_SENDBOARDINFO_" in data:
                self.reply_thread.add("_RECVBOARDINFO_" + data[15:])
        else:
            self.reply_thread.add(data)
        sleep(0.3) # emulating processing time
        
    def main(self):  
        while True:
            try:
                conn, address = self.s.accept()

                thread = ClientThread(self,conn,address[0])
                thread.start()
                self.clients[address[0]] = thread
                
            except socket.error as msg:
                print("Socket error!: " + str(msg))
                pass

            #clean up any innactive threads
            for key,value in self.clients.iteritems():
                if value.running == False:
                    self.clients = removekey(self.clients,key)
            
        self.process_thread.stop()
        self.process_thread.join()
        self.reply_thread.stop()
        self.reply_thread.join()
 
#########################################################
if __name__ == "__main__":
    server = Server()
    server.main()
