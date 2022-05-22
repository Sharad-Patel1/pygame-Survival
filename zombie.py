# Sharad Patel
# 19768944
# Bullet.py

# Python Libraries
import pygame

# Local files
from player import Player
from settings import *

############## End Imports ##############


class Zombie(Player):
    '''
        Class:
        ======
        This class is in charge of the zombies in the game.
        This class inhertis the attributes of the player class.
        The class handles the movement of the zombie, the sight, the collision detection,
        the animation of the zombie for various modes i.e. idle, moving, etc. 

        Methods:
        ========
            - draw: Display the player on the surface, main play scene, draws the zombie only if they
                    are alive otherwise shows the death animation and hides the zombie. 
            - move: The movement of the zombie in the game, and adjustments based on the location of of the player.
            - collision: Zombie collision detection, either player or chunk (the ground/platforms)
            - attack: Attack the player if he is in range, and there is no cooldown. 
            - see: Checking to see if the zombie can see the player. and returning a tuple which 
                   constis of a boolean (true/false if they see the player or not) and the direction 
                   in which they saw the player. 
            - animate: Animate and change the zombie img every time stamp to "move" the player.
            - checkOffset: Checks to see if the zombie has to turn around 
            - deathAnimation: Show the death animation if the zombie dies. 
            - alive: Checks to see if the zombie is alive. 
            - camera: Moves the objs on x axis in the opposite direction of the player with the speed 
                      of the player moving forward to give illusion of scroll effect. 
            - healthBar: Draws the rectangle above the zombie head to show their health. 
            - jump: makes the zombie jump.
    '''

    def __init__(self, x, y) -> None:
        '''
        cannot be inherited from Player
        '''
        self.x = x
        self.ix = x
        self.y = y
        self.vel = 1
        self.velUp = 0

        self.time = 0
        self.bulletCooldown = 0
        self.health = 100
        self.maxHealth = self.health
        self.scale = 2.3

        self.direction = -1
        self.damage = ZOMBIE_DAMAGE
        self.seeingDistance = 300
        self.offset = 200

        #loading in images
        self.imgs = []
        self.deaths = []

        self.scoreAdded = False

        for i in range(1, 4):
            img = pygame.image.load(f"images/enemy/walk left{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
            self.imgs.append(img)

        for i in range(1, 5):
            img = pygame.image.load(f"images/player/death/death{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale)) 
            self.deaths.append(img)

        self.img = self.imgs[0]

        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.flip = False

        self.resetted = False

    def draw(self, surf: pygame.Surface) -> None:
        '''
            Only draw if enemy is alive else death animation > then remove enemy
        '''

        if self.alive():
            maxHealth, health = self.healthBar()
            pygame.draw.rect(surf, BLUE, maxHealth)
            pygame.draw.rect(surf, PINK, health)
        
        surf.blit(pygame.transform.flip(self.img, self.flip, False), (self.x, self.y))

    def move(self, targets: list, target, daytime: str) -> None:
        '''
            Depending on whether or not zombie sees player
                > seeing distance
        '''
        if self.direction == -1:
            self.flip = True
        else:
            self.flip = False

        dx = dy = 0
        saw, inRange, direction = self.see(target, daytime)
        if saw:
            self.direction = direction
            self.vel = 3
            if inRange:
                self.vel = 0
                self.attack(target)
        else:
            if self.vel == 3:
                self.ix = self.x
            self.vel = 1
            if self.checkOffset():
                self.direction *= -1

        dx = self.vel
        dy = self.velUp

        dx, dy, obs = self.collision(targets, dx, dy)
        if obs:
            self.jump()

        self.x += dx * self.direction
        self.y += dy

        self.cooldown()
        self.animate()
        self.gravity()
        self.updateRect()

    def collision(self, targets: list, dx: int, dy: int) -> tuple:
        '''
            Edited player collision function
        '''

        obs = False

        for chunk in targets:
            for tile in chunk:
                if tile.rect.colliderect(self.x + dx, self.y, self.width, self.height):
                    dx = 0
                    obs = True
                if tile.rect.colliderect(self.x, self.y + dy, self.width, self.height):
                    if self.velUp < 0:
                        self.velUp = 0
                        dy = tile.rect.y + TILE_SIZE  - self.y
                    elif self.velUp >= 0:
                        self.velUp = 0
                        self.jumping = False
                        dy = tile.rect.y - (self.y + self.height)

        return dx, dy, obs

    def updateRect(self) -> None:
        '''
            No inheritation possible
        '''
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def attack(self, target: tuple) -> None:
        '''
            Attack the player if cooldown allows it
        '''

        if self.bulletCooldown == 0:
            target.health -= self.damage
            self.bulletCooldown = 1

    def see(self, target: Player, time) -> tuple:
        '''
            Check if zombie can see the player -> returning: seeing: bool, touching: bool, direction: int
        '''

        canSee = (False, False, self.direction)

        if time == "day":
            self.seeingDistance = 300
        else:
            self.seeingDistance = 100
        
        if self.x - self.seeingDistance < target.rect.x and self.x > target.rect.x and abs(self.y - target.rect.y) < 100:
            if self.rect.colliderect(target.rect):
                canSee = (True, True, -1)
            canSee = (True, False, -1)
        
        elif self.x + self.width + self.seeingDistance > target.rect.x and self.x < target.rect.x and abs(self.y - target.rect.y) < 100:
            if self.rect.colliderect(target.rect):
                canSee = (True, True, 1)
            canSee = (True, False, 1)

        return canSee

    def animate(self) -> None:
        '''
            Animation funciton (cannot be inherited from Player)
        '''

        self.time += 1
        if self.time < 8:
            self.img = self.imgs[0]
        elif self.time < 16:
            self.img = self.imgs[1]
        elif self.time < 24:
            self.img = self.imgs[2]
        else:
            self.time = 0

    def checkOffset(self) -> bool:
        '''
            Check if zombie has to turn around (when on patrol)
        '''

        offset = False

        if abs(self.x - self.ix) > self.offset:
            offset = True
        return offset

    def deathAnimation(self):
        ''' 
            Death animation based on time (not possible to inherit from player)
        '''
        
        if not self.resetted:
            self.rect.x = -100
            self.rect.y = -100
            self.time = 0
            self.resetted = True

        self.time += 1

        if self.time < 5:
            self.img = self.deaths[0]
        elif self.time < 10:
            self.y += 2 * self.scale
            self.img = self.deaths[1]
        elif self.time < 15:
            self.y += 2 * self.scale
            self.img = self.deaths[2]
        elif self.time < 20:
            if self.time == 15:
                self.y += 5 * self.scale
                self.x -= 3 * self.scale
            self.img = self.deaths[3]
        elif self.time > 120:
            return True

    def alive(self) -> bool:
        '''
            Check if player is alive
        '''

        isAlive = False

        if self.health > 0:
            isAlive = True

        return isAlive
   
    def camera(self, scroll: int) -> None:
        '''
            Add camera effect to object
        '''
        self.x += scroll
        self.ix += scroll
        self.rect.x += scroll

    def healthBar(self) -> tuple:
        '''
            Get healthbar and return according rect
        '''
        relHealth = (self.health / self.maxHealth) * 100
        maxHealth = pygame.Rect(self.x + self.width / 2 - self.maxHealth / 2, self.y - 20, self.maxHealth, 10)
        health = pygame.Rect(self.x + self.width / 2 - self.maxHealth / 2, self.y - 20, relHealth, 10)

        return maxHealth, health

    def jump(self) -> None:
        '''
            Jump up > change up value > gravitiy pulls object down
        '''

        self.velUp = -15


        