from sprite import Sprite
from config import GRID_SIZE,enemies,grid,WIDTH,HEIGHT
from pygame.transform import rotate
class Enemy:
    def __init__(self,x,y,w,h,state,colorOrImagePath,id,walkSpeed,health,new):
        self.sprite = Sprite(x,y,w,h,state,colorOrImagePath)
        self.speed = [0,0]
        self.walkSpeed = walkSpeed
        self.health = health
        self.id = id
        self.new = new
        self.sprite.display = rotate(self.sprite.display,90)
        enemies.append(self)
    def move(self):
        self.sprite.rect.x += self.speed[0]
        self.sprite.rect.y += self.speed[1]
    def changeSpeed(self,x,y):
        self.speed = [x,y]