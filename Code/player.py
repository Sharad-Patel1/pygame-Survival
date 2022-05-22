# Sharad Patel
# 19768944
# Bullet.py

# Python Libraries
import pygame

# Local files 
from tile import Tile
from settings import *
from bullet import Bullet

############## End Imports ##############


class Player:

    # CONSTANTS
    COOLDOWN = 60
    GRAVITY = 1
    SHOOT_COOL = 30
    ATTACK_COOL = 60

    def __init__(self, x: int, y: int,) -> None:
        self.x = x
        self.y = y
        self.vel = 10
        self.velUp = 0
        self.time = 0
        self.bulletCooldown = 0
        self.attackCooldown = 0
        self.health = 100
        self.maxHealth = self.health
        self.food = 100
        self.maxFood = self.food
        self.water = 100
        self.maxWater = self.water
        self.desire = 0
        
        self.secondJump = False
        self.hitEnemy = False

        self.scale = 5
        self.direction = 1
        self.current = 0
        self.currentItem = 0
        self.items = 3
        self.imgs = []
        self.deaths = []

        # standart sprite sheets
        items = ["normal", "pistol", "sword"]
        animations = ["idle", "walk", "swim", "attack"]
        
        for item in items:
            items = []
        
            for animation in animations:
                l = []
        
                for i in range(1, 5):
                    img = pygame.image.load(f"images/player/{item}/{animation}/{animation} left{i}.png")
                    img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
                    l.append(img)
        
                items.append(l)
        
            self.imgs.append(items)
        
        self.img = self.imgs[self.currentItem][self.current][0]

        # death animation
        for i in range(1, 5):
            img = pygame.image.load(f"images/player/death/death{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale)) 
            self.deaths.append(img)


        self.width = self.img.get_width()
        self.height = self.img.get_height() - 2 * self.scale
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.flip = False
        self.jumping = False

        self.resetted = False

        # list where all shot bullets are stored
        self.bullets = []

    def draw(self, surf: pygame.Surface) -> None:
        '''
            Drawing the player with every additional element
        '''

        # checking for iamge flip and drawing image
        surf.blit(pygame.transform.flip(self.img, self.flip, False), (self.x, self.y))
        
        # getting bar rects
        maxHealth, health = self.healthBar()
        maxFood, food, maxWater, water = self.getFood()
        
        # drawign bar rects
        pygame.draw.rect(surf, BLUE, maxHealth)
        pygame.draw.rect(surf, PINK, health)

        pygame.draw.rect(surf, BLUE, maxFood)
        pygame.draw.rect(surf, PINK, food)
        
        pygame.draw.rect(surf, BLUE, maxWater)
        pygame.draw.rect(surf, PINK, water)

        # drawing bullets
        for bullet in self.bullets:
            bullet.draw(surf)

    def move(self, left: bool, right: bool, targets: list, items: list, cameraLim: int) -> int:
        ''' 
            Updating the player movement
            Handling most of the events related or affected by player movement
        '''

        scroll = 0
        dx = dy = 0
        
        if left and self.current != 3 or right and self.current != 3:
            self.current = 1
        
        if left:
            dx += self.vel
            self.flip = True
            self.direction = -1
        elif right:
            dx -= self.vel
            self.flip = False
            self.direction = 1
        else:
            if self.current != 3:
                self.current = 0

        self.time += 1

        self.gravity()

        dy += self.velUp

        dx, dy = self.collision(targets, dx, dy)

        self.x += dx
        self.y += dy

        if self.x > WIDTH - cameraLim - self.width and self.direction == -1:
            self.x -= dx
            scroll = -dx

        self.animate()
        self.updateRect()
        self.attCooldown()
        self.itemCollision(items)

        #updating every bullet to camera
        for bullet in self.bullets:
            bullet.camera(scroll)

        #returning camera value
        return scroll

    def updateRect(self) -> None:
        '''
            Update the player rect every frame
        '''

        self.width = self.img.get_width()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def animate(self) -> None:
        '''
            Animate the player every frame
        '''

        if self.time < 10:
            self.img = self.imgs[self.currentItem][self.current][0]
        
        elif self.time < 20:
            self.img = self.imgs[self.currentItem][self.current][1]
        
        elif self.time < 30:
            self.img = self.imgs[self.currentItem][self.current][2]
        
        elif self.time < 40:
            self.img = self.imgs[self.currentItem][self.current][3]
        else:
            if self.current == 3:
                if self.currentItem == 2:
                    self.attackAdjustmend()
                self.current = 0
            self.time = 0
        
        if self.current == 3:
            
            if self.currentItem == 1:
                self.shootAdjustmend()
            elif self.currentItem == 2:
                self.attackAdjustmend()

    def alive(self) -> bool:
        '''
            Check if player is still alive
        '''
        isAlive = False 

        if self.health > 0:
            isAlive = True
            
        return isAlive

    def gravity(self) -> None:
        '''
            Constantly add gravity to players movement
        '''

        self.velUp += self.GRAVITY
        if self.velUp > 20:
            self.velUp = 20

    def collision(self, targets: list, dx: int, dy: int) -> tuple:
        '''
            Check for player collisions
        '''

        for chunk in targets:
            for tile in chunk:
                if tile.rect.colliderect(self.x + dx, self.y, self.width, self.height):
                    dx = 0
                if tile.rect.colliderect(self.x, self.y + dy, self.width, self.height):
                    if self.velUp < 0:
                        self.velUp = 0
                        dy = tile.rect.y + TILE_SIZE  - self.y
                    elif self.velUp >= 0:
                        self.velUp = 0
                        self.jumping = self.secondJump = False
                        dy = tile.rect.y - (self.y + self.height)

        if self.x + dx < 0:
            dx = 0

        return dx, dy

    def itemCollision(self, items: list) -> list:
        
        b = False
        
        for item in items:
            if item.rect.colliderect(self.rect):
                if item.type == 0:
                    self.food += item.value
                    items.remove(item)
                    if self.food > 100:
                        self.food = 100
                else:
                    self.water += item.value
                    if self.water > 100:
                        self.water = 100
                    items.remove(item)

        return items
                    

    def shoot(self) -> None:
        '''
            Add bullet to self.bullets
        '''

        if self.bulletCooldown == 0:
            self.current = 3
            self.time = 0
            if self.direction == -1:
                bullet = Bullet(self.x + 12 * self.scale, self.y + 8 * self.scale, -self.direction, PISTOL_DAMAGE)
            else:
                bullet = Bullet(self.x - 2 * self.scale, self.y + 8 * self.scale, -self.direction, PISTOL_DAMAGE)
            self.bullets.append(bullet)
            self.bulletCooldown = 1
    
    def attack(self) -> None:
        '''
            Attack with sword and shield
        '''

        if self.attackCooldown == 0:
            self.current = 3
            self.time = 0
            self.attackCooldown = 1

    def attackHit(self, targets: list) -> None:
        '''
            Check if sword hitted target when swinging
        '''

        if self.time == 1:
            self.hitEnemy = False
        if not self.hitEnemy:

            if self.time < 20 and self.current == 3:
                if self.direction == -1:
                    for target in targets:
                        offset = self.x - target.rect.x
                        offsety = self.y - target.rect.y
            
                        if abs(offset) <= self.width and abs(offsety) < 15 * self.scale:
                            target.health -= SWORD_DAMAGE
                            self.hitEnemy = True
                            
                else:
                    for target in targets:
                        offsety = self.y - target.rect.y
                        if self.x < (target.rect.x + target.width) and self.x > (target.rect.x - 9 * self.scale) and abs(offsety) < 15 * self.scale:
                            target.health -= SWORD_DAMAGE
                            self.hitEnemy = True
                            break

    def moveBullets(self, obstacles: list, targets: list) -> None:
        '''
            Move the bullets after shooting
        '''

        self.cooldown()
        for bullet in self.bullets:
            v1 = bullet.move(obstacles, targets)
            if v1:
                self.bullets.remove(bullet)

    def cooldown(self) -> None:
        '''
            Shooting cooldown
        '''

        if self.bulletCooldown > 0:
            self.bulletCooldown += 1
            if self.bulletCooldown >= self.SHOOT_COOL:
                self.bulletCooldown = 0

    def attCooldown(self) -> None:
        '''
            Sword cooldown
        '''

        if self.attackCooldown > 0:
            self.attackCooldown += 1
            if self.attackCooldown >= self.ATTACK_COOL:
                self.attackCooldown = 0


    def nextItem(self) -> None:
        '''
            Get the next item after rolling the mouse wheel
        '''

        self.currentItem += 1
        if self.currentItem > self.items - 1:
            self.currentItem = 0

        # changing the speed if player takes gun or sword
        if self.currentItem == 1:
            self.vel = 7
        elif self.currentItem == 2:
            self.vel = 5
        else:
            self.vel = 10

    def shootAdjustmend(self) -> None:
        '''
            Image topleft changes because of the gun tip when firing -> adjustment
        '''

        if self.direction == 1:
            if self.time == 1:
                self.x -= 4 * self.scale
            elif self.time == 10:
                self.x += 5 * self.scale
            elif self.time == 20:
                self.x -= 1 * self.scale

    def attackAdjustmend(self) -> None:
        '''
            Image topleft changes because of the sword tip when attacking -> adjustment
        '''
        if self.direction == -1:
            if self.time == 1:
                self.x -= 3 * self.scale
            elif self.time == 10:
                self.x += 4 * self.scale
            elif self.time == 20:
                self.x -= 5 * self.scale
            elif self.time == 40:
                self.x += 4 * self.scale
        elif self.direction == 1:
            if self.time == 1:
                self.x -= 10 * self.scale
            #elif self.time == 10:
                #self.x += 4 * self.scale
            elif self.time == 20:
                self.x += 10 * self.scale
            #elif self.time == 40:
                #self.x += 4 * self.scale

    def checkShoot(self) -> None:
        '''
            Getting all keys that are held down:
                > this is done, so the player can shoot/attack continously
                > when holding down the mouse button
        '''
        if pygame.mouse.get_pressed()[0]:
            if self.currentItem == 1:
                self.shoot()
            elif self.currentItem == 2:
                self.attack()

    def deathAnimation(self):
        '''
            death animation:
                > stops every other activity (in main.py)
        '''

        if not self.resetted:
            self.time = 0
            self.resetted = True

        self.time += 1

        if self.time < 5:
            self.img = self.deaths[0]
        elif self.time < 10:
            self.y += 0.2 * self.scale
            self.img = self.deaths[1]
        elif self.time < 15:
            self.y += 0.2 * self.scale
            self.img = self.deaths[2]
        elif self.time < 20:
            if self.time == 15:
                self.y += 2 * self.scale
                self.x -= 5 * self.scale
            self.img = self.deaths[3]
        else:
            return True

    def healthBar(self) -> tuple:
        '''
            Returns Rects to draw health bar
        '''
        relHealth = (self.health / self.maxHealth) * 100
        maxHealth = pygame.Rect(5, 5, self.maxHealth * 2, 20)
        health = pygame.Rect(5, 5, relHealth * 2, 20)

        return maxHealth, health

    def getFood(self):
        '''
        returns Rects to draw for bars
        '''
        maxFood = pygame.Rect(5, 30, self.maxFood * 2, 20)
        maxWater = pygame.Rect(5, 55, self.maxWater * 2, 20)

        food = pygame.Rect(5, 30, self.food * 2, 20)
        water = pygame.Rect(5, 55, self.water * 2, 20)

        return maxFood, food, maxWater, water

    def getDesire(self) -> None:
        '''
            Food and water bar decreases every time this funcion is called
        '''
        self.desire += 1
        if self.desire >= 60:
            self.food -= FOOD_DECREASE
            self.water -= FOOD_DECREASE
            self.desire = 0

    def useItem(self, targets: list) -> None:
        '''
            Pick up food or water and add points to according bar
        '''
        for target in targets:
            if self.rect.colliderect(target.rect):
                if target.type == 0:
                    self.water += 20
                    if self.water > 100:
                        self.water = 100

                else:
                    self.food += 20
                    if self.food > 100:
                        self.food = 100
                

    def foodShortage(self) -> None:
        '''
            Check if food or water is less than 0 > health decreases
        '''
        if self.food < 0 or self.water < 0:
            self.health -= 1

    def jump(self) -> None:
        if not self.secondJump:
            self.velUp = -20
            if self.jumping:
                self.secondJump = True
            else:
                self.jumping = True