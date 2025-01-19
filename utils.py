import pygame
import os
import math
from config import *
import random
def loadLevel():
    gridList = []
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
                obj["color"] = (GAME_BG_COLOR[0]+random.randint(-2,2),GAME_BG_COLOR[1]+random.randint(-2,2),GAME_BG_COLOR[2]+random.randint(-2,2))
            elif char == "1" or char == "2" or char == "5" or char == "6" or char == "7" or char == "8":
                obj["color"] = (WAY_COLOR[0]+random.randint(-2,2),WAY_COLOR[1]+random.randint(-2,2),WAY_COLOR[2]+random.randint(-2,2))
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
    basicBossZombies = round(waves/10)
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
        for i in range(0,round(2*1)):
            waveMobs.append("basicZombie")
    if waves != 1 and waves % 10 == 0:
        for i in range(1,basicBossZombies):
            waveMobs.append("basicBossZombie")
    random.shuffle(waveMobs)
    return waveMobs
def lookAt(sprite,sprite2):
    rel_x, rel_y = sprite2.rect.centerx - sprite.rect.centerx, sprite2.rect.centery - sprite.rect.centery
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    sprite.display = pygame.transform.rotate(sprite.original_image, int(angle+180))
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