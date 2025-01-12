import pygame
import os
import math
from config import *
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
                obj["color"] = GAME_BG_COLOR
            elif char == "1" or char == "2" or char == "5" or char == "6" or char == "7" or char == "8":
                obj["color"] = WAY_COLOR
            elif char == "3":
                obj["color"] = CASTLE_COLOR
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
    waveMobs = {
        "basicZombie": math.floor(2*((waves-0.5)*2)),
        "fastZombie": math.floor(2*(waves-1))
    }
    return waveMobs
def lookAt(sprite,sprite2):
    rel_x, rel_y = sprite2.rect.y - sprite.rect.x, sprite2.rect.y - sprite.rect.y
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    sprite.display = pygame.transform.rotate(sprite.original_image, int(angle))
    # sprite.rect = sprite.display.get_rect(center=sprite.rect)