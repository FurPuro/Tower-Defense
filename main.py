import pygame
import random
import math
import copy
import os
import sys
from button import Button
from tower import Tower
from enemy import Enemy
from config import *
from itertools import chain
from utils import loadLevel,generateWave,lookAt,calculateDistance

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
summonTimerTimes = 0
summonTimer = 0
summonTimerNeedTimes = 0
waveTimer = FPS*40
basicFont = pygame.font.SysFont("Comic Sans MS",15)
smallBasicFont = pygame.font.SysFont("Comic Sans MS",10)
marbiesText = basicFont.render(f"{marbies}m",True,HOTBAR_COLOR)
healthText = basicFont.render(f"{castle_health}hp",True,HOTBAR_COLOR)

background = pygame.image.load(fr"{IMAGES_DIR}\MenuBackground.png")
background = pygame.transform.scale(background,(WIDTH,HEIGHT))

playbutton = Button(WIDTH/2-240/2,HEIGHT/2-120/2,240,120,"menu",rf"{IMAGES_DIR}\playButton.png",rf"""
grid = loadLevel()
wave = 0
castle_health = CASTLE_MAX_HEALTH
game_state = 'game'
""")
shopbutton = Button(WIDTH/2-270,HEIGHT/2-90/2,90,90,"menu",rf"{IMAGES_DIR}\shopButton.png",rf"""
game_state = 'shop'
""")
returnbutton = Button(5,5,30,30,"shop",rf"{IMAGES_DIR}\returnButton.png",rf"""
game_state = 'menu'
""")
returnbutton2 = Button(5,5,30,30,"saves",rf"{IMAGES_DIR}\returnButton.png",rf"""
game_state = 'menu'
""")
savesbutton = Button(WIDTH/2+180,HEIGHT/2-90/2,90,90,"menu",rf"{IMAGES_DIR}\savesButton.png",rf"""
game_state = 'saves'
""")

playbutton.sprite.display = pygame.transform.scale(playbutton.sprite.display,(playbutton.sprite.rect.w,playbutton.sprite.rect.h))
shopbutton.sprite.display = pygame.transform.scale(shopbutton.sprite.display,(shopbutton.sprite.rect.w,shopbutton.sprite.rect.h))
returnbutton.sprite.display = pygame.transform.scale(returnbutton.sprite.display,(returnbutton.sprite.rect.w,returnbutton.sprite.rect.h))
returnbutton2.sprite.display = pygame.transform.scale(returnbutton2.sprite.display,(returnbutton2.sprite.rect.w,returnbutton2.sprite.rect.h))
savesbutton.sprite.display = pygame.transform.scale(savesbutton.sprite.display,(savesbutton.sprite.rect.w,savesbutton.sprite.rect.h))

bowTower = Tower(0,0,90,90,"none",fr"{IMAGES_DIR}\bowTurret.png",fr"{IMAGES_DIR}\arrow.png","bow",125,250,1,2,1,1.5,180,210,[])
cannonTower = Tower(0,0,90,90,"none",fr"{IMAGES_DIR}\cannonTurret.png",fr"{IMAGES_DIR}\Core.png","cannon",200,325,4,3,2,1.25,240,300,[])
piqueTower = Tower(0,0,90,90,"none",fr"{IMAGES_DIR}\piqueTurret.png",fr"{IMAGES_DIR}\None.png","pique",150,275,0.5,1,0.25,0.5,120,150,[])

towersTimer = {}

shopTowers = []

shopTowers.append(cannonTower)
shopTowers.append(piqueTower)

save = open(fr"{SAVES_DIR}\save0.txt","r+")
saveLines = save.readlines()
if saveLines:
    if saveLines[0] and saveLines[0] != "":
        gold = int(saveLines[0])
    else:
        gold = 0
    if saveLines[1] and saveLines[1] != "":
         
        for line in saveLines:
            if line != saveLines[0]:
                readedTower = []
                for index,tower in enumerate(line.split(",")):
                    add = tower
                    if index == 0 or index == 1 or index == 2 or index == 3 or (index >= 8 and index < 16):
                        add = float(tower)
                    elif index == 16:
                        add = []
                    readedTower.append(add)
                equippedTowers.append(Tower(*readedTower))
    else:
        equippedTowers.append(bowTower)
else:
    gold = 0
    equippedTowers.append(bowTower)
    # saveList = ["0\n"]
    # for tower in equippedTowers:
    #     saveList.append(f"{tower.sprite.rect.x},{tower.sprite.rect.y},{tower.sprite.rect.w},{tower.sprite.rect.h},{tower.sprite.path},{tower.projectileSprite.path},{tower.id},{tower.price},{tower.upgradePrice},{tower.damage},{tower.upgradeDamage},{tower.attacksPerSecond},{tower.upgradedAttacksPerSecond},{tower.maxDistance},{tower.upgradedMaxDistance},{tower.territories}\n")
    # save.writelines(saveList)
save.close()

basicZombie = Enemy(0,0,60,60,"none",fr"{IMAGES_DIR}\basicZombie.png","basicZombie",2,13,False)
fastZombie = Enemy(0,0,60,60,"none",fr"{IMAGES_DIR}\fastZombie.png","fastZombie",3,8,False)
heavyZombie = Enemy(0,0,60,60,"none",fr"{IMAGES_DIR}\heavyZombie.png","heavyZombie",1,40,False)
basicBossZombie = Enemy(0,0,90,90,"none",fr"{IMAGES_DIR}\basicBossZombie.png","basicBossZombie",1,120,False)

while True:
    save = open(fr"{SAVES_DIR}\save0.txt","w")
    saveList = [f"{gold}\n"]
    if equippedTowers:
        for tower in equippedTowers:
            saveList.append(f"{tower.sprite.rect.x},{tower.sprite.rect.y},{tower.sprite.rect.w},{tower.sprite.rect.h},{tower.sprite.state},{tower.sprite.path},{tower.projectileSprite.path},{tower.id},{tower.price},{tower.upgradePrice},{tower.damage},{tower.upgradeDamage},{tower.attacksPerSecond},{tower.upgradedAttacksPerSecond},{tower.maxDistance},{tower.upgradedMaxDistance},{tower.territories}\n")
    else:
        equippedTowers.append(bowTower)
        for tower in equippedTowers:
            saveList.append(f"{tower.sprite.rect.x},{tower.sprite.rect.y},{tower.sprite.rect.w},{tower.sprite.rect.h},{tower.sprite.state},{tower.sprite.path},{tower.projectileSprite.path},{tower.id},{tower.price},{tower.upgradePrice},{tower.damage},{tower.upgradeDamage},{tower.attacksPerSecond},{tower.upgradedAttacksPerSecond},{tower.maxDistance},{tower.upgradedMaxDistance},{tower.territories}\n")
        
    save.writelines(saveList)
    save.close()

    if game_state == "menu":
        screen.fill(MENU_BG_COLOR)
        screen.blit(background,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.sprite.rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]) and button.sprite.state == game_state:
                        exec(button.code)
    elif game_state == "shop":
        screen.fill(MENU_BG_COLOR)
        goldText = basicFont.render(f"{gold}G",True,(0,255,0))
        
        for i,tower in enumerate(shopTowers):
            tower.sprite.draw(screen)
            tower.sprite.rect.x = 30+i*120
            tower.sprite.rect.y = 60
            text1 = smallBasicFont.render(f"PRICE: {tower.price} > {tower.upgradePrice}",True,(0,255,255))
            text2 = smallBasicFont.render(f"DAMAGE: {tower.damage} > {tower.upgradeDamage}",True,(0,255,255))
            text3 = smallBasicFont.render(f"ATTACKSPEED: {tower.attacksPerSecond} > {tower.upgradedAttacksPerSecond}",True,(0,255,255))
            text4 = smallBasicFont.render(f"DISTANCE: {tower.maxDistance} > {tower.upgradedMaxDistance}",True,(0,255,255))
            if tower.id == "cannon":
                text5 = smallBasicFont.render(f"GOLD PRICE: 800",True,(0,255,255))
            if tower.id == "pique":
                text5 = smallBasicFont.render(f"GOLD PRICE: 2400",True,(0,255,255))
            screen.blit(text1, (tower.sprite.rect.x,tower.sprite.rect.y+tower.sprite.rect.h+smallBasicFont.get_linesize()*0,text1.get_rect().w,text1.get_rect().h))
            screen.blit(text2, (tower.sprite.rect.x,tower.sprite.rect.y+tower.sprite.rect.h+smallBasicFont.get_linesize()*1,text2.get_rect().w,text2.get_rect().h))
            screen.blit(text3, (tower.sprite.rect.x,tower.sprite.rect.y+tower.sprite.rect.h+smallBasicFont.get_linesize()*2,text3.get_rect().w,text3.get_rect().h))
            screen.blit(text4, (tower.sprite.rect.x,tower.sprite.rect.y+tower.sprite.rect.h+smallBasicFont.get_linesize()*3,text4.get_rect().w,text4.get_rect().h))
            screen.blit(text5, (tower.sprite.rect.x,tower.sprite.rect.y+tower.sprite.rect.h+smallBasicFont.get_linesize()*4,text5.get_rect().w,text5.get_rect().h))

        screen.blit(goldText, (0,HEIGHT-basicFont.get_linesize()*1,goldText.get_rect().w,goldText.get_rect().h))
        for event in pygame.event.get():
            mx,my = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.sprite.rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]) and button.sprite.state == game_state:
                        exec(button.code)
                for tower in shopTowers:
                    if tower.sprite.rect.collidepoint(mx,my):
                        have_this = False
                        for tower2 in equippedTowers:
                            if tower.id == tower2.id:
                                have_this = True
                            if have_this == False and tower.id == "cannon":
                                if gold >= 800:
                                    gold -= 800
                                    selected_tower = Tower(tower.sprite.rect.x,tower.sprite.rect.y,tower.sprite.rect.w,tower.sprite.rect.h,tower.sprite.state,tower.sprite.path,tower.projectileSprite.path,tower.id,tower.price,tower.upgradePrice,tower.damage,tower.upgradeDamage,tower.attacksPerSecond,tower.upgradedAttacksPerSecond,tower.maxDistance,tower.upgradedMaxDistance,tower.territories)
                                    equippedTowers.append(selected_tower)
                            if have_this == False and tower.id == "pique":
                                if gold >= 2400:
                                    gold -= 2400
                                    selected_tower = Tower(tower.sprite.rect.x,tower.sprite.rect.y,tower.sprite.rect.w,tower.sprite.rect.h,tower.sprite.state,tower.sprite.path,tower.projectileSprite.path,tower.id,tower.price,tower.upgradePrice,tower.damage,tower.upgradeDamage,tower.attacksPerSecond,tower.upgradedAttacksPerSecond,tower.maxDistance,tower.upgradedMaxDistance,tower.territories)
                                    equippedTowers.append(selected_tower)
    elif game_state == "saves":
        screen.fill(MENU_BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.sprite.rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]) and button.sprite.state == game_state:
                        exec(button.code)
    elif game_state == "game":
        screen.fill(GAME_BG_COLOR)
        waveMobs = None
        waveMobs = generateWave(wave)
        marbiesText = basicFont.render(f"{round(marbies,1)}m",True,HOTBAR_COLOR)
        healthText = basicFont.render(f"{castle_health}hp",True,HOTBAR_COLOR)
        goldText = basicFont.render(f"{gold}G",True,HOTBAR_COLOR)
        wavesText = basicFont.render(f"Wave {wave}",True,HOTBAR_COLOR)
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
            marbies += wave*20
            summonTimer = 0
            summonTimerTimes = 0
            summonTimerNeedTimes = len(waveMobs)
            gold += 3 * wave
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
            enemyText = basicFont.render(str(round(enemy.health)),True,(255,0,0))
            screen.blit(enemyText,(enemy.sprite.rect.x+enemyText.get_width()/2,enemy.sprite.rect.y-enemy.sprite.rect.w/3,enemyText.get_width(),basicFont.get_linesize()))
            if enemy.health <= 0:
                enemiesOnMap.remove(enemy)
                marbies += 25
                gold += 1
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
                        targetEnemy = None
                        maxHP = 0
                        maxWS = 0
                        for enemy in enemiesOnMap:
                            distance = calculateDistance(tower.sprite.rect.centerx,tower.sprite.rect.centery,enemy.sprite.rect.centerx,enemy.sprite.rect.centery)
                            if enemy.health > maxHP and enemy.walkSpeed > maxWS and distance <= tower.maxDistance:
                                targetEnemy = enemy
                                maxHP = enemy.health
                                maxWS = enemy.walkSpeed
                        if targetEnemy != None:
                            towersTimer[key] = 0
                            targetEnemy.health -= tower.damage
                            lookAt(tower.sprite,targetEnemy.sprite)

        if hotbar_opened == True:
            pygame.draw.rect(screen,HOTBAR_COLOR,(0,0,WIDTH,GRID_SIZE*3))
            if equippedTowers and len(equippedTowers) <= MAX_EQUIPPED_TOWERS:
                for i,tower in enumerate(equippedTowers):
                    tower.sprite.rect.x = i*90
                    tower.sprite.rect.y = 0
                    tower.sprite.draw(screen)
                    text1 = smallBasicFont.render(f"PRC: {tower.price} > {tower.upgradePrice}",True,(0,255,255))
                    text2 = smallBasicFont.render(f"DMG: {tower.damage} > {tower.upgradeDamage}",True,(0,255,255))
                    text3 = smallBasicFont.render(f"ATKSPD: {tower.attacksPerSecond} > {tower.upgradedAttacksPerSecond}",True,(0,255,255))
                    text4 = smallBasicFont.render(f"DST: {tower.maxDistance} > {tower.upgradedMaxDistance}",True,(0,255,255))
                    screen.blit(text1, (tower.sprite.rect.x,tower.sprite.rect.y+tower.sprite.rect.h+smallBasicFont.get_linesize()*0,text1.get_rect().w,text1.get_rect().h))
                    screen.blit(text2, (tower.sprite.rect.x,tower.sprite.rect.y+tower.sprite.rect.h+smallBasicFont.get_linesize()*1,text2.get_rect().w,text2.get_rect().h))
                    screen.blit(text3, (tower.sprite.rect.x,tower.sprite.rect.y+tower.sprite.rect.h+smallBasicFont.get_linesize()*2,text3.get_rect().w,text3.get_rect().h))
                    screen.blit(text4, (tower.sprite.rect.x,tower.sprite.rect.y+tower.sprite.rect.h+smallBasicFont.get_linesize()*3,text4.get_rect().w,text4.get_rect().h))
        screen.blit(marbiesText, (0,HEIGHT-basicFont.get_linesize(),marbiesText.get_rect().w,marbiesText.get_rect().h))
        screen.blit(healthText, (0,HEIGHT-basicFont.get_linesize()*2,healthText.get_rect().w,healthText.get_rect().h))
        screen.blit(goldText, (0,HEIGHT-basicFont.get_linesize()*3,goldText.get_rect().w,goldText.get_rect().h))
        screen.blit(wavesText, (0,HEIGHT-basicFont.get_linesize()*4,wavesText.get_rect().w,wavesText.get_rect().h))
        for event in pygame.event.get():
            mx,my = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for tower in equippedTowers:
                    if tower.sprite.rect.collidepoint(mx,my):
                        selected_tower = Tower(tower.sprite.rect.x,tower.sprite.rect.y,tower.sprite.rect.w,tower.sprite.rect.h,tower.sprite.state,tower.sprite.path,tower.projectileSprite,tower.id,tower.price,tower.upgradePrice,tower.damage,tower.upgradeDamage,tower.attacksPerSecond,tower.upgradedAttacksPerSecond,tower.maxDistance,tower.upgradedMaxDistance,tower.territories)
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
                                    territories = []
                                    for x in range(-GRID_SIZE,GRID_SIZE*2,GRID_SIZE):
                                        for y in range(-GRID_SIZE,GRID_SIZE*2,GRID_SIZE):
                                            for obj2 in grid:
                                                if "color" in obj2 and "x" in obj2 and "y" in obj2 and "id" in obj2:
                                                    if obj["x"]+x == obj2["x"] and obj["y"]+y == obj2["y"] and obj["x"]+x >= 0 and obj["y"]+y >= 0 and obj["x"]+x <= WIDTH and obj["y"]+y <= HEIGHT:
                                                        obj2["id"] = "4"
                                                        territories.append(obj2)
                                                        obj2["color"] = (GAME_BG_COLOR[0]-10,GAME_BG_COLOR[1]-10,GAME_BG_COLOR[2]-10)

                                    placedTower = Tower(selected_tower.sprite.rect.x,selected_tower.sprite.rect.y,selected_tower.sprite.rect.w,selected_tower.sprite.rect.h,selected_tower.sprite.state,selected_tower.sprite.path,selected_tower.projectileSprite,selected_tower.id,selected_tower.price,selected_tower.upgradePrice,selected_tower.damage,selected_tower.upgradeDamage,selected_tower.attacksPerSecond,selected_tower.upgradedAttacksPerSecond,selected_tower.maxDistance,selected_tower.upgradedMaxDistance,territories)
                                    placedTower.sprite.rect.x = obj["x"]-GRID_SIZE
                                    placedTower.sprite.rect.y = obj["y"]-GRID_SIZE
                                    placedTowers.append(placedTower)                                           
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    hotbar_opened = True
                elif event.key == pygame.K_e:
                    for tower in placedTowers:
                        if tower.sprite.rect.collidepoint(mx,my):
                            # print(mx,my,tower.sprite.rect)
                            if tower.upgraded == False and marbies >= tower.upgradePrice:
                                marbies -= tower.upgradePrice
                                tower.upgrade()
                elif event.key == pygame.K_x:
                    for tower in list(placedTowers):
                        if tower.sprite.rect.collidepoint(mx,my):
                            marbies += tower.price/1.75
                            for obj in grid:
                                for terObj in tower.territories:
                                    if obj == terObj:
                                        obj["id"] = "0"
                                        obj["color"] = (GAME_BG_COLOR[0]+random.randint(-2,2),GAME_BG_COLOR[1]+random.randint(-2,2),GAME_BG_COLOR[2]+random.randint(-2,2))
                            placedTowers.remove(tower)
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