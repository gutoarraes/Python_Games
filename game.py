# Imports
import pygame
import sys
import random
from pygame.locals import *
from os import path
from time import sleep

# settings
pygame.init()
pygame.mixer .init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
size = width, height = (1024, 1024) 
FPS = 60

# Screen
screen = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# images
ship = pygame.image.load("ship.png")
enemy = pygame.image.load("enemy1.png").convert_alpha()
enemy.set_colorkey((255,255,255))
enemy = enemy.convert()
background  = pygame.image.load("background.png")
background = pygame.transform.scale(background, size)
background = background.convert()
shot = pygame.image.load("shot.png")
shot = shot.convert()
shot.set_colorkey((0,0,0))


# sounds

# ship
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ship
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.y = 930
        self.speed_x = 0


    def movement(self):
        self.speed_x = 0
        events = pygame.key.get_pressed()
        if events[pygame.K_a]:
            self.speed_x = -10
        elif events[pygame.K_d]:
            self.speed_x = 10
        self.rect.centerx += self.speed_x

    def boundary(self):
        if self.rect.left < 0:
            self.rect.left = -5
        elif self.rect.right > width:
            self.rect.right = width +10
        
    def update(self):
        self.movement()
        self.boundary()

# shots
class Shot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3,8))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.speed_y = -15
        self.rect.x = ship.rect.centerx
        self.rect.y = 930

    def update(self):  
        self.rect.y = self.rect.y + self.speed_y
        if self.rect.bottom < 0:
            self.kill()


# enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed_y = random.randint(2, 6)
        self.image = enemy
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1000)
        self.rect.y = 0

    def update(self):
        self.rect.y = self.rect.y + self.speed_y
        if self.rect.y > 1024:
            self.kill()

# display lives

# global variables

all_sprites = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
all_shots = pygame.sprite.Group()

ship = Ship()
all_sprites.add(ship)


# main game loop
def game():
    while True:
        
        while len(all_enemies) < 8:
            new_enemy = Enemy()
            all_sprites.add(new_enemy)
            all_enemies.add(new_enemy)
        # Run game at 60 FPS
        clock.tick(FPS)

        # check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            new_shot = Shot()
            all_shots.add(new_shot)
            all_sprites.add(new_shot)
            collision = pygame.sprite.groupcollide(all_shots, all_enemies, True, True)
        
                        

        # check if a shot is in the rectangle of an enemy sprite, if so, kill enemy and shot
            
        # update all sprites
        all_sprites.update()

        # draw to screen
        all_sprites.draw(screen)
        pygame.display.update()
        screen.blit(background,(0,0))


    

# end of game loop

game()

