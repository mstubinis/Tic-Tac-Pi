#!/usr/bin/env python
# client.py

import sys
import socket


class Client(object):
    def __init__(self):
        self.connected = False
        self.client = None
        self.connection_destination = ""
    def connect_to_server(self,server):
        try:
            if self.connected == False:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection_destination = server
                self.client.connect((self.connection_destination, 6119))
                self.client.send("_CONNECT" + socket.gethostname())
                self.connected = True
        except:
            print("Unable to connect to server")
            pass
    def disconnect_from_server(self):
        if self.connected == True:
            self.client.send("_DISCONNECT" + socket.gethostname())
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
            self.connected = False
    def update(self):
        pass
