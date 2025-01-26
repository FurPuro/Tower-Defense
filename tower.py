from sprite import Sprite
from config import *
from os.path import isfile
class Tower:
    def __init__(self,x,y,w,h,state,colorOrImagePath,colorOrImagePathProjectile,id,price,upgradePrice,damage,upgradeDamage,attacksPerSecond,upgradedAttacksPerSecond,maxDistance,upgradedMaxDistance,territories,attackRadius,gPrice):
        self.sprite = Sprite(x,y,w,h,state,colorOrImagePath)
        self.projectileSprite = Sprite(x,y,GRID_SIZE/2,GRID_SIZE/2,state,colorOrImagePathProjectile)
        self.id = id
        self.price = price
        self.upgradePrice = upgradePrice
        self.damage = damage
        self.upgradeDamage = upgradeDamage
        self.attacksPerSecond = attacksPerSecond
        self.upgradedAttacksPerSecond = upgradedAttacksPerSecond
        self.maxDistance = maxDistance
        self.upgradedMaxDistance = upgradedMaxDistance
        self.upgraded = False
        self.upgraded2 = False
        self.territories = territories
        self.attackRadius = attackRadius
        self.gPrice = gPrice
        towers.append(self)
    def upgrade(self):
        x,y,w,h,state,path = self.sprite.rect.x,self.sprite.rect.y,self.sprite.rect.w,self.sprite.rect.h,self.sprite.state,self.sprite.path
        if isfile(path.replace(".png","Upgraded.png")):
            self.sprite = Sprite(x,y,w,h,state,path.replace(".png","Upgraded.png"))
            self.price = self.upgradePrice
            self.damage = self.upgradeDamage
            self.attacksPerSecond = self.upgradedAttacksPerSecond
            self.maxDistance = self.upgradedMaxDistance
            self.upgraded = True
            return True
        return False
    def upgrade2(self):
        x,y,w,h,state,path = self.sprite.rect.x,self.sprite.rect.y,self.sprite.rect.w,self.sprite.rect.h,self.sprite.state,self.sprite.path
        if isfile(path.replace(".png","Upgraded2.png")):
            self.sprite = Sprite(x,y,w,h,state,path.replace(".png","Upgraded2.png"))
            self.price = self.upgradePrice
            self.damage = self.upgradeDamage
            self.attacksPerSecond = self.upgradedAttacksPerSecond
            self.maxDistance = self.upgradedMaxDistance
            self.upgraded2 = True
            return True
        return False
    def copy(self):
        return Tower(self.sprite.rect.x,self.sprite.rect.y,self.sprite.rect.w,self.sprite.rect.h,self.sprite.state,self.sprite.path,self.projectileSprite.path,self.id,self.price,self.upgradePrice,self.damage,self.upgradeDamage,self.attacksPerSecond,self.upgradedAttacksPerSecond,self.maxDistance,self.upgradedMaxDistance,self.territories,self.attackRadius,self.gPrice)