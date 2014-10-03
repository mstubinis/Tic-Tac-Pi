import pygame
from pygame.locals import *
import resourceManager

class TextObject(pygame.sprite.Sprite):
    def __init__(self,pos,fontSize,fontcolor,textstring):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer

        self.position = pos
        self.message = textstring
        self.color = fontcolor
        self.font = pygame.font.Font(None,fontSize)
        self.text = self.font.render(self.message, 1,fontcolor)
        self.rect = pygame.Rect((0,0),self.font.size(self.message))

        self.rect.midtop = pos

    def is_clicked(self):
        if self.is_mouse_over() == True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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

    def update_message(self,message):
        self.message = message
        self.text = self.font.render(self.message, 1,self.color)
        self.rect.w = self.font.size(self.message)[0]
        self.rect.h = self.font.size(self.message)[1]
        self.rect.midtop = self.position

    def update(self):
        pass
    def draw(self,screen):
        screen.blit(self.text, self.rect)
