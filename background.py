# Sharad Patel
# 19768944
# Background.py 

# Python libraries 
import pygame

# Local files
from settings import *

############## End Imports ##############


class BG(pygame.sprite.Sprite):

    '''
        Class:
        ======
        This class is in charge of handling the creation and display of the background of the game.
        The class also handles the view for the in game commands that the player can type to change the game mode. 

        Methods:
        ========
            - draw: Displays the bg on the main surface. 
            - dayNightCycle: The day night cycle changes the background based on the "time" ingame
            - command: This displays a different background based on the input from the command the user inputs. 
            - getDaytime: This changes the bg based on the "time" ingame. 
            - setDaytime: This sets the background of the game to be the either day or night. 

    '''

    def __init__(self, image):
        super().__init__()

        #load images
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        
        # current time
        self.time = 0
    
    def draw(self, surf):
        ''' 
            Display the bg onto the main surface
        '''
        surf.blit(self.image, self.rect)

    def dayNightCycle(self) -> None:
        '''
            Change background based on current time
        '''
        self.time += 1
        if self.time > 1800:
            self.image = night
        elif self.time > 2600:
            self.image = bg
            self.time = 0

    def command(self, command: str) -> None:
        '''
            Adjust background based on command
        '''
        
        if command == "/night":
            self.setDaytime("night")
        elif command == "/day":
            self.setDaytime("day")

    def getDaytime(self) -> str:
        dayOrNight = "night"

        if self.time < 1800:
            dayOrNight = "day"
        
        return dayOrNight

    def setDaytime(self, daytime) -> None:
        
        if daytime == "night":
            self.image = night
            self.time = 1800

        elif daytime == "day":
            self.image = bg
            self.time = 0