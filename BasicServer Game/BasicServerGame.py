################################################################################################################
# Package Imports                                                                                              #
################################################################################################################
from pickle import dump,load
from pygame.locals import *
from math import *
import pygame
import random
import math
import sys
import os

################################################################################################################
# Global Variable Definitions                                                                                  #
################################################################################################################
clock = pygame.time.Clock()
pygame.font.init()
particleList = []
pullList = [0,0]
partPullList = [0,0]

# font initialization
GameOver = pygame.font.SysFont('Ariel', 140, bold=True, italic=False)
font = pygame.font.SysFont('Ariel', 80, bold=True, italic=False)

# Color Definitions
WHITE = (255, 255, 255)
GREY = (119, 136, 153)
ORANGE = (255, 102, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen Size
screenWidth = 700
screenHeight = 700
xCenter = screenWidth/2
yCenter = screenHeight/2

################################################################################################################
# Class Definitions                                                                                            #
################################################################################################################

# Background Class Initialization
class Background():  # represents the player, not the game
    def __init__(self,color = BLACK,width = screenWidth,height = screenHeight):
        """ The constructor of the class """
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # the background's position
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0

    def draw(self, surface):
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))


# Character Class Initialization
class Character():  # represents the player, not the game
    def __init__(self,color,x,y,width = 20,height = 20):
        """ The constructor of the class """
        # the character's position
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.x = x-self.width/2 + xCenter
        self.y = y-self.height/2 + yCenter
        self.xVel = 0
        self.yVel = 0
        self.xAcc = 0
        self.yAcc = 0
        
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))
        
    def gameControl(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() # quit the screen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit() # quit the screen
                elif event.key == pygame.K_LEFT:
                    self.xVel -= 5
                elif event.key == pygame.K_RIGHT:
                    self.xVel += 5
                elif event.key == pygame.K_UP:
                    self.yVel -= 5
                elif event.key == pygame.K_DOWN:
                    self.yVel += 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    sys.exit() # quit the screen
                elif event.key == pygame.K_LEFT:
                    self.xVel += 5
                elif event.key == pygame.K_RIGHT:
                    self.xVel -= 5
                elif event.key == pygame.K_UP:
                    self.yVel += 5
                elif event.key == pygame.K_DOWN:
                    self.yVel -= 5
    def moveChar(self):
        self.x += self.xVel
        self.y += self.yVel

################################################################################################################
# Pre-Run Initializatio                                                                                        #
################################################################################################################
# pygame.init()
background = Background(BLACK)
character = Character(WHITE,10,10)
# Define the Screen
screen = pygame.display.set_mode((screenWidth, screenHeight))

################################################################################################################
# Main Loop                                                                                                    #
################################################################################################################

if __name__ == "__main__": 
    while True:
        background.draw(screen)
        character.draw(screen)
        pygame.display.flip()
        character.gameControl()
        character.moveChar()
        clock.tick(10)