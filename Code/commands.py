# Sharad Patel
# 19768944 
# Commands.py

# Python Libraries
import pygame

# Local Files 
from settings import *

############## End Imports ##############


class Commands:
    '''
        Class:
        ======
        This class is in charge of handling the in game commands that the user will input to change the way the game behaves
        The current commands are /day, /night to change the in game "time" to change whether the player is fighting humans or 
        zombies. 

        Methods: 
        ========
            - draw: Displaying the command line on the screen.
            - update: Update the command text to actually run the command. 
            - appendLetter: Add the letter that has been entered by the user to the command text.
            - removeLetter: Remove the last letter from the current command if the user inputs a backspace.
            - resetInput: Resetting the command text after the user executes the command, ready for the next command. 
            - makeAction: placeholder until the action comes to be able to execute.
    
    '''

    def __init__(self) -> None:
        self.x = 0
        self.width = WIDTH
        self.height = 30
        self.y = HEIGHT - self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.t = "/"
        self.text = mainFont.render(self.t, 1, BLACK)

    def draw(self, surf: pygame.Surface) -> None:
        # drawing rect into background
        pygame.draw.rect(surf, (150, 150, 150), self.rect)

        # drawing line as cursor
        pygame.draw.line(surf, BLACK, (self.x + self.text.get_width() + 5, HEIGHT - self.height + 2), (self.x + self.text.get_width() + 5, HEIGHT - 2))
        
        # blitting text onto the rect
        surf.blit(self.text, (5, self.y + self.height / 2 - self.text.get_height() / 2))
    
    def update(self) -> None:
        '''
            Updating variables
        '''

        self.text = mainFont.render(self.t, 1, BLACK)
        
    def appendLetter(self, letter: str) -> None:
        '''
            Append letter to current text
        '''

        self.t += letter
    
    def removeLetter(self) -> None:
        '''
            Remove last latter from current text
        '''

        if len(self.t) > 1:
            self.t = self.t[:-1]

    def resetInput(self) -> str:
        '''
            Returning the text
            Setting it back to None
                > done after hitting enter to execute command
        '''
        
        t = self.t
        self.t = "/"
        return t
    
    def make_action(self):
        pass