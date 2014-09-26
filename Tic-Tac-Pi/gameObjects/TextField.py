import pygame
from pygame.locals import *
import resourceManager

class TextField(pygame.sprite.Sprite):
    def __init__(self,pos,maxChars,fontSize,buttonName):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.mouseOver = False
        self.selected = False
        self.blink = False
        self.timer = 0
        self.name = buttonName

        self.maxChars = maxChars
        self.message = ""
        temp_message = ""
        for i in range(maxChars):
            temp_message += "X"
        
        self.font = pygame.font.Font(None,fontSize)
        self.text = self.font.render(self.message, 1,(255,255,255))
        self.rect = pygame.Rect(0,0,self.font.size(temp_message)[0]+6,self.font.size(temp_message)[1]+8)

        self.nametext = self.font.render(self.name, 1,(255,255,255))
        self.rect_name = pygame.Rect(0,0,self.font.size(self.name)[0],self.font.size(self.name)[1])
        
        self.rect.midtop = pos
        self.rect_name.midtop = pos
        self.rect_name.y -= self.font.size("X")[1] + 8

    def is_clicked(self):
        if pygame.mouse.get_pressed()[0] == 1:
            if self.is_mouse_over() == True:
                self.selected = True
                return True
            else:
                self.selected = False
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
        if ord(message) != 8 and ord(message) != 13:#not backspace key or enter key
            if len(self.message) < self.maxChars:
                self.message += message
                self.text = self.font.render(self.message, 1,(255,255,255))
        elif ord(message) == 8:#backspace key
            if len(self.message) > 0:
                self.message = self.message[:-1]
                self.text = self.font.render(self.message, 1,(255,255,255))
        elif ord(message) == 13:#enter key
            if self.selected == True:
                self.blink = False
                self.timer = 0
                self.selected = False
    
    def update(self):
        self.is_clicked()
        if self.is_mouse_over() == True:
            self.mouseOver = True
        else:
            self.mouseOver = False
            
        if self.selected == True:
            self.timer += 1
            if self.timer > 20:
                self.timer = 0
                self.blink = not self.blink
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    try:
                        self.update_message(str(chr(event.key)))
                    except:
                        pass
            

    def draw(self,screen):
        if self.selected == True:
            pygame.draw.rect(screen,(25,25,25),self.rect)
            if self.blink == True:
                rectNew = pygame.Rect(self.rect.x+self.font.size(self.message)[0] + 8,self.rect.y+4,8,self.rect.h-9)
                pygame.draw.rect(screen,(255,255,255),rectNew)
        else:
            pygame.draw.rect(screen,(0,0,0),self.rect)
        screen.blit(self.nametext, self.rect_name)
        screen.blit(self.text, self.rect)
