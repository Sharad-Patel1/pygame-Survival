# Sharad Patel
# 19768944
# test.py

# Python Libraries
from turtle import back
import pygame
import sys
import random
from pygame import K_ESCAPE, K_SPACE, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEWHEEL, QUIT, K_a, K_d, mixer

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

# initalise pygame
pygame.init()
pygame.font.init()
mixer.init()
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

# main function
def main():
    # Create the game clock, i.e. time in game.  
    clock = pygame.time.Clock()
    FPS = 60

    right = False
    left = False
    active = False

    # Initlaise the map, the background and command line
    map = Map()
    background = BG(bg)
    commands = Commands()

    # "Spawn" the player.
    player = Player(200, 200)

    scroll = 0
    
        
    lastTile =  CHUNK_SIZE * TILE_SIZE
    
    noiseX = CHUNK_SIZE * 4

    gunner = Gunner(800, 200)
    map.enemies.append(gunner)
    print(map.enemies)
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
                scroll = player.move(right, left, map.obstacles, map.items)
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
                        if not player.jumping:
                            player.jumping = True
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
                    
                    

if __name__ == "__main__":
    main()
