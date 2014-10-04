import sys, socket,thread,select,pygame,json,Queue
from urllib2 import urlopen
from time import sleep
from threading import Thread

def GetIp():
    return json.load(urlopen('http://httpbin.org/ip'))['origin']

class ClientThreadSend(Thread):
    def __init__(self,socket):
        super(ClientThreadSend, self).__init__()
        self.running = True
        self.conn = socket
        self.q = Queue.Queue()
    def add(self,data):
        self.q.put(data)
    def stop(self):
        self.conn.shutdown(socket.SHUT_RDWR)
        self.conn.close()
        self.running = False 
    def run(self):
        while self.running:
            try:
                if not self.q.empty():
                    message = self.q.get(block=True, timeout=1)
                    self.conn.send(message)
            except socket.error, msg:
                print("Socket error! %s" % msg)
                pass
        self.conn.close()
class ClientThreadRecieve(Thread):
    def __init__(self,socket):
        super(ClientThreadRecieve, self).__init__()
        self.running = True
        self.conn = socket

    def stop(self):
        self.conn.shutdown(socket.SHUT_RDWR)
        self.conn.close()
        self.running = False 
    def run(self):
        while self.running:
            try:
                data = self.conn.recv(1024)
                print(data)
            except socket.error, msg:
                print("Socket error! %s" % msg)
                pass
        self.conn.close()
        
class Client(object):
    def __init__(self):
        self.ip = GetIp()
        self.client = None
        self.client1 = None
        self.connected = False
        self.connection_destination = ""
        self.username = ""
    def connect_to_server(self,errorButton,server,username):
        if username == "":
            error = "Please enter your name"
            errorButton.update_message(error)
            return
        if server == "":
            error = "Please enter the server ip"
            errorButton.update_message(error)
            return
        try:
            if self.connected == False:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection_destination = server
                self.username = username

                client_socket.connect((self.connection_destination, 6119))
                
                self.client = ClientThreadSend(client_socket)
                self.client.start()

                self.client1 = ClientThreadRecieve(client_socket)
                self.client1.start()
                
                self.send_message("_CONNECT_" + self.username,errorButton)
                
                self.connected = True
            else:
                error = "Already connected to a server!"
                errorButton.update_message(error)
        except:
            pass
    def disconnect_from_server(self,errorButton,error=False):
        if error == False:
            self.send_message("_DISCONNECT_" + self.username,errorButton)
            
        self.client.stop()
        self.client1.stop()
        self.connected = False

    def send_message(self,message,errorButton):
        if self.client != None:       
            self.client.add(message)
      
    def update(self,errorButton,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                try:
                    self.send_message(self.username,errorButton)
                except:
                    pass
