from sprite import Sprite
from config import *
class Tower:
    def __init__(self,x,y,w,h,state,colorOrImagePath,colorOrImagePathProjectile,id,price,upgradePrice,damage,upgradeDamage,attacksPerSecond,upgradedAttacksPerSecond,maxDistance,upgradedMaxDistance,upgraded):
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
        towers.append(self)