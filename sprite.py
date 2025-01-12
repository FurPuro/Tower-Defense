import pygame
import os
from config import sprites
class Sprite:
    def __init__(self,x,y,w,h,state,colorOrImagePath):
        self.rect = pygame.rect.Rect(x,y,w,h)
        self.display = colorOrImagePath
        self.state = state
        if os.path.isfile(str(self.display)):
            self.path = colorOrImagePath
            self.display = pygame.image.load(self.display)
        sprites.append(self)
    def draw(self,screen):
        if type(self.display) is not tuple:  #os.path.isfile(str(self.display)):
            screen.blit(self.display,self.rect)
        else:
            pygame.draw.rect(screen,self.display,self.rect)