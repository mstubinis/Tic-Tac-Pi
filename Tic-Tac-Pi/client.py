import sys, socket,thread,select,pygame
from time import sleep

def GetIp():
    import json
    from urllib2 import urlopen
    ip = json.load(urlopen('http://httpbin.org/ip'))['origin']
    return ip

class Client(object):
    def __init__(self):
        self.ip = GetIp()
        self.timer = 0
        self.client = None
        self.connected = False
        self.connection_destination = ""
    def connect_to_server(self,errorButton,server):
        try:
            if self.connected == False:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection_destination = server
                self.client.connect((self.connection_destination, 6119))
                self.client.sendall("_CONNECT" + socket.gethostname())
                self.print_response(errorButton)
                self.connected = True
            else:
                error = "Already connected to a server!"
                errorButton.update_message(error)
        except:
            pass
    def disconnect_from_server(self,error=False):
        if error == False:
            self.client.sendall("_DISCONNECT" + socket.gethostname())
        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()
        self.connected = False

    def send_message(self,message,errorButton):
        if self.client != None:
            self.client.sendall(message)
            self.print_response(errorButton)
        
    def print_response(self,errorButton):
        try:
            data = self.client.recv(4096)
            print(data)
        except:
            error = "Server was shut down"
            errorButton.update_message(error)
            self.disconnect_from_server(True)
            pass
        
    def update(self,errorButton):
        self.timer += 1
        if self.timer > 50:
            self.send_message(".",errorButton)
            self.timer = 0
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                try:
                    self.send_message("hi",errorButton)
                except:
                    pass
