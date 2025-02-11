from sprite import Sprite
from config import enemies
from pygame.transform import rotate
class Enemy:
    def __init__(self,x,y,w,h,state,colorOrImagePath,id,walkSpeed,health,new):
        self.sprite = Sprite(x,y,w,h,state,colorOrImagePath)
        self.speed = [0,0]
        self.pos = [x,y]
        self.walkSpeed = walkSpeed
        self.defaultWalkSpeed = walkSpeed
        self.health = health
        self.id = id
        self.new = new
        self.sprite.display = rotate(self.sprite.display,90)
        enemies.append(self)
    def move(self):
        self.pos = [self.pos[0]+self.speed[0],self.pos[1]+self.speed[1]]
        self.sprite.rect.x = round(self.pos[0])
        self.sprite.rect.y = round(self.pos[1])
    def changeSpeed(self,x,y):
        self.speed = [x,y]