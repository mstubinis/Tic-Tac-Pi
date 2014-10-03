import socket,sys,select,thread
from time import sleep

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def GetIp():
    import json
    from urllib2 import urlopen
    ip = json.load(urlopen('http://httpbin.org/ip'))['origin']
    return ip

class WaitingClient():
    def __init__(self,conn,addr):
        self.conn = conn
        self.addr = addr
        
class Server(object):
    def __init__(self):
        self.host = GetIp()
        self.port = 6119
        self.s = socket.socket()
        self.s.bind((self.host, self.port))
        print("Hosting on IP: " + str(self.host) + "\r\nListening on port: " + str(self.port)+ "\r\n")
        self.s.listen(5)

        self.waiting_clients = []
        self.clients = {}
        self.clients[self.host] = self.s

    def process(self,data,conn):
        if not data:
            return
        if data[0] == "_":

            if len(self.waiting_clients) > 0:
                for i in self.waiting_clients:
                    if i == conn.getpeername()[0]:
                        self.clients = removekey(self.clients,i)
                        self.clients[data[9:]] = conn
                        self.waiting_clients.remove(i)
            
            if "_CONNECT_" in data:
                print(data[9:] + " connected!")               
            elif "_DISCONNECT_" in data:
                print(data[12:] + " disconnected!")
        else:
            print(data)
        sleep(0.2)
        
    def send_message(self,username,client_socket,data):
        #client_socket.sendall(username + ": " + data)
        client_socket.sendall(data)
        sleep(0.2)
        
    def main(self):
        while True:
            inputReady, outputReady, exceptReady = select.select(self.clients.values(), [], [])
            for x in inputReady:
                if x != None:
                    if x == self.s:
                        try:
                            conn, addr = self.s.accept()
                            self.clients[addr[0]] = conn
                            self.waiting_clients.append(addr[0])
                            #self.clients[addr[0]] = thread.start_new_thread(client_thread ,(conn,)) 
                        except socket.error, msg:
                            print("Socket error: " + str(msg))
                            pass

                    else:  
                        data = x.recv(1024)
                        if data:
                            if not "." in data:
                                self.process(data,x)
                            for username,client_socket in self.clients.iteritems():
                                if client_socket != None and client_socket is not self.s:
                                    self.send_message(username,client_socket,data)
        sys.exit(1)

if __name__ == "__main__":
    server = Server()
    server.main()
