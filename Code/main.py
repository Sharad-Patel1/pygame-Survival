# Sharad Patel
# 19768944
# Main.py

# Python Libraries
import pygame
import sys
import random
from pygame import K_ESCAPE, K_SPACE, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEWHEEL, QUIT, K_a, K_d, mixer
from argparse import ArgumentParser

# Local files
from settings import *
from player import Player
from tile import Tile
from map import Map
from zombie import Zombie
from background import BG
from gunner import Gunner
from commands import Commands

############## End Imports ##############

# Initalise pygame
pygame.init()
pygame.font.init()
mixer.init()
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

# Normal Mode
def survivalMode(background):
    clock = pygame.time.Clock()
    FPS = 60

    right = False
    left = False
    active = False

    map = Map()
    commands = Commands()

    player = Player(200, 200)

    scroll = 0
    
    lastTile =  CHUNK_SIZE * TILE_SIZE
    
    noiseX = CHUNK_SIZE * 4

    def redrawWindow():
        WIN.fill(BLACK)

        background.draw(WIN)

        map.drawDeco(WIN)
        map.drawItems(WIN)
        map.draw(WIN)
        
        WIN.blit(mainFont.render(str(round(clock.get_fps())), 1, BLACK), (210, 0))
        
        for enemy in map.enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        pygame.display.update()

    while 1:
        clock.tick(FPS)

        daytime = background.getDaytime()

        if not active:
            if lastTile < -CHUNK_SIZE * TILE_SIZE:
                x = round((lastTile + CHUNK_SIZE * TILE_SIZE * 3) / CHUNK_SIZE / TILE_SIZE, 1) - 0.2
                chunk, deco, items = map.generateChunk(x, 0, noiseX)
                map.enemies += map.generateEnemy(x, daytime)
                map.obstacles.append(chunk)
                map.deco.append(deco)

                if items != []:
                    map.items += items

                chunk, deco, items = map.generateChunk(x, 1, noiseX)
                map.obstacles.append(chunk)
                map.deco.append(deco)
                
                if items != []:
                    map.items += items

                del map.obstacles[0]
                del map.obstacles[1]

                del map.deco[0]
                del map.deco[1]

                lastTile = -TILE_SIZE
                noiseX += CHUNK_SIZE

            lastTile += scroll

            map.camera(scroll)
            for enemy in map.enemies:
                enemy.camera(scroll)

            if player.alive():
                scroll = player.move(right, left, map.obstacles, map.items, CAMERA_LIM)
                player.moveBullets(map.obstacles, map.enemies)
                player.getDesire()
                player.foodShortage()
                player.checkShoot()
                map.items = player.itemCollision(map.items)
                if player.currentItem == 2:
                    player.attackHit(map.enemies)
            
            else:
                scroll = 0
                finished = player.deathAnimation()
                if finished:
                    pass

            for enemy in map.enemies:
                if enemy.alive():
                    enemy.move(map.obstacles, player, daytime)
                else:
                    finished = enemy.deathAnimation()
                    if finished:
                        map.enemies.remove(enemy)

            background.dayNightCycle()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_d:
                        right = True
                    elif event.key == K_a:
                        left = True
                    elif event.key == K_SPACE:
                        player.jump()
                    elif event.key == pygame.K_ESCAPE:
                        active = True

                if event.type == KEYUP:
                    if event.key == K_d:
                        right = False
                    elif event.key == K_a:
                        left = False
                if event.type == MOUSEWHEEL:
                    player.nextItem()
                
            redrawWindow()
        else:
            commands.draw(WIN)
            pygame.display.update()

            commands.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        t = commands.resetInput()
                        background.command(t)
                        active = False

                    elif event.key == pygame.K_BACKSPACE:
                        commands.removeLetter()
                    
                    elif event.unicode.isalpha():
                        commands.appendLetter(event.unicode)

# Zombie Mode
def zombieMode(background):
    clock = pygame.time.Clock()
    FPS = 60

    time = 0
    score = 0

    spawnDensity = 120

    right = False
    left = False

    map = Map()
    map.items = []
    map.enemies = []
    map.obstacles = []
    map.deco = []

    with open("level.txt", "r") as f:
        targetY = 0
        for line in f:
            chunk = []
            targetX = 0
            
            for tile in range(0, len(line), 2):
                
                if line[tile] != "0":
                    chunk.append(Tile(targetX * TILE_SIZE, targetY * TILE_SIZE, int(line[tile])))
                
                targetX += 1
            
            map.obstacles.append(chunk)
            targetY += 1

    background.setDaytime("night")

    commands = Commands()

    player = Player(200, 200)

    kills = mainFont.render("Kills: " + str(score), 1, BLACK)

    def redrawWindow():
        background.draw(WIN)

        map.drawDeco(WIN)
        map.draw(WIN)

        WIN.blit(mainFont.render(str(round(clock.get_fps())), 1, BLACK), (210, 0))
        WIN.blit(kills, (WIDTH - kills.get_width(), 0))
        
        for enemy in map.enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        pygame.display.update()

    while 1:
        clock.tick(FPS)

        kills = mainFont.render("Kills: " + str(score), 1, BLACK)

        if player.alive():
            player.move(right, left, map.obstacles, map.items, 0)
            player.moveBullets(map.obstacles, map.enemies)
            player.checkShoot()
            
            if player.currentItem == 2:
                player.attackHit(map.enemies)
        
        else:
            finished = player.deathAnimation()
            if finished:
                pass
    
        for enemy in map.enemies:
            if enemy.alive():
                enemy.move(map.obstacles, player, "day")
            else:
                finished = enemy.deathAnimation()
                if not enemy.scoreAdded:
                    score += 1
                    enemy.scoreAdded = True
                if finished:
                    map.enemies.remove(enemy)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_d:
                    right = True
                elif event.key == K_a:
                    left = True
                elif event.key == K_SPACE:
                    player.jump()
                elif event.key == pygame.K_ESCAPE:
                    active = True

            if event.type == KEYUP:
                if event.key == K_d:
                    right = False
                elif event.key == K_a:
                    left = False
            if event.type == MOUSEWHEEL:
                player.nextItem()        

        redrawWindow()

        # generate enemies
        if time >= spawnDensity:
            enem = map.spawnEnemy(0, WIDTH, 1, "zombie")
            for e in enem:
                e.seeingDistance = 900
            map.enemies += map.spawnEnemy(0, WIDTH, 1, "zombie")
            time = 0
            if spawnDensity > 45:
                spawnDensity -= 1

        time += 1

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--day", action="store_true", help="Set Daytime to Day")
    parser.add_argument("-n", "--night", action="store_true", help="Set Daytime to Night")
    parser.add_argument("-z", "--zombie", action="store_true", help="Set Mode to Zombie Mode")

    args, leftovers = parser.parse_known_args()

    background = BG(bg)

    if args.night:
        background.command("/night")
    
    if args.zombie:
        zombieMode(background)
    
    else:
        survivalMode(background)
