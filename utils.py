import pygame
import math
import os
from config import *
import random
import cv2
import numpy as np
def loadLevel():
    global level,marbies
    level = fr"{LEVELS_DIR}/{random.choice(os.listdir(LEVELS_DIR))}"
    gridList = []
    grass_color = (random.randint(75,150),random.randint(75,150),random.randint(75,150))
    way_color = (random.randint(75,150),random.randint(75,150),random.randint(75,150))
    if ".png" in level:
        img = cv2.imread(f'{level}',0)
        rows,cols = img.shape
        for row in range(rows):
            for col in range(cols):
                k = img[row,col]
                if k == 195:
                    char = "0"
                elif k == 224:
                    char = "1"
                elif k == 183:
                    char = "2"
                elif k == 40:
                    char = "3"
                elif k == 97:
                    char = "4"
                elif k == 126:
                    char = "5"
                elif k == 95:
                    char = "6"
                elif k == 60:
                    char = "7"
                elif k == 47:
                    char = "8"
                else:
                    char = "-1"
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
    else:
        save = open(fr"{level}")
        for row,line in enumerate(save.read().replace(" ","").splitlines()):
            for col,char in enumerate(line):
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
        save.close()
    marbies = START_MARBIES
    return gridList
def getObjectInGrid(x,y):
    for obj in grid:
        if "color" in obj and "x" in obj and "y" in obj and "id" in obj:
            if x >= obj["x"] and y >= obj["y"] and x <= obj["x"]+GRID_SIZE and y <= obj["y"]+GRID_SIZE:
                return obj
    return None
def generateWave(waves):
    global waveTen
    for enemy in enemies:
        if waveTen > 1 and enemy not in enemiesOnMap:
            enemy.health += enemy.health/2.5
    if waves % 10 == 0 and waves > 1:
        waveTen += 1
    waveMobsGen = []
    basicZombies = round(1.3*(waves/waveTen))
    fastZombies = round(0.9*(waves/waveTen))
    heavyZombies = round(0.8*(waves/waveTen))
    basicBossZombies = math.floor((waves+5)/10)
    if waves > 1:
        if basicZombies > 0:
            for i in range(1,basicZombies):
                waveMobsGen.append("basicZombie")
        if fastZombies > 0:
            for i in range(1,fastZombies):
                waveMobsGen.append("fastZombie")
        if heavyZombies > 0:
            for i in range(1,heavyZombies):
                waveMobsGen.append("heavyZombie")
    else:
        for i in range(0,2):
            waveMobsGen.append("basicZombie")
    if waves % 10 == 0:
    # if waves == 10 or waves == 20 or waves == 30 or waves == 40 or waves == 50 or waves == 60 or waves == 70 or waves == 80 or waves == 90 or waves == 100:
        for i in range(0,basicBossZombies):
            waveMobsGen.append("basicBossZombie")
    random.shuffle(waveMobsGen)
    return waveMobsGen
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