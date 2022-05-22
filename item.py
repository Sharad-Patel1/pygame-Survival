# Sharad Patel
# 19768944
# Item.py

# Python Libraries
import pygame

# Local files
from settings import *
from tile import Tile

############## End Imports ##############


class Item(Tile):
    '''
        Class:
        ======
        this class is in charge if the food and water

        Methods:
        ========
            - onScreen: boolean to return whether the item is on screen or not. 
    
    '''
    
    def __init__(self, x, y, number):

        super().__init__(x, y, number)
        self.image = items[number - 1]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.value = itemValues[number - 1]
        
        # Type food or water
        if number <= 5:
            self.type = 0
        else:
            self.type = 1

    def onScreen(self) -> bool:
        '''
            checks if the item is still on screen
                > removes it if not
        '''
    
        isOnScreen = False

        if self.rect.x > 0:
            isOnScreen = True

        return isOnScreen