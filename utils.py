import pygame
import math
from config import *
import random
def loadLevel():
    gridList = []
    grass_color = (random.randint(75,150),random.randint(75,150),random.randint(75,150))
    way_color = (random.randint(75,150),random.randint(75,150),random.randint(75,150))
    save = open(fr"{LEVELS_DIR}\lvl{level}.txt")
    for row,line in enumerate(save.read().replace(" ","").splitlines()):
        for col,char in enumerate(line):
            # print((row)*GRID_SIZE,(col)*GRID_SIZE,char)
            obj = {
                "id": char,
                "x": (col)*GRID_SIZE,
                "y": (row)*GRID_SIZE
            }
            if char == "0":
                obj["color"] = (grass_color[0]+random.randint(-2,2),grass_color[1]+random.randint(-2,2),grass_color[2]+random.randint(-2,2))
            elif char == "1" or char == "2" or char == "5" or char == "6" or char == "7" or char == "8":
                obj["color"] = (way_color[0]+random.randint(-2,2),way_color[1]+random.randint(-2,2),way_color[2]+random.randint(-2,2))
            elif char == "3":
                obj["color"] = (CASTLE_COLOR[0]+random.randint(-2,2),CASTLE_COLOR[1]+random.randint(-2,2),CASTLE_COLOR[2]+random.randint(-2,2))
            gridList.append(obj)
    marbies = START_MARBIES
    return gridList
def getObjectInGrid(x,y):
    for obj in grid:
        if "color" in obj and "x" in obj and "y" in obj and "id" in obj:
            if x >= obj["x"] and y >= obj["y"] and x <= obj["x"]+GRID_SIZE and y <= obj["y"]+GRID_SIZE:
                return obj
    return None
def generateWave(waves):
    waveMobs = []
    basicZombies = round(1.3*waves)
    fastZombies = round(0.9*waves)
    heavyZombies = round(0.8*waves)
    basicBossZombies = math.floor((waves+5)/10)
    if waves > 1:
        if basicZombies > 0:
            for i in range(1,basicZombies):
                waveMobs.append("basicZombie")
        if fastZombies > 0:
            for i in range(1,fastZombies):
                waveMobs.append("fastZombie")
        if heavyZombies > 0:
            for i in range(1,heavyZombies):
                waveMobs.append("heavyZombie")
    else:
        for i in range(0,2):
            waveMobs.append("basicZombie")
    if waves % 10 == 0:
    # if waves == 10 or waves == 20 or waves == 30 or waves == 40 or waves == 50 or waves == 60 or waves == 70 or waves == 80 or waves == 90 or waves == 100:
        for i in range(0,basicBossZombies):
            waveMobs.append("basicBossZombie")
    random.shuffle(waveMobs)
    return waveMobs
def lookAt(sprite,sprite2):
    rel_x, rel_y = sprite2.rect.centerx - sprite.rect.centerx, sprite2.rect.centery - sprite.rect.centery
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    sprite.display = pygame.transform.rotate(sprite.original_image, int(angle+180))
    sprite.rect = sprite.display.get_rect(center=sprite.rect.center)
def rotate(sprite,angle):
    sprite.display = pygame.transform.rotate(sprite.original_image, int(angle))
    sprite.rect = sprite.display.get_rect(center=sprite.rect.center)
def projectileLookAt(sprite,sprite2):
    rel_x, rel_y = sprite2.rect.centerx - sprite.rect.centerx, sprite2.rect.centery - sprite.rect.centery
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    sprite.display = pygame.transform.rotate(sprite.original_image, int(angle-90))
    sprite.rect = sprite.display.get_rect(center=sprite.rect.center)
def calculateDistance(x1,y1,x2,y2):
    dx = x2-x1
    dy = y2-y1
    return math.sqrt(dx*dx+dy*dy)