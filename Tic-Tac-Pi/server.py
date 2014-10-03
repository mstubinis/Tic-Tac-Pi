import socket,sys,select,thread
from time import sleep

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
            if "_CONNECT" in data:
                print(data[8:] + " connected!")


                    
            elif "_DISCONNECT" in data:
                print(data[11:] + " disconnected!")
        else:
            print(data)
        
    def send_message(self,client,conn,message):
        conn.sendall(client + ": " + message)
        
    def main(self):
        while True:
            inputReady, outputReady, exceptReady = select.select(self.clients.values(), [], [])
            for x in inputReady:
                if x != None:
                    if x == self.s:
                        try:
                            conn, addr = self.s.accept()
                            self.clients[addr[0]] = conn
                        except socket.error, msg:
                            print("Socket error: " + str(msg))
                            pass

                    else:  
                        data = x.recv(4096)
                        if data:
                            if not "." in data:
                                self.process(data,x)
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
