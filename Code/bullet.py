# Sharad Patel
# 19768944
# Bullet.py

# Python Libraries
import pygame

# Local files 
from settings import *

############## End Imports ##############


class Bullet:
    '''
        Class:
        ======
        This class is in charge of handling the creation display and the physics of the bullet. 
        The class handles the movement and collision detection of the bullet. 

        Methods:
        ========
            - draw: Displays the bullet onto the main surface.
            - move: This method handles the movement of the bullet in game, checking to see if it collides with anything. 
            - offScreen: This methods checks to see if the bullet has travelled off screen. 
            - camera: this method checks to see if the surface i.e. the player is moving in game and adds that to the movement 
                      of the bullet so the physics make sense. 
    '''

    def __init__(self, x: int, y: int, direction: int, damage: int) -> None:
        self.x = x
        self.y = y
        self.vel = 30
        self.damage = damage
        self.img = BULLET

        self.direction = direction

        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def draw(self, surf: pygame.Surface) -> None:
        surf.blit(self.img, (self.x, self.y))

    def move(self, obstacles: list, targets: list) -> bool:
        '''
            Moving the bullet
            Collison check with enemy or tile. 
        '''
        
        isOffScreen = False

        self.x += self.vel * self.direction
        self.rect.x = self.x
        if self.offScreen():
            isOffScreen = True
        else: 
            isOffScreen = False
        
        for target in targets:
            if self.rect.colliderect(target.rect):
                target.health -= self.damage
                isOffScreen = True
            else:
                isOffScreen = False

        
        for row in obstacles:
            for obstacle in row:
                if self.rect.colliderect(obstacle.rect):
                    isOffScreen = True
                else: 
                    isOffScreen = False

        return isOffScreen

    def offScreen(self) -> bool:
        '''
            Check if bullet went off screen
        '''

        isOffScreen = False

        if self.x > WIDTH or self.x < 0:
            isOffScreen = True
 
        return isOffScreen

    def camera(self, scroll: int) -> None:
        ''' 
            Adjusting bullet according to camera
        ''' 

        self.x += scroll
        self.rect.x += scroll