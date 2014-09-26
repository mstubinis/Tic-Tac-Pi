import pygame
from pygame.locals import *
import resourceManager

class MenuButton(pygame.sprite.Sprite):
    def __init__(self,stringOfText,pos):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.mouseOver = False

        self.message = stringOfText
        self.font = pygame.font.Font(None,120)
        self.text = self.font.render(self.message, 1,(255,255,255))
        self.rect = pygame.Rect((0,0),self.font.size(self.message))
        self.rect.midtop = pos

    def is_clicked(self):
        if self.is_mouse_over() == True:
            if pygame.mouse.get_pressed()[0] == 1:
                return True
        return False
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
    
    def update(self):
        if self.is_mouse_over() == True:
            self.mouseOver = True
        else:
            self.mouseOver = False

    def draw(self,screen):
        if self.mouseOver == True:
            pygame.draw.rect(screen,(0,255,0),self.rect)
        else:
            pygame.draw.rect(screen,(125,125,125),self.rect)
        screen.blit(self.text, self.rect)
