import pygame
import random
from button import Button
from tower import Tower
from enemy import Enemy
from config import *
import math
from utils import loadLevel,generateWave,lookAt,calculateDistance,projectileLookAt,rotate

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
summonTimerTimes = 0
summonTimer = 0
summonTimerNeedTimes = 0
waveTimer = FPS*40
basicFont = pygame.font.SysFont("Comic Sans MS",15)
smallBasicFont = pygame.font.SysFont("Comic Sans MS",10)
largeBasicFont = pygame.font.SysFont("Comic Sans MS",45)
infoText1 = largeBasicFont.render("Controls:",True,(150,150,150))
infoText2 = largeBasicFont.render("E - Upgrade tower",True,(150,150,150))
infoText3 = largeBasicFont.render("X - Sell tower",True,(150,150,150))
infoText4 = largeBasicFont.render("TAB - Open/Close Hotbar (Hold)",True,(150,150,150))
infoText5 = basicFont.render("By FurPuro (Main Devoloper) & sazin66644 (j.Designer)",True,(150,150,150))
infoText6 = largeBasicFont.render(f"Max Towers - {MAX_TOWERS}",True,(150,150,150))
infoText7 = largeBasicFont.render("R - Skip wave",True,(150,150,150))

background = pygame.image.load(fr"{IMAGES_DIR}\MenuBackground.png")
background = pygame.transform.scale(background,(WIDTH,HEIGHT))

playbutton = Button(WIDTH/2-240/2,HEIGHT/2-120/2,240,120,"menu",rf"{IMAGES_DIR}\playButton.png",rf"""
grid = loadLevel()
wave = 0
marbies = START_MARBIES
summonTimerTimes = 0
summonTimer = 0
summonTimerNeedTimes = 0
projectiles.clear()
waveTimer = FPS*40
castle_health = CASTLE_MAX_HEALTH
game_state = 'game'
""")
shopbutton = Button(WIDTH/2-270,HEIGHT/2-90/2,90,90,"menu",rf"{IMAGES_DIR}\shopButton.png",rf"""
game_state = 'shop'
""")
returnbutton = Button(5,5,30,30,"shop",rf"{IMAGES_DIR}\returnButton.png",rf"""
game_state = 'menu'
""")
returnbutton2 = Button(5,5,30,30,"info",rf"{IMAGES_DIR}\returnButton.png",rf"""
game_state = 'menu'
""")
infobutton = Button(WIDTH/2+180,HEIGHT/2-90/2,90,90,"menu",rf"{IMAGES_DIR}\infoButton.png",rf"""
game_state = 'info'
""")

playbutton.sprite.display = pygame.transform.scale(playbutton.sprite.display,(playbutton.sprite.rect.w,playbutton.sprite.rect.h))
shopbutton.sprite.display = pygame.transform.scale(shopbutton.sprite.display,(shopbutton.sprite.rect.w,shopbutton.sprite.rect.h))
returnbutton.sprite.display = pygame.transform.scale(returnbutton.sprite.display,(returnbutton.sprite.rect.w,returnbutton.sprite.rect.h))
returnbutton2.sprite.display = pygame.transform.scale(returnbutton2.sprite.display,(returnbutton2.sprite.rect.w,returnbutton2.sprite.rect.h))
infobutton.sprite.display = pygame.transform.scale(infobutton.sprite.display,(infobutton.sprite.rect.w,infobutton.sprite.rect.h))

bowTower = Tower(0,0,90,90,"none",fr"{IMAGES_DIR}\bowTurret.png",fr"{IMAGES_DIR}\arrow.png","bow",125,250,1,2,1,1.5,180,240,[])
cannonTower = Tower(0,0,90,90,"none",fr"{IMAGES_DIR}\cannonTurret.png",fr"{IMAGES_DIR}\core.png","cannon",200,325,4,3,2,1.25,240,300,[])
piqueTower = Tower(0,0,90,90,"none",fr"{IMAGES_DIR}\piqueTurret.png",fr"{IMAGES_DIR}\piqueProjectile.png","pique",150,275,0.5,1,0.75,1,120,150,[])
staffTower = Tower(0,0,90,90,"none",fr"{IMAGES_DIR}\staffTurret.png",fr"{IMAGES_DIR}\magicalProjectile.png","staff",230,400,3,4,1.8,1.7,180,240,[])
farmTower = Tower(0,0,90,90,"none",fr"{IMAGES_DIR}\farmTurret.png",fr"{IMAGES_DIR}\none.png","farm",100,300,0,0,5,4,0,0,[])

towersTimer = {}
projectiles = {}
slownessTimer = {}

shopTowers = []

shopTowers.append(cannonTower)
shopTowers.append(piqueTower)
shopTowers.append(staffTower)
shopTowers.append(farmTower)

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
save.close()

basicZombie = Enemy(0,0,60,60,"none",fr"{IMAGES_DIR}\basicZombie.png","basicZombie",2,13,False)
fastZombie = Enemy(0,0,60,60,"none",fr"{IMAGES_DIR}\fastZombie.png","fastZombie",3,8,False)
heavyZombie = Enemy(0,0,60,60,"none",fr"{IMAGES_DIR}\heavyZombie.png","heavyZombie",1,40,False)
basicBossZombie = Enemy(0,0,90,90,"none",fr"{IMAGES_DIR}\basicBossZombie.png","basicBossZombie",2,120,False)

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
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.sprite.rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]) and button.sprite.state == game_state:
                        exec(button.code)
    elif game_state == "shop":
        screen.fill(MENU_BG_COLOR)
        goldText = basicFont.render(f"GOLD: {gold}",True,WHITE)
        
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
            if tower.id == "staff":
                text5 = smallBasicFont.render(f"GOLD PRICE: 4200",True,(0,255,255))
            if tower.id == "farm":
                text5 = smallBasicFont.render(f"GOLD PRICE: 1600",True,(0,255,255))
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
                quit()
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
                        if have_this == False and tower.id == "staff":
                            if gold >= 4200:
                                gold -= 4200
                                selected_tower = Tower(tower.sprite.rect.x,tower.sprite.rect.y,tower.sprite.rect.w,tower.sprite.rect.h,tower.sprite.state,tower.sprite.path,tower.projectileSprite.path,tower.id,tower.price,tower.upgradePrice,tower.damage,tower.upgradeDamage,tower.attacksPerSecond,tower.upgradedAttacksPerSecond,tower.maxDistance,tower.upgradedMaxDistance,tower.territories)
                                equippedTowers.append(selected_tower)
                        if have_this == False and tower.id == "farm":
                            if gold >= 1600:
                                gold -= 1600
                                selected_tower = Tower(tower.sprite.rect.x,tower.sprite.rect.y,tower.sprite.rect.w,tower.sprite.rect.h,tower.sprite.state,tower.sprite.path,tower.projectileSprite.path,tower.id,tower.price,tower.upgradePrice,tower.damage,tower.upgradeDamage,tower.attacksPerSecond,tower.upgradedAttacksPerSecond,tower.maxDistance,tower.upgradedMaxDistance,tower.territories)
                                equippedTowers.append(selected_tower)
    elif game_state == "info":
        screen.fill(MENU_BG_COLOR)

        screen.blit(infoText1, (30,30+largeBasicFont.get_linesize()*0,infoText1.get_rect().w,infoText1.get_rect().h))
        screen.blit(infoText2, (60,30+largeBasicFont.get_linesize()*1,infoText2.get_rect().w,infoText2.get_rect().h))
        screen.blit(infoText3, (60,30+largeBasicFont.get_linesize()*2,infoText3.get_rect().w,infoText3.get_rect().h))
        screen.blit(infoText4, (60,30+largeBasicFont.get_linesize()*3,infoText4.get_rect().w,infoText4.get_rect().h))
        screen.blit(infoText5, (WIDTH-infoText5.get_width(),HEIGHT-basicFont.get_linesize()*1,infoText5.get_rect().w,infoText5.get_rect().h))
        screen.blit(infoText6, (30,30+largeBasicFont.get_linesize()*5,infoText6.get_rect().w,infoText6.get_rect().h))
        screen.blit(infoText7, (60,30+largeBasicFont.get_linesize()*4,infoText7.get_rect().w,infoText7.get_rect().h))

        for event in pygame.event.get():
            mx,my = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.sprite.rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]) and button.sprite.state == game_state:
                        exec(button.code)
    elif game_state == "game":
        screen.fill(GAME_BG_COLOR)
        waveMobs = None
        waveMobs = generateWave(wave)
        marbiesText = basicFont.render(f"MARBIES: {round(marbies,1)}",True,WHITE)
        healthText = basicFont.render(f"CASTLE HEALTH: {castle_health}",True,WHITE)
        goldText = basicFont.render(f"GOLD: {gold}",True,WHITE)
        wavesText = basicFont.render(f"WAVE: {wave}",True,WHITE)
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
                    if pygame.rect.Rect(enemy.sprite.rect.centerx-3,enemy.sprite.rect.centery-3,4,4).collidepoint(obj["x"]+GRID_SIZE/2,obj["y"]+GRID_SIZE/2): # enemy.sprite.rect.centerx >= obj["x"]+GRID_SIZE/2 and enemy.sprite.rect.centery >= obj["y"]+GRID_SIZE/2 and enemy.sprite.rect.centerx <= obj["x"]+GRID_SIZE and enemy.sprite.rect.centery <= obj["y"]+GRID_SIZE and enemy.sprite.rect.centerx >= 0 and enemy.sprite.rect.centery >= 0 and enemy.sprite.rect.centerx <= WIDTH and enemy.sprite.rect.centery <= HEIGHT:
                        if obj != None:
                            if obj["id"] == "5":
                                enemy.changeSpeed(enemy.walkSpeed,0)
                                rotate(enemy.sprite,90)
                            elif obj["id"] == "6":
                                enemy.changeSpeed(0,enemy.walkSpeed)
                                rotate(enemy.sprite,0)
                            elif obj["id"] == "7":
                                enemy.changeSpeed(0,-enemy.walkSpeed)
                                rotate(enemy.sprite,180)
                            elif obj["id"] == "8":
                                enemy.changeSpeed(-enemy.walkSpeed,0)
                                rotate(enemy.sprite,-90)
                            elif obj["id"] == "3":
                                castle_health -= enemy.health
                                enemy.sprite.rect.x = 0
                                enemy.sprite.rect.y = 0
                                enemiesOnMap.remove(enemy)

        if castle_health <= 0:
            enemiesOnMap.clear()
            placedTowers.clear()
            game_state = "menu"

        waveTimer += 1
        summonTimer += 1

        if slownessTimer:
            for enemy in enemiesOnMap:
                if enemy in slownessTimer:
                    slownessTimer[enemy] += 1
                    if enemy.speed[0] == 0 and enemy.speed[1] != 0:
                        if enemy.speed[1] > 0:
                            enemy.changeSpeed(0,enemy.defaultWalkSpeed-1/enemy.speed[1]*enemy.speed[1])
                        else:
                            enemy.changeSpeed(0,-(enemy.defaultWalkSpeed-1)/enemy.speed[1]*enemy.speed[1])
                    elif enemy.speed[1] == 0 and enemy.speed[0] != 0:
                        if enemy.speed[0] > 0:
                            enemy.changeSpeed(enemy.defaultWalkSpeed-1/enemy.speed[0]*enemy.speed[0],0)
                        else:
                            enemy.changeSpeed(-(enemy.defaultWalkSpeed-1)/enemy.speed[0]*enemy.speed[0],0)
                    elif enemy.speed[0] != 0 and enemy.speed[1] != 0:
                        if enemy.speed[1] > 0:
                            enemy.changeSpeed(enemy.speed[0],enemy.defaultWalkSpeed-1/enemy.speed[1]*enemy.speed[1])
                        else:
                            enemy.changeSpeed(enemy.speed[0],-(enemy.defaultWalkSpeed-1)/enemy.speed[1]*enemy.speed[1])
                        if enemy.speed[0] > 0:
                            enemy.changeSpeed(enemy.defaultWalkSpeed-1/enemy.speed[0]*enemy.speed[0],enemy.speed[1])
                        else:
                            enemy.changeSpeed(-(enemy.defaultWalkSpeed-1)/enemy.speed[0]*enemy.speed[0],enemy.speed[1])
                    if slownessTimer[enemy] >= FPS/3:
                        slownessTimer[enemy] = 0
                        if enemy.speed[0] == 0 and enemy.speed[1] != 0:
                            if enemy.speed[1] > 0:
                                enemy.changeSpeed(0,enemy.defaultWalkSpeed)
                            else:
                                enemy.changeSpeed(0,-enemy.defaultWalkSpeed)
                        elif enemy.speed[1] == 0 and enemy.speed[0] != 0:
                            if enemy.speed[0] > 0:
                                enemy.changeSpeed(enemy.defaultWalkSpeed,0)
                            else:
                                enemy.changeSpeed(-enemy.defaultWalkSpeed,0)
                        elif enemy.speed[0] != 0 and enemy.speed[1] != 0:
                            if enemy.speed[1] > 0:
                                enemy.changeSpeed(enemy.speed[0],enemy.defaultWalkSpeed)
                            else:
                                enemy.changeSpeed(enemy.speed[0],-enemy.defaultWalkSpeed)
                            if enemy.speed[0] > 0:
                                enemy.changeSpeed(enemy.defaultWalkSpeed,enemy.speed[1])
                            else:
                                enemy.changeSpeed(-enemy.defaultWalkSpeed,enemy.speed[1])
                            
                        slownessTimer.pop(enemy)

        for tower in placedTowers:
            tower.sprite.draw(screen)
        if towersTimer:
            for projectile in projectiles:
                projectile.draw(screen) 
            for tower in placedTowers:
                key = f"{tower.sprite.rect.x} {tower.sprite.rect.y}"
                projectile = tower.projectileSprite
                if projectile in projectiles:
                    if projectile.rect.colliderect(projectiles[projectile][0]-GRID_SIZE/3,projectiles[projectile][1]-GRID_SIZE/3,projectiles[projectile][0]+GRID_SIZE/3,projectiles[projectile][1]+GRID_SIZE/3):
                        projectiles.pop(projectile)
                    else:
                        dx, dy = (projectiles[projectile][0] - projectile.rect.centerx, projectiles[projectile][1] - projectile.rect.centery)
                        stepx, stepy = (dx / FPS*2.5, dy / FPS*2.5)
                        projectile.rect.x += stepx
                        projectile.rect.y += stepy

                if key in towersTimer:
                    towersTimer[key] += 1
                    if towersTimer[key] >= tower.attacksPerSecond*FPS:
                        if tower.id != "farm":
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
                                if tower.id == "cannon":
                                    for enemy in enemies:
                                        if enemy.sprite.rect.colliderect(targetEnemy.sprite.rect.x-60,targetEnemy.sprite.rect.y-60,targetEnemy.sprite.rect.x+60,targetEnemy.sprite.rect.y+60):
                                            enemy.health -= tower.damage
                                else:
                                    targetEnemy.health -= tower.damage
                                if tower.id == "pique" and tower.upgraded == True:
                                    slownessTimer[targetEnemy] = 0
                                if projectile not in projectiles:
                                    projectiles[projectile] = (targetEnemy.sprite.rect.centerx,targetEnemy.sprite.rect.centery)
                                    projectile.rect.centerx = tower.sprite.rect.centerx
                                    projectile.rect.centery = tower.sprite.rect.centery
                                    projectileLookAt(tower.projectileSprite,targetEnemy.sprite)
                                lookAt(tower.sprite,targetEnemy.sprite)
                        else:
                            towersTimer[key] = 0
                            if tower.upgraded == False:
                                marbies += 12.5
                            else:
                                marbies += 25

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
                    screen.blit(text1, (tower.sprite.rect.x,tower.sprite.rect.y+smallBasicFont.get_linesize()*0,text1.get_rect().w,text1.get_rect().h))
                    screen.blit(text2, (tower.sprite.rect.x,tower.sprite.rect.y+smallBasicFont.get_linesize()*1,text2.get_rect().w,text2.get_rect().h))
                    screen.blit(text3, (tower.sprite.rect.x,tower.sprite.rect.y+smallBasicFont.get_linesize()*2,text3.get_rect().w,text3.get_rect().h))
                    screen.blit(text4, (tower.sprite.rect.x,tower.sprite.rect.y+smallBasicFont.get_linesize()*3,text4.get_rect().w,text4.get_rect().h))
        screen.blit(marbiesText, (0,HEIGHT-basicFont.get_linesize(),marbiesText.get_rect().w,marbiesText.get_rect().h))
        screen.blit(healthText, (0,HEIGHT-basicFont.get_linesize()*2,healthText.get_rect().w,healthText.get_rect().h))
        screen.blit(goldText, (0,HEIGHT-basicFont.get_linesize()*3,goldText.get_rect().w,goldText.get_rect().h))
        screen.blit(wavesText, (0,HEIGHT-basicFont.get_linesize()*4,wavesText.get_rect().w,wavesText.get_rect().h))
        for event in pygame.event.get():
            mx,my = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for tower in equippedTowers:
                    if tower.sprite.rect.collidepoint(mx,my) and hotbar_opened == True:
                        selected_tower = Tower(tower.sprite.rect.x,tower.sprite.rect.y,tower.sprite.rect.w,tower.sprite.rect.h,tower.sprite.state,tower.sprite.path,tower.projectileSprite.path,tower.id,tower.price,tower.upgradePrice,tower.damage,tower.upgradeDamage,tower.attacksPerSecond,tower.upgradedAttacksPerSecond,tower.maxDistance,tower.upgradedMaxDistance,tower.territories)
                if selected_tower != None and hotbar_opened == False and len(placedTowers) < MAX_TOWERS:
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
                                                        obj2["color"] = (obj2["color"][0]-10,obj2["color"][1]-10,obj2["color"][2]-10)

                                    placedTower = Tower(selected_tower.sprite.rect.x,selected_tower.sprite.rect.y,selected_tower.sprite.rect.w,selected_tower.sprite.rect.h,selected_tower.sprite.state,selected_tower.sprite.path,selected_tower.projectileSprite.path,selected_tower.id,selected_tower.price,selected_tower.upgradePrice,selected_tower.damage,selected_tower.upgradeDamage,selected_tower.attacksPerSecond,selected_tower.upgradedAttacksPerSecond,selected_tower.maxDistance,selected_tower.upgradedMaxDistance,territories)
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
                elif event.key == pygame.K_r:
                    if summonTimerTimes == summonTimerNeedTimes:
                        waveTimer = 45*FPS
                elif event.key == pygame.K_x:
                    for tower in list(placedTowers):
                        if tower.sprite.rect.collidepoint(mx,my):
                            marbies += tower.price/1.75
                            for obj in grid:
                                for terObj in tower.territories:
                                    if obj == terObj:
                                        obj["id"] = "0"
                                        obj["color"] = (obj["color"][0]+10,obj["color"][1]+10,obj["color"][2]+10)
                            if tower.projectileSprite in projectiles:
                                projectiles.pop(tower.projectileSprite)
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