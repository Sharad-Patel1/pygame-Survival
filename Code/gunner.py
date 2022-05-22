# Sharad Patel
# 19768944
# Gunner.py

# Python Libraries
import pygame

# Local files
from settings import *
from bullet import Bullet
from player import Player

############## End Imports ##############


class Gunner(Player):
    '''
        Class:
        ======
        This class is in charge of the human enemies in the game. 
        This class inherits the attributes of the player class. 
        The class handles the movement of the enemy, the sight, the collision detection,
        the animation of the enemy for various modes i.e. idle, moving shooting, etc. 
        
        Methods:
        ========
            - move: The movement of the enemy in game, and adjustments based on location of the player. 
            - collision: Enemy collision detection, either player or chunk (the ground/platforms)
            - animate: Animate and change the enemy img every time stamp to "move" the player.
            - see: Checking to see if the gunner can see the player. and returning a tuple which 
                   consists of a boolean (true/false if they see the player or not) and the direction 
                   in which they saw the player. 
            - shoot: Shoot the player if they see the gunner sees player. 
            - camera: Moves the objs on x axis in the opposite direction of the player with the speed 
                      of the player moving forward to give illusion of scroll effect. 
            - draw: Display the player on the surface, main play scene, draws the gunner only if they
                    are alive otherwise shows the death animation and hides the gunner. 
            - healthBar: Draws the rectangle above the gunners head to show their health. 

    '''

    SHOOT_COOL = GUNNER_COOLDOWN

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.vel = 2
        self.ix = x
        self.patrolOffset = 400
        self.scale = 2.2

        self.imgs = []
        self.current = 0
        animations = ["run", "death"]

        for animation in animations:
            l = []
            
            for i in range(1,5):
                img = pygame.image.load(f"images/enemy/{animation}/{animation}{i}.png")
                img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
                l.append(img)
            
            self.imgs.append(l)

        # gunner standing
        img = pygame.image.load(f"images/enemy/stand/standing.png")
        img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale)) 
        self.imgs.append([])
        
        for i in range(4):
            self.imgs[2].append(img)

    def move(self, targets: list, target: Player, daytime: int) -> None:
        '''
            Adjusted player move function > not inherited
        '''
        dx = 0
        dy = 0

        if abs(self.x - self.ix) > self.patrolOffset:
            self.direction *= -1

        dx += self.vel * self.direction

        self.flip = False if self.direction == 1 else True
        
        self.gravity()

        dy += self.velUp

        dx, dy, obs = self.collision(targets, dx, dy)

        if obs:
            self.direction *= -1

        saw, dir = self.see(target, daytime)
        if saw:
            self.direction = dir
            self.ix = self.x
            self.shoot()
            self.current = 2
            dx = 0
        else:
            self.current = 0
            

        self.x += dx
        self.y += dy

        self.time += 1

        self.animate()
        self.updateRect()
        self.moveBullets(targets, [target])

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

    def animate(self) -> None:
        '''
            Animate the player every frame
        '''

        if self.time < 10:
            self.img = self.imgs[self.current][0]
        
        elif self.time < 20:
            self.img = self.imgs[self.current][1]
        
        elif self.time < 30:
            self.img = self.imgs[self.current][2]
        
        elif self.time < 40:
            self.img = self.imgs[self.current][3]
        
        else:
            self.time = 0

    def see(self, target: Player, time) -> tuple:
        '''
            Check if gunner can see the player -> returning: seeing: bool, direction: int
        '''

        canSee = (False, self.direction)

        if time == "day":
            self.seeingDistance = 500
        else:
            self.seeingDistance = 100
        if self.x - self.seeingDistance < target.rect.x and self.x > target.rect.x and abs(self.y - target.rect.y) < 75:
            canSee = (True, -1)
        elif self.x + self.width + self.seeingDistance > target.rect.x and self.x < target.rect.x and abs(self.y - target.rect.y) < 75:
            canSee = (True, 1)

        return canSee

    def shoot(self) -> None:
        '''
            Adjusted
        '''

        if self.bulletCooldown == 0:
            if self.direction == -1:
                bullet = Bullet(self.x + 14 * self.scale, self.y + 13 * self.scale, self.direction, GUNNER_DAMAGE)
            else:
                bullet = Bullet(self.x - 4 * self.scale, self.y + 13 * self.scale, self.direction, GUNNER_DAMAGE)
            self.bullets.append(bullet)
            self.bulletCooldown = 1

    def camera(self, scroll):
        
        self.x += scroll
        self.ix += scroll

    def draw(self, surf: pygame.Surface) -> None:
        '''
            Only draw if gunner is alive else death animation > then remove gunner
        '''

        if self.alive():
            maxHealth, health = self.healthBar()
            pygame.draw.rect(surf, BLUE, maxHealth)
            pygame.draw.rect(surf, PINK, health)

        surf.blit(pygame.transform.flip(self.img, self.flip, False), (self.x, self.y))

        for bullet in self.bullets:
            bullet.draw(surf)


    def healthBar(self) -> tuple:
        '''
            Returns Rects to draw health bar
        '''

        relHealth = (self.health / self.maxHealth) * 100
        maxHealth = pygame.Rect(self.x + self.width / 2 - self.maxHealth / 2, self.y - 20, self.maxHealth, 10)
        health = pygame.Rect(self.x + self.width / 2 - self.maxHealth / 2, self.y - 20, relHealth, 10)

        return maxHealth, health

