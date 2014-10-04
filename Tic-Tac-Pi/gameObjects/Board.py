import pygame, Player, random, TextObject
from pygame.locals import *
import resourceManager, TextObject
from time import sleep
pygame.init()

class BoardSpot(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.mouseOver = False
        self.token = ""
        self.position = pos
        self.rect = pygame.Rect((0,0),(100,100))
        self.rect.midtop = self.position

    def is_mouse_over(self):
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] < self.rect.x:
            return False
        if mousePos[0] > self.rect.x + self.rect.w:
            return False
        if mousePos[1] < self.rect.y:
            return False
        if mousePos[1] > self.rect.y + self.rect.h:
            return False
        return True

    def set_token(self,board):
        if self.token == "":
            self.token = board.currentPlayer.token
            if board.currentPlayer == board.player1:
                board.currentPlayer = board.player2
            else:
                board.currentPlayer = board.player1
            board.currentPlayerTextObject.update_message("It is " + board.currentPlayer.name + "'s turn!")
        else:
            error = "That spot already has a token on it!"
            board.errorObject.update_message(error)

    def update(self):
        if self.is_mouse_over() == True:
            self.mouseOver = True
        else:
            self.mouseOver = False

    def draw(self,screen,x,o):
        if self.mouseOver == True:
            pygame.draw.rect(screen,(115,205,205),self.rect)
        else:
            pass
        if self.token != "":
            if self.token == "X":
                screen.blit(x,self.rect)
            else:
                screen.blit(o,self.rect)

class Board(object):
    def __init__(self,player1,player2,windowWidth,windowHeight,multiplayer=False,username=""):
        self.player1 = player1
        self.player2 = player2

        self.image_X,self.image_X_Rect = resourceManager.load_image("X.png",-1)
        self.image_O,self.image_O_Rect = resourceManager.load_image("O.png",-1)

        self.currentPlayer = None
        self.gameOver = False

        # do not touch these 2, they will be used in multiplayer games
        self.multiplayer = multiplayer
        self.username = username

        # load and position the tic-tac-toe board
        self.board_image,self.board_rect = resourceManager.load_image("board.png",-1)
        self.board_rect.midtop = (windowWidth/2,0)

        # create error text object and current player text object
        self.currentPlayerTextObject = TextObject.TextObject((windowWidth/2,windowHeight-110),50,(255,255,0),"")
        self.errorObject = TextObject.TextObject((windowWidth/2,windowHeight-50),50,(255,0,0),"")


        # Here is how the board spots are indexed in the list
        #    |   |
        #  0 | 3 | 6
        #--------------
        #  1 | 4 | 7
        #--------------
        #  2 | 5 | 8
        #    |   |
        #
        #
        # for example, self.spots[0] will point to the top left spot
        #              self.spots[4] will point to the middle spot
        #              self.spots[5] will point to the middle bottom spot

        # now let's actually spawn the board spots
        self.spots = []
        for i in range(3):
            for j in range(3):
                pos = (self.board_rect.x + 58 + (130 * i),self.board_rect.y + 7 + (130 * j))
                self.spots.append(BoardSpot(pos))

    def setplayers(self,p1,p2):
        # set the game players and randomly choose one of them to go first
        self.player1 = p1
        self.player2 = p2
        random_int = random.randint(0,1)
        if random_int == 0:
            self.currentPlayer = self.player1
        else:
            self.currentPlayer = self.player2
        self.currentPlayerTextObject.update_message("It is " + self.currentPlayer.name + "'s turn!")

    # mtubinis will use these methods, they are for multi-player games only
    def setplayer1(self,p1):
        pass
    def setplayer2(self,p2):
        pass

    def domove(self,events):
        if self.currentPlayer.type == "Human":
            # these lines check to see if the player clicked on an empty spot to place their token at
            for i in self.spots:
                if i.mouseOver == True:
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                if self.multiplayer == False:
                                    i.set_token(self)
                                else:
                                    if self.currentPlayer.name == self.username:
                                        i.set_token(self)
                    
        elif self.currentPlayer.type == "Computer":
            # this method is called if it is the computer's turn
            self.doaimove()
        # after every move, check to see if any of the players have won, or if the game ended in a tie
        self.checkforwin()

    def doaimove(self):# mtubinis will place computer AI here later on
        
        # for now, can you just make it so the computer will choose
        # a random empty spot to place his token at?
        # just pick a random spot from self.spots, and call spot.set_token(self)
        # you can check if a spot is empty if: spot.token == ""

        for spot in self.spots:
            # place checking code here, and don't forget to remove "pass" right below this comment line
            pass
        
        sleep(1)

    # this method will check to see if either of the 3 rows, columns, or diagonals are a win condition.
    # If not and all the spots on the board are filled,then it will be a tie. Use the commented out code when you determine if
    # player1 wins, player2 wins, or if the game is a tie
    def checkforwin(self):
        
        winner = "" # set this variable to the player that won the game, use "Player 1" for player 1,
                    # "Player 2" for player 2, and "None" for a tie game
        
        # put in winning checking code here

        
        if winner == "Player 1":
            self.currentPlayerTextObject.update_message(self.player1.name + " wins!")
            self.gameOver = True
        elif winner == "Player 2":
            self.currentPlayerTextObject.update_message(self.player2.name + " wins!")
            self.gameOver = True
        elif winner == "None":
            self.currentPlayerTextObject.update_message("The game ended in a tie!")
            self.gameOver = True
        else:
            pass

    def update(self,events):
        self.domove(events)
        self.currentPlayerTextObject.update()
        self.errorObject.update()
        for i in self.spots:
            i.update()

    def draw(self, screen):
        screen.blit(self.board_image,self.board_rect)
        self.currentPlayerTextObject.draw(screen)
        self.errorObject.draw(screen)
        for i in self.spots:
            i.draw(screen,self.image_X,self.image_O)
