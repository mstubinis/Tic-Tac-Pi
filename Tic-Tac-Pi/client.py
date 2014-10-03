#!/usr/bin/env python
# client.py
import sys, socket

class Client(object):
    def __init__(self):
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
        except:
            error = "Unable to connect to server"
            errorButton.update_message(error)
            pass
    def disconnect_from_server(self,error=False):
        if error == False:
            self.client.send("_DISCONNECT" + socket.gethostname())
        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()
        self.connected = False

    def send_message(self,message,errorButton):
        self.client.connect((self.connection_destination, 6119))
        self.client.sendall(message)
        self.print_response(errorButton)
        
    def print_response(self,errorButton):
        try:
            data = self.client.recv(4096)
            print("Received response: " + str(data))
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
        except:
            error = "Server was shut down"
            errorButton.update_message(error)
            self.disconnect_from_server(True)
            pass
        
    def update(self,errorButton):
        pass
