
import pygame
from pygame.locals import *
import random
from os import path
import sys


pygame.init()

# settings
size = width, height = (1600, 1000)
FPS = 60
running = True
BLACK = (0,0,0)
blue = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)
font_name = pygame.font.match_font("comicsansms")
click = False

# Game window
FpsClock = pygame.time.Clock() 
screen = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("Fruit game")
pygame.display.update()


# Images
apple = pygame.image.load("apple2.png").convert()
apple = pygame.transform.rotozoom(apple, 0, 0.08)
apple.set_colorkey((0,0,0))
background = pygame.image.load("forest.jpg").convert()
background = pygame.transform.scale(background,size)
background_rect = background.get_rect()
screen.blit(background,(0,0))


# Apples
class Apple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = apple
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width - self.rect.width)
        self.rect.y = -50
        self.speed_y = random.randrange(1, 8)
    
    def update(self):
        self.rect.y += self.speed_y


# Group all apples
all_apples = pygame.sprite.Group() 


# Display to screen
def message_to_screen(message, color, font_size, x, y):
    """Displays messages to screen"""
    font = pygame.font.SysFont(font_name, font_size)
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    screen.blit(text, text_rect)


for i in range(1, 5):
    a = Apple()
    all_apples.add(a)


class globaVariables():
    score = 0
    lives = 3

def game():
    

    running = True
    while running:
        
        mx, my = pygame.mouse.get_pos()
        # Draw to screen   
        screen.blit(background,(0,0))
        all_apples.draw(screen) 
        all_apples.update()
        message_to_screen("Your score is: " + str(globaVariables.score), WHITE, 24, width*0.05, height*0.05)
        message_to_screen(str(globaVariables.lives) + " lives", WHITE, 24, width*0.03, height*0.03)

        click = False

        # End game if player presses window "X"
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
        pygame.display.update()
        FpsClock.tick(FPS)
        if len(all_apples) < 4:
            a = Apple()
            all_apples.add(a)

        if pygame.mouse.get_pressed()[0]:
            for item in all_apples:
                    if item.rect.collidepoint((mx, my)):  
                        item.kill()
                        globaVariables.score = globaVariables.score + 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    
        
        for item in all_apples:
            if item.rect.y > height:
                globaVariables.lives -= 1
                screen.blit(background,(0,0))
                item.kill()
                if globaVariables.lives == 0:
                    end_game()
                    

def end_game():
    running = True
    while running:
        pygame.draw.rect(screen, WHITE, (width*0.4, height*0.4, 330, 250))
        message_to_screen("Total score: " + str(globaVariables.score), BLACK, 50, width/2, height/2)
        #restart = message_to_screen("Restart? ", GREEN, 50, 800, 600)

        text = pygame.font.SysFont(font_name, 50).render("Restart?", True, GREEN)
        text_rect = text.get_rect()
        text_rect.center = (800, 600)
        screen.blit(text, text_rect)
        pygame.display.update()
        FpsClock.tick(60)

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if pygame.mouse.get_pressed()[0]:
                if text_rect.collidepoint(event.pos):
                    globaVariables.lives = 3
                    globaVariables.score = 0 
                    for item in all_apples:
                        item.kill()
                    for i in range(1, 5):
                        a = Apple()
                        all_apples.add(a)
                    game()

game()

pygame.quit()