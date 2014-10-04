import pygame
from pygame.locals import *
import resourceManager
pygame.init()

class Player(object):
    def __init__(self,playerType,playerToken,playerName):
        self.type = playerType   # Human or AI
        self.token = playerToken # X or 0
        self.name = playerName   # Username if multiplayer, otherwise "You" if you, or "Computer" if AI
    def update(self):
        pass
