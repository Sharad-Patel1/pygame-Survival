# Sharad Patel
# 19768944
# Bullet.py

# Python Libraries
import pygame

# Local files
from settings import *

############## End Imports ##############


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, number) -> None:
        super().__init__()
        self.image = tiles[number - 1]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surf: pygame.Surface) -> None:
        surf.blit(self.image, self.rect)