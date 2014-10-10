import sys, socket,thread,select,pygame,json,Queue,resourceManager
from gameObjects import Player
from urllib2 import urlopen
from time import sleep
from threading import Thread

def GetIp():
    return json.load(urlopen('http://httpbin.org/ip'))['origin']

class ClientThreadSend(Thread):
    def __init__(self,client,socket):
        super(ClientThreadSend, self).__init__()
        self.running = True
        self.conn = socket
        self.q = Queue.Queue()
        self.client = client
        self.board = None
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
                    message = self.q.get(block=True, timeout=0.3)
                    self.conn.send(message)
            except socket.error as msg:
                print("Socket error!: " +  str(msg))
                pass
        self.conn.close()
class ClientThreadRecieve(Thread):
    def __init__(self,client,socket):
        super(ClientThreadRecieve, self).__init__()
        self.running = True
        self.conn = socket
        self.client = client
        self.board = None
    def stop(self):
        self.conn.shutdown(socket.SHUT_RDWR)
        self.conn.close()
        self.running = False 
    def run(self):
        while self.running:
            try:
                data = self.conn.recv(1024)
                if "_SENDCLIENTS_" in data:
                    l = resourceManager.parse_message(data,"_SENDCLIENTS_")
                    if len(l) == 1:
                        p1 = Player.Player("Human","X",l[0])
                        self.board.setplayers(p1,None,False)
                    elif len(l) == 2:
                        p1 = Player.Player("Human","X",l[0])
                        p2 = Player.Player("Human","O",l[1])
                        self.board.setplayers(p1,p2,False)

                        self.client.send_message("_STARTMATCH_")
                        
                elif "_STARTMATCH_" in data:
                    self.board.setcurrentplayer(data[12])
                    self.board.start_game()
                elif "_RECVBOARDINFO_" in data:
                    count = 0
                    for i in data[15:]:
                        if i != "N":
                            self.board.spots[count].token = i
                        else:
                            self.board.spots[count].token = ""
                        count += 1
                    self.board.getnextplayer()
                    self.board.checkforwin()
                    
            except socket.error as msg:
                print("Socket error!: " + str(msg))
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
        self.board = None
    def connect_to_server(self,errorButton,server,username):
        if username == "":
            error = "Please enter your name"
            errorButton.update_message(error)
            return False
        if server == "":
            error = "Please enter the server ip"
            errorButton.update_message(error)
            return False
        try:
            if self.connected == False:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                self.connection_destination = server
                if server.lower() == "localhost":
                    self.connection_destination = GetIp()

                
                self.username = username

                client_socket.connect((self.connection_destination, 6119))
                
                self.client = ClientThreadSend(self,client_socket)
                self.client.start()

                self.client1 = ClientThreadRecieve(self,client_socket)
                self.client1.start()
                
                self.send_message("_CONNECT_" + self.username,errorButton)

                self.connected = True
                return True
            else:
                error = "Already connected to a server!"
                errorButton.update_message(error)
                return False
        except:
            return False
    def disconnect_from_server(self,errorButton,error=False):
        if error == False:
            self.send_message("_DISCONNECT_" + self.username,errorButton)
            
        self.client.stop()
        self.client1.stop()
        self.connected = False

    def set_board(self,board):
        self.board = board
        self.client.board = board
        self.client1.board = board
    def send_message(self,message,errorButton=None):
        if self.client != None:       
            self.client.add(message)
      
    def update(self,errorButton,events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                try:
                    self.send_message(self.username,errorButton)
                except:
                    pass
