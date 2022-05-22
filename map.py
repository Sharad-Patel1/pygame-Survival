# Sharad Patel
# 19768944
# Map.py

# Python Libraries
from curses.ascii import RS
import pygame
import random
import noise

# Local Files 
from settings import *
from tile import Tile
from item import Item
from zombie import Zombie
from gunner import Gunner

############## End Imports ##############

class Map:
    '''
        Class:
        ======
        This class handles any and all things related to the map. 
        The file handles the "Spawning" of elements on the map. i.e. display all the objects on the map. 

        Methods:
        ========
            - generateChunk: Generate the platforms in the map, randomly. 
            - generateEnemy: Spawns the enemies on the map.
            - loadMap: Generating the initial start point of the map, the place where the game begins. 
            - draw: Displaying all the tiles to the scene. 
            - drawDeco: Displaying all the map decoration, the lamposts and rocks etc. 
            - drawItems: Displaying all the food and water items. 
            - camera: Moving all the objects in the scene to the left, to give illusion of player moving on screen.
    
    '''

    def __init__(self) -> None:
        self.map = []
        self.obstacles = []
        self.items = []
        self.deco = []
        self.enemies = []
        self.loadMap()

    def generateChunk(self, x: float, y: float, noiseX: int): #! improve
        '''
            Generates chunk with x and y value
            NoiseX: x value for 1d noise map gen
        '''

        chunk = []
        items = []
        chunkDeco = []
        nX = noiseX
        maxHeight = 8
        
        for yPos in range(CHUNK_SIZE):
            nX = noiseX

            for xPos in range(CHUNK_SIZE):
                targetX = x * CHUNK_SIZE + xPos
                targetY = y * CHUNK_SIZE + yPos
                height = int(noise.pnoise1(nX * 0.1, repeat=999999) * 4)
                maxHeight = min(7 - height, maxHeight)
                
                nX += 1
                
                if targetY > 7 - height:
                    chunkDeco.append(Tile(targetX * TILE_SIZE, targetY * TILE_SIZE , 2))
                
                elif targetY == 7 - height:
                    chunk.append(Tile(targetX * TILE_SIZE, targetY * TILE_SIZE, 1))
                
                elif targetY == 5 - height:
                    r = random.randint(1, 20)
                    if r <= 3:
                        chunkDeco.append(Tile(targetX * TILE_SIZE, targetY * TILE_SIZE + TILE_SIZE * 1.5, random.randint(12, 14)))
                    elif r == 5:
                        chunkDeco.append(Tile(targetX * TILE_SIZE, (targetY) * TILE_SIZE, 17))
                    elif r == 6:
                        chunkDeco.append(Tile(targetX * TILE_SIZE, targetY * TILE_SIZE + TILE_SIZE, 18))
                    elif r == 7:
                        pass
                        #enemies.append(Zombie())
                
                elif targetY == 6 - height:
                    r = random.randint(1, 3)
                    if r <= 2:
                        chunkDeco.append(Tile(targetX * TILE_SIZE, targetY * TILE_SIZE + TILE_SIZE * 0.76, random.randint(9, 11)))
                
                elif targetY == 4 - height:
                    if xPos == CHUNK_SIZE - 1:
                        r = random.randint(1, 2)
                        if r == 1:
                            yR = random.randint(2, 4)
                            rSize = random.randint(0, 4)
                            p = targetX - CHUNK_SIZE + random.randint(0, CHUNK_SIZE - rSize - 2)

                            chunk.append(Tile(p * TILE_SIZE + 5, maxHeight * TILE_SIZE - (TILE_SIZE * yR), 3))
                            i = 0
                            for i in range(rSize):
                                chunk.append(Tile(p * TILE_SIZE + (TILE_SIZE * (i + 1)), maxHeight * TILE_SIZE - (TILE_SIZE * yR), 1))
                            chunk.append(Tile(p * TILE_SIZE + (TILE_SIZE * (i + 1)), maxHeight * TILE_SIZE - (TILE_SIZE * yR), 4))
                            items.append(Item(p * TILE_SIZE + (TILE_SIZE * (i)), maxHeight * TILE_SIZE - (TILE_SIZE * (yR + 0.5)), random.randint(1, ITEMS)))


        return chunk, chunkDeco, items

    def generateEnemy(self, x: float, daytime: str) -> list:
        '''
            Generate enemies in new chunk
        '''

        enemies = []
        
        # get daytime > for how many enemies can spawn in one chunk
        if daytime == "night":
            r = random.randint(0, 5)
        else:
            r = random.randint(0, 2)
        
        # spawn every enemy at random pos in chunk based on daytime
        for _i in range(r):
            if daytime == "night":
                enemies.append(Zombie(x * CHUNK_SIZE * TILE_SIZE + random.randint(0, CHUNK_SIZE * TILE_SIZE), TILE_SIZE * 2))
            else:
                enemies.append(Gunner(x * CHUNK_SIZE * TILE_SIZE + random.randint(0, CHUNK_SIZE * TILE_SIZE), TILE_SIZE * 2))
        
        return enemies

    
    def loadMap(self) -> None:
        '''
            Loding the first chunks and generating map
        '''
        
        for x in range(4):
            for y in range(2):
                chunkObs, chunkDeco, items = self.generateChunk(x, y, x * CHUNK_SIZE)
                if x != 0:
                    self.enemies += self.generateEnemy(x, y)
                self.obstacles.append(chunkObs)
                self.deco.append(chunkDeco)
                if items:
                    self.items += items

    def draw(self, surf: pygame.Surface) -> None:
        '''
            Drawing all tiles
        '''

        for chunk in self.obstacles:
                for tile in chunk:
                    tile.draw(surf)

    def drawDeco(self, surf: pygame.Surface) -> None:
        '''
            Drawing all decoration
        '''

        for chunk in self.deco:
                for tile in chunk:
                    tile.draw(surf)

    def drawItems(self, surf: pygame.Surface) -> None:
        '''
            Drawing all items
        '''

        for tile in self.items:
            if tile.onScreen():
                tile.draw(surf) 
            else:
                self.items.remove(tile)
    
    def camera(self, scroll: None) -> None:
        '''
            Adding camera effect for every map object
        '''
        
        for chunk in self.obstacles:
            for tile in chunk:
                tile.rect.x += scroll

        for chunk in self.deco:
            for tile in chunk:
                tile.rect.x += scroll

        for item in self.items:
            item.rect.x += scroll

    def spawnEnemy(self, spawnRangeA: int, spawnRangeB: int, i: int, t: str) -> list:
        enemies = []
        for _i in range(i):
            if t == "zombie":
                enemies.append(Zombie(random.randint(spawnRangeA, spawnRangeB), -200))
            else:
                enemies.append(Gunner(random.randint(spawnRangeA, spawnRangeB), -200))
        return enemies