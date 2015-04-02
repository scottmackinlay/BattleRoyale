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
bulletList = []
enemyList = []

# Number Initializations
MaxEnemies = 10

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

# Define the Screen
screen = pygame.display.set_mode((screenWidth, screenHeight))

################################################################################################################
# Class Definitions                                                                                            #
################################################################################################################

# World Class Initialization
class World():  # represents a bullet, not the game
    def __init__(self,color,x,y,width = 4,height = 4):
        """ The constructor of the class """
        self.backgrounds = []
        self.characters = []
        self.bullets = []
        self.enemys = []
        self.blocks = []
        
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))


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
        self.x = -self.width/2 + xCenter
        self.y = -self.height/2 + yCenter
        self.xVel = 0
        self.yVel = 0
        self.xAcc = 0
        self.yAcc = 0
        
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))

    def bulletDirection(self):
        mousePos = pygame.mouse.get_pos()
        mouseX = mousePos[0]
        mouseY = mousePos[1]

        xPart = float(abs(mouseX-self.x)**2)/(abs(mouseX-self.x)**2 + abs(mouseY-self.y)**2)
        yPart = float(abs(mouseY-self.y)**2)/(abs(mouseX-self.x)**2 + abs(mouseY-self.y)**2)

        if self.x < mouseX:
            # attraction must go right
            xDir = 'right'
        elif self.x > mouseX:
            # attraction must go left
            xDir = 'left'
        else:
            xDir = ''

        if self.y > mouseY:
            # attraction must go right
            yDir = 'up'
        elif self.y < mouseY:
            # attraction must go left
            yDir = 'down'
        else:
            yDir = ''
        return [xDir,yDir,xPart,yPart]

    def shoot(self,alist):
        partsDir = self.bulletDirection()
        xDir = partsDir[0]
        yDir = partsDir[1]
        xPart = partsDir[2]
        yPart = partsDir[3]
        initBulletVel = 20
        mousePress = pygame.mouse.get_pressed()
        if mousePress[0] == True:
            bullet = Bullet(GREY,0,0)
            bullet.x = self.x+self.width/2
            bullet.y = self.y+self.height/2

            if xDir == 'right':
                bullet.xVel += xPart*initBulletVel
            elif xDir == 'left':
                bullet.xVel -= xPart*initBulletVel
            else:
                bullet.xVel = 0

            if yDir == 'down':
                bullet.yVel += yPart*initBulletVel
            elif yDir == 'up':
                bullet.yVel -= yPart*initBulletVel
            else:
                bullet.yVel = 0
            alist.append(bullet)

    def gameControl(self,alist):
        self.shoot(alist)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() # quit the screen
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    sys.exit() # quit the screen
                elif event.key == pygame.K_a:
                    self.xVel -= 8
                elif event.key == pygame.K_d:
                    self.xVel += 8
                elif event.key == pygame.K_w:
                    self.yVel -= 8
                elif event.key == pygame.K_s:
                    self.yVel += 8

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    sys.exit() # quit the screen
                elif event.key == pygame.K_a:
                    self.xVel += 8
                elif event.key == pygame.K_d:
                    self.xVel -= 8
                elif event.key == pygame.K_w:
                    self.yVel += 8
                elif event.key == pygame.K_s:
                    self.yVel -= 8

    def moveChar(self):
        self.x += self.xVel
        self.y += self.yVel
                

# Bullet Class Initialization
class Bullet():  # represents a bullet, not the game
    def __init__(self,color,x,y,width = 4,height = 4):
        """ The constructor of the class """
        # the bullet's position
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.x = x-self.width/2
        self.y = y-self.height/2
        self.xVel = 0
        self.yVel = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))

    def moveBullet(self):
        self.x += self.xVel
        self.y += self.yVel

    def bulletCleaner(self):
        if self.x > screenWidth:
            return True
        elif self.x < 0:
            return True
        elif self.y > screenHeight:
            return True
        elif self.y < 0:
            return True
        else:
            return False
        
        
# Block Class Initialization
class Block():  # represents a bullet, not the game
    def __init__(self,color,x,y,width = 4,height = 4):
        """ The constructor of the class """
        # the block's position
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.x = x-self.width/2
        self.y = y-self.height/2
        
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))
        # y = Character.self.y
        
        
# Enemy Class Initialization
class Enemy():  # represents a bullet, not the game
    def __init__(self,color,x,y,width = 10,height = 10):
        """ The constructor of the class """
        # the enemy's position
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.x = -self.width/2
        self.y = -self.height/2
        self.xVel = 0
        self.yVel = 0
        
        self.health = 10
        self.damage = 10
        self.speed = 10

    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))

    def enemyDirection(self):
        choiceX = [1,-1]
        choiceY = [1,-1]
        changeX = random.choice(choiceX)
        changeY = random.choice(choiceY)
        self.xVel += changeX
        self.yVel += changeY

        if self.xVel > 0:   
            if abs(self.xVel) > 10:
                self.xVel = 10
        else:
            if abs(self.xVel) > 10:
                self.xVel = -10

        if self.yVel > 0:   
            if abs(self.yVel) > 10:
                self.yVel = 10
        else:
            if abs(self.yVel) > 10:
                self.yVel = -10

    def moveEnemy(self):
        self.x += self.xVel
        self.y += self.yVel

    def edgeBounce(self):
        if self.x > screenWidth or self.x < 0:
            self.xVel = -1*(self.xVel)
        if self.y > screenHeight or self.y < 0:
            self.yVel = -1*(self.yVel)

    def enemyCleaner(self):
        if self.x > screenWidth+15:
            return True
        elif self.x < -15:
            return True
        elif self.y > screenHeight+15:
            return True
        elif self.y < -15:
            return True
        else:
            return False

    
        
        
################################################################################################################
# Function Definitions                                                                                         #
################################################################################################################

def loadData():
    filename = './BattleRoyale.txt'
    data_file = open(filename,'r')
    data_list = load(data_file)
    data_file.close()
    return data_list

def saveData(alist):
    filename = './BattleRoyale.txt'
    data_file = open(filename,'w')
    dump(alist,data_file)
    data_file.close()

def generateEnemies(alist): # maybe add (isGameOver = False)
        # this function generates the colored tiles that make up the game image
        if len(alist) == 0:
            numEnemies = random.randint(5,10)
            for enemy in range(numEnemies):
                color = (ORANGE)
                enemy = Enemy(color,0,0)
                enemy.x = random.randrange(screenWidth)
                enemy.y = random.randrange(screenHeight)
                
                enemy.draw(screen)
                alist.append(enemy)

def drawBullets(alist):
        i=0
        for bullet in alist:
            bullet.moveBullet()
            delete = bullet.bulletCleaner()
            bullet.draw(screen)
            if delete == True:
                del alist[i]
            i+=1

def killEnemy(alist,blist):
    i=0
    delete = False
    for enemy in alist:
        j=0
        for bullet in blist:
            if bullet.rect.colliderect(enemy.rect) == True:
                delete = True
            else:
                delete = False
            if delete == True:
                del alist[i]
                del blist[j]
            j+=1
        i+=1



def drawEnemies(alist):
    i=0
    generateEnemies(enemyList)
    for enemy in alist:
        enemy.enemyDirection()
        enemy.moveEnemy()
        delete = enemy.enemyCleaner()
        enemy.draw(screen)
        enemy.edgeBounce()
        if delete == True:
            del alist[i]
        i+=1

def drawAll(alist,blist):
    drawBullets(alist)
    drawEnemies(blist)
    # killEnemy(enemyList,bulletList)

################################################################################################################
# Pre-Run Initializatio                                                                                        #
################################################################################################################
# pygame.init()
background = Background(BLACK)
character = Character(WHITE,10,10)

################################################################################################################
# Main Loop                                                                                                    #
################################################################################################################

if __name__ == "__main__": 
    while True:
        background.draw(screen)
        character.gameControl(bulletList)
        character.moveChar()
        drawAll(bulletList,enemyList)
        character.draw(screen)
        pygame.display.flip()
        clock.tick(10)
        
        
        
        
        