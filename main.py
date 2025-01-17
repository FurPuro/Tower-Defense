import pygame
import random
import math
import copy
from button import Button
from tower import Tower
from enemy import Enemy
from config import *
from utils import loadLevel,generateWave,lookAt

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
waveTimer = FPS*40
summonTimerTimes = 0
summonTimer = 0
summonTimerNeedTimes = 0

basicFont = pygame.font.SysFont("Comic Sans MS",15)
marbiesText = basicFont.render(f"{marbies}m",True,HOTBAR_COLOR)
healthText = basicFont.render(f"{castle_health}hp",True,HOTBAR_COLOR)

playbutton = Button(WIDTH/2-240/2,HEIGHT/2-120/2,240,120,"menu",rf"{IMAGES_DIR}\playButton.png",rf"""
grid = loadLevel()
wave = 1
castle_health = CASTLE_MAX_HEALTH
game_state = 'game'
""")
playbutton.sprite.display = pygame.transform.scale(playbutton.sprite.display,(playbutton.sprite.rect.w,playbutton.sprite.rect.h))
bowTower = Tower(0,0,90,90,"none",fr"{IMAGES_DIR}\bowTurret.png",fr"{IMAGES_DIR}\arrow.png","bow0",100,150,1,2,0.8,1,180,210,False)

towersTimer = {}

equippedTowers.append(bowTower)

basicZombie = Enemy(0,0,60,60,"none",fr"{IMAGES_DIR}\basicZombie.png","basicZombie",2,13,False)
fastZombie = Enemy(0,0,60,60,"none",fr"{IMAGES_DIR}\fastZombie.png","fastZombie",3,8,False)
heavyZombie = Enemy(0,0,60,60,"none",fr"{IMAGES_DIR}\heavyZombie.png","heavyZombie",1,40,False)

while True:
    if game_state == "menu":
        screen.fill(MENU_BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.sprite.rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                        exec(button.code)
    elif game_state == "game":
        screen.fill(GAME_BG_COLOR)
        waveMobs = None
        waveMobs = generateWave(wave)
        marbiesText = basicFont.render(f"{marbies}m",True,HOTBAR_COLOR)
        healthText = basicFont.render(f"{castle_health}hp",True,HOTBAR_COLOR)
        for tower in placedTowers:
            if f"{tower.sprite.rect.x} {tower.sprite.rect.y}" not in towersTimer:
                    towersTimer[f"{tower.sprite.rect.x} {tower.sprite.rect.y}"] = 0
        for obj in grid:
            if "color" in obj and "x" in obj and "y" in obj and "id" in obj:
                pygame.draw.rect(screen,obj["color"],(obj["x"],obj["y"],GRID_SIZE,GRID_SIZE))
                if int(obj["id"]) == 2:
                    spawnCenterX = obj["x"]+(GRID_SIZE/2)
                    spawnCenterY = obj["y"]+(GRID_SIZE/2)
        if waveTimer >= FPS*45:
            waveTimer = 0
            wave += 1
            marbies += wave*40
            summonTimer = 0
            summonTimerTimes = 0
            summonTimerNeedTimes = len(waveMobs)
        if summonTimer >= FPS/3:
            summonTimer = 0
            if summonTimerNeedTimes > 0 and summonTimerTimes < summonTimerNeedTimes:
                summonTimerTimes += 1
                for index, waveEnemy in enumerate(waveMobs):
                    if index == summonTimerTimes-1:
                        for enemy in enemies:
                            if enemy.id == waveEnemy and enemy.new == False:
                                placedEnemy = Enemy(spawnCenterX+GRID_SIZE-enemy.sprite.rect.w/2,spawnCenterY-enemy.sprite.rect.h/2,enemy.sprite.rect.w,enemy.sprite.rect.h,enemy.sprite.state,enemy.sprite.path,enemy.id,enemy.walkSpeed,enemy.health,True)
                                enemiesOnMap.append(placedEnemy)
                                break
        
        for enemy in list(enemiesOnMap):
            enemy.sprite.draw(screen)
            enemy.move()
            enemy.new = False
            enemyText = basicFont.render(str(enemy.health),True,(255,0,0))
            screen.blit(enemyText,(enemy.sprite.rect.x+enemyText.get_width()/2,enemy.sprite.rect.y-enemy.sprite.rect.w/3,enemyText.get_width(),basicFont.get_linesize()))
            if enemy.health <= 0:
                enemiesOnMap.remove(enemy)
                marbies += 25
            for obj in grid:
                if "color" in obj and "x" in obj and "y" in obj and "id" in obj:
                    if enemy.sprite.rect.centerx >= obj["x"] and enemy.sprite.rect.centery >= obj["y"] and enemy.sprite.rect.centerx <= obj["x"]+GRID_SIZE and enemy.sprite.rect.centery <= obj["y"]+GRID_SIZE and enemy.sprite.rect.centerx >= 0 and enemy.sprite.rect.centery >= 0 and enemy.sprite.rect.centerx <= WIDTH and enemy.sprite.rect.centery <= HEIGHT:
                        if obj != None:
                            if obj["id"] == "5":
                                enemy.changeSpeed(enemy.walkSpeed,0)
                            elif obj["id"] == "6":
                                enemy.changeSpeed(0,enemy.walkSpeed)
                            elif obj["id"] == "7":
                                enemy.changeSpeed(0,-enemy.walkSpeed)
                            elif obj["id"] == "8":
                                enemy.changeSpeed(-enemy.walkSpeed,0)
                            elif obj["id"] == "3":
                                castle_health -= enemy.health
                                enemy.sprite.rect.x = 0
                                enemy.sprite.rect.y = 0
                                enemiesOnMap.remove(enemy)

        if castle_health <= 0:
            pygame.quit()

        waveTimer += 1
        summonTimer += 1

        for tower in placedTowers:
            tower.sprite.draw(screen)

        if towersTimer:
            for tower in placedTowers:
                key = f"{tower.sprite.rect.x} {tower.sprite.rect.y}"
                # print(keyTuple,value,tower.attacksPerSecond)
                if key in towersTimer:
                    towersTimer[key] += 1
                    if towersTimer[key] >= tower.attacksPerSecond*FPS:
                        towersTimer[key] = 0
                        targetEnemy = None
                        for enemy in enemiesOnMap:
                            if enemy.sprite.rect.centerx >= tower.sprite.rect.centerx-tower.maxDistance and enemy.sprite.rect.centery >= tower.sprite.rect.centerx-tower.maxDistance and enemy.sprite.rect.centerx <= tower.sprite.rect.centerx+tower.maxDistance and enemy.sprite.rect.centery <= tower.sprite.rect.centery+tower.maxDistance:
                                targetEnemy = enemy
                                break
                        if targetEnemy != None:
                            # lookAt(tower.sprite,targetEnemy.sprite)
                            targetEnemy.health -= tower.damage

        if hotbar_opened == True:
            pygame.draw.rect(screen,HOTBAR_COLOR,(0,0,WIDTH,GRID_SIZE*3))
            if equippedTowers and len(equippedTowers) <= MAX_EQUIPPED_TOWERS:
                for i,tower in enumerate(equippedTowers):
                    tower.sprite.rect.x = i*90
                    tower.sprite.rect.y = 0
                    tower.sprite.draw(screen)
        screen.blit(marbiesText, (0,HEIGHT-basicFont.get_linesize(),marbiesText.get_rect().w,marbiesText.get_rect().h))
        screen.blit(healthText, (0,HEIGHT-basicFont.get_linesize()*2,marbiesText.get_rect().w,marbiesText.get_rect().h))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                for tower in equippedTowers:
                    if tower.sprite.rect.collidepoint(mx,my):
                        selected_tower = Tower(tower.sprite.rect.x,tower.sprite.rect.y,tower.sprite.rect.w,tower.sprite.rect.h,tower.sprite.state,tower.sprite.path,tower.projectileSprite,tower.id,tower.price,tower.upgradePrice,tower.damage,tower.upgradeDamage,tower.attacksPerSecond,tower.upgradedAttacksPerSecond,tower.maxDistance,tower.upgradedMaxDistance,False)
                if selected_tower != None and hotbar_opened == False:
                    for obj in grid:
                        if "color" in obj and "x" in obj and "y" in obj and "id" in obj:
                            if mx >= obj["x"] and my >= obj["y"] and mx <= obj["x"]+GRID_SIZE and my <= obj["y"]+GRID_SIZE:
                                goodPlace = True
                                for x in range(-GRID_SIZE,GRID_SIZE*2,GRID_SIZE):
                                    for y in range(-GRID_SIZE,GRID_SIZE*2,GRID_SIZE):
                                        for obj2 in grid:
                                            if "color" in obj2 and "x" in obj2 and "y" in obj2 and "id" in obj2:
                                                if obj["x"]+x == obj2["x"] and obj["y"]+y == obj2["y"] and obj["x"]+x >= 0 and obj["y"]+y >= 0 and obj["x"]+x <= WIDTH and obj["y"]+y <= HEIGHT:
                                                    if int(obj2["id"]) != 0:
                                                        goodPlace = False

                                if goodPlace == True and marbies >= selected_tower.price:
                                    marbies -= selected_tower.price
                                    for x in range(-GRID_SIZE,GRID_SIZE*2,GRID_SIZE):
                                        for y in range(-GRID_SIZE,GRID_SIZE*2,GRID_SIZE):
                                            for obj2 in grid:
                                                if "color" in obj2 and "x" in obj2 and "y" in obj2 and "id" in obj2:
                                                    if obj["x"]+x == obj2["x"] and obj["y"]+y == obj2["y"] and obj["x"]+x >= 0 and obj["y"]+y >= 0 and obj["x"]+x <= WIDTH and obj["y"]+y <= HEIGHT:
                                                        obj2["id"] = "4"
                                                        obj2["color"] = (GAME_BG_COLOR[0]-10,GAME_BG_COLOR[1]-10,GAME_BG_COLOR[2]-10)

                                    placedTower = Tower(selected_tower.sprite.rect.x,selected_tower.sprite.rect.y,selected_tower.sprite.rect.w,selected_tower.sprite.rect.h,selected_tower.sprite.state,selected_tower.sprite.path,selected_tower.projectileSprite,selected_tower.id,selected_tower.price,selected_tower.upgradePrice,selected_tower.damage,selected_tower.upgradeDamage,selected_tower.attacksPerSecond,selected_tower.upgradedAttacksPerSecond,selected_tower.maxDistance,selected_tower.upgradedMaxDistance,False)
                                    placedTower.sprite.rect.x = obj["x"]-GRID_SIZE
                                    placedTower.sprite.rect.y = obj["y"]-GRID_SIZE
                                    placedTowers.append(placedTower)                                           
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    hotbar_opened = True
                # elif event.key == pygame.K_x:
                #     for tower in list(placedTowers):
                #         if tower.sprite.rect.collidepoint(mx,my):
                #             if tower.upgraded == True:
                #                 marbies += tower.upgradePrice/2
                #             else:
                #                 marbies += tower.price/2
                #             for obj in grid:
                #                 if "color" in obj and "x" in obj and "y" in obj and "id" in obj:
                #                     if mx >= obj["x"] and my >= obj["y"] and mx <= obj["x"]+GRID_SIZE and my <= obj["y"]+GRID_SIZE:
                #                         for x in range(-GRID_SIZE,GRID_SIZE*2,GRID_SIZE):
                #                             for y in range(-GRID_SIZE,GRID_SIZE*2,GRID_SIZE):
                #                                 print(x,y)
                #                                 for obj2 in grid:
                #                                     if "color" in obj2 and "x" in obj2 and "y" in obj2 and "id" in obj2:
                #                                         if obj["id"] == "4" and tower.sprite.rect.x+GRID_SIZE+x == obj2["x"] and tower.sprite.rect.y+GRID_SIZE+y == obj2["y"] and tower.sprite.rect.x+GRID_SIZE+x >= 0 and tower.sprite.rect.y+GRID_SIZE+y >= 0 and tower.sprite.rect.x+GRID_SIZE+x <= WIDTH and tower.sprite.rect.y+GRID_SIZE+y <= HEIGHT:
                #                                             obj2["id"] = "0"
                #                                             obj2["color"] = GAME_BG_COLOR
                #             placedTowers.remove(tower)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_TAB:
                    hotbar_opened = False

    for sprite in sprites:
        if sprite.state == game_state:
            sprite.draw(screen)
    pygame.display.set_caption(f"Tower Defense (FPS - {round(clock.get_fps())}, State - {str.capitalize(game_state)})")
    pygame.display.update()
    clock.tick(FPS)

#ДЗ проект