# Imports
from os import path
import random
from re import X
import sys
from turtle import color
import pygame


pygame.init()
# Settings
size = width, height = (1600, 1000)
FPS = 60
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
font_name = pygame.font.match_font("comicsans")
font_size = 25


# Game Window
FpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("Apple game")


# Images
game_folder = path.dirname(__file__)
apple = pygame.image.load(path.join(game_folder, "apple2.png")).convert()
apple = pygame.transform.rotozoom(apple, 0, 0.08)
apple.set_colorkey(BLACK)
background = pygame.image.load(path.join(game_folder, "forest.jpg")).convert()
background = pygame.transform.scale(background, size)
background_rect = background.get_rect()


# Apple class
class Apple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = apple
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width - self.rect.width)
        self.rect.y = -50
        self.speed_y = random.randrange(1, 10)

    def update(self):
        self.rect.y += self.speed_y

# Group all apples
all_apples = pygame.sprite.Group()

# Global variables
class globalVariables():
    score = 0
    lives = 3

for i in range(1, 5):
    a = Apple()
    all_apples.add(a)


# Display text to screen
def screenText(message, color, font_size, x, y):
    font = pygame.font.SysFont(font_name, font_size)
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    screen.blit(text, text_rect)



# Main game
def game():

    running = True
    while running:
        pygame.display.update()
        # get mouse position
        mx, my = pygame.mouse.get_pos()
        
        #Draw to screen
        screen.blit(background,(0,0))
        screenText("Score: " + str(globalVariables.score), WHITE, 25, width*0.05, height*0.05)
        screenText("lives: " + str(globalVariables.lives), WHITE, 25, width*0.05, height*0.08)
        all_apples.draw(screen)
        all_apples.update()        

        # check if player clicks the x button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
        
        FpsClock.tick(FPS)
        if len(all_apples) < 4:
            a = Apple()
            all_apples.add(a)

        # Kill apple player clicks it (compare mouse position with apple position, check if user left click, if so kill Apple)
        if pygame.mouse.get_pressed()[0]:
            for item in all_apples:
                if item.rect.collidepoint((mx,my)):
                    item.kill()
                    globalVariables.score += 1
                    
        # If apple falls below screen, kill Apple and deduct 1 life
        for item in all_apples:
            if item.rect.y > height:
                item.kill()
                globalVariables.lives -= 1
                if globalVariables.lives == 0:
                    end_game()


# End game screen
def end_game():
    
    mx, my = pygame.mouse.get_pos()
    running = True
    while running:
        pygame.display.update()
        screen.blit(background,(0,0))
        pygame.draw.rect(screen, WHITE, (width*0.4, height*0.4, 330, 250))
        screenText("Total Score " + str(globalVariables.score), BLACK, 50, width/2, height/2)
        # screenText("Restart?", BLUE, 50, 800, 550)
        text = pygame.font.SysFont(font_name, 50).render("Restart?", True, BLUE)
        text_rect = text.get_rect()
        text_rect.center = (800, 550)
        screen.blit(text, text_rect)
    

        # check if player clicks the x button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
        
        # check if player clicks restart, in which case start game again
        if pygame.mouse.get_pressed()[0]:
            if text_rect.collidepoint(event.pos):
                # reset variables
                globalVariables.lives = 3
                globalVariables.score = 0
                game()            
                

game()

pygame.quit()
