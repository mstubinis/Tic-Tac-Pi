import socket,sys,select,thread
from time import sleep

def GetIp():
    import json
    from urllib2 import urlopen
    ip = json.load(urlopen('http://httpbin.org/ip'))['origin']
    return ip

def process(conn,data):
    if not data:
        return
    if data[0] == "_":
        if "_CONNECT" in data:
            print(data[8:] + " connected!")
            respond(conn,"I got your connection, " + data[8:])
        elif "_DISCONNECT" in data:
            print(data[11:] + " disconnected!")
    else:
        if data != ".":
            print(data)
            respond(conn,data)

def respond(conn,data):
    if not data:
        return
    try:
        conn.sendall(data)
    except:#client disconnect
        pass

def client_thread(conn):
    while True:
        try:
            data = conn.recv(2048)
            process(conn,data)
        except:#client disconnect
            pass

class Server(object):
    def __init__(self):
        self.host = GetIp()
        self.port = 6119
        self.s = socket.socket()
        self.s.bind((self.host, self.port))
        print("Hosting on IP: " + str(self.host) + "\r\nListening on port: " + str(self.port)+ "\r\n")
        self.s.listen(5)

        self.clients = {}
        self.clients[self.host] = self.s
        
    def send_message(self,client,conn,message):
        conn.sendall(conn.getpeername()[0] + ": " + message)
        
    def main(self):
        while True:
            inputReady, outputReady, exceptReady = select.select(self.clients.values(), [], [])
            for x in inputReady:
                if x != None:
                    if x == self.s:
                        try:
                            csock, addr = self.s.accept()
                            self.clients[addr[0]] = csock
                        except socket.error, msg:
                            print("Socket error: " + str(msg))
                            pass

                    else:  
                        data = x.recv(4096)
                        if data:
                            if not "." in data:
                                print(data)
                            for key,value in self.clients.iteritems():
                                if value is not self.s:
                                    if value != None:
                                        self.send_message(key,value,data)
                    #try:
                        #conn, addr = self.s.accept()
                        #if not addr[0] in self.clients:
                            #self.clients[addr[0]] = thread.start_new_thread(client_thread ,(conn,))                    
                    #except socket.error, msg:
                        #print("Socket error: " + str(msg))
                        #pass
        sys.exit(1)

if __name__ == "__main__":
    server = Server()
    server.main()
