#!/usr/bin/env python
# server.py
 
import socket,sys,select
from threading import Thread
from time import sleep

def GetIp():
    import json
    from urllib2 import urlopen
    ip = json.load(urlopen('http://httpbin.org/ip'))['origin']
    return ip

def process(value):
    if value[0] != "_":
        print(value)
    else:
        if "CONNECT" in value:
            print(value[8:] + " connected!")
        elif "DISCONNECT" in value:
            print(value[11:] + " disconnected!")
    sleep(1)
    
class ClientInfo(object):
    def __init__(self,client,name,ip):
        self.name = name
        self.ip = ip[0]
        self.connected = True
        self.client_socket = client
        self.respond("I recieved your connection, " + str(self.ip))
    def print_info(self):
        print("Name: " + self.name + " , IP: " + self.ip + " , Connected: " + str(self.connected) + "\r\n")

    def respond(self,message):
        self.client_socket.send(str(message))
        
class Server(object):
    def __init__(self):
        self.clients = []
        
        self.host = GetIp()
        self.s = socket.socket()            # Create a socket object
        self.port = 6119                    # Reserve a port for your service.
        self.s.bind((self.host, self.port)) # Bind to the port
        print("Hosting on IP: " + str(self.host) + "\r\nListening on port: " + str(self.port)+ "\r\n")
        self.running = True
        self.s.listen(5)                 # Now wait for client connection.

    def add_client(self,client,addr,data):
        for i in self.clients:
            if i.ip == addr[0]:
                return False
        self.clients.append(ClientInfo(client,"",addr))
            
    def run(self):
        try:
            client, addr = self.s.accept()
            ready = select.select([client,],[], [],2)
            if ready[0]:
                data = client.recv(4096)
                process(data)#print data
                
            self.add_client(client,addr,data)
                                    
        except socket.error, msg:
            print("Socket error: " + str(msg))
            self.running = False
            
    def main(self):
        while True:
            if self.running == True:
                self.run()
            else:
                sys.exit(1)
        sys.exit(1)

if __name__ == "__main__":
    server = Server()
    server.main()
