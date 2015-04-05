import sys
from time import sleep
from sys import stdin, exit
from PodSixNet.Connection import connection, ConnectionListener
from thread import *
import pygame
from pygame.locals import *
pygame.init()

def load_image(name):
    """Code to load images from folder into game screen"""
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    return image, image.get_rect()

class Client(ConnectionListener):
	def __init__(self, host, port):
		self.Connect((host, port))
		print "client started"
		# get a name from the user before starting
		print "Enter your name: ",
		connection.Send({"action": "name", "name": stdin.readline().rstrip("\n")})
		self.move=[0,0]
	
	def Loop(self):
		connection.Pump()
		self.Pump()
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_LEFT:
				self.move[0]+=1
			if event.type == KEYUP and event.key == K_LEFT:
				self.move[0]-=1
			if event.type == KEYDOWN and event.key == K_RIGHT:
				self.move[0]-=1
			if event.type == KEYUP and event.key == K_RIGHT:
				self.move[0]+=1
			if event.type == KEYDOWN and event.key == K_UP:
				self.move[1]+=1
			if event.type == KEYUP and event.key == K_UP:
				self.move[1]-=1
			if event.type == KEYDOWN and event.key == K_DOWN:
				self.move[1]-=1
			if event.type == KEYUP and event.key == K_DOWN:
				self.move[1]+=1
		connection.Send({'action':'move','move':self.move})

	def Network_update(self,data):
		print data['update']
		view.frame(data['update'])

	def Network_connected(self, data):
		print "You are now connected to the server"
	
	def Network_error(self, data):
		print 'error:', data['error'][1]
		connection.Close()
	
	def Network_disconnected(self, data):
		print 'Server disconnected'
		exit()

class Game_element(pygame.sprite.Sprite):
	def __init__(self,image_name):
		pygame.sprite.Sprite.__init__(self) 
		self.image, self.rect = load_image(image_name)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()

class Hero(Game_element):
	def __init__(self):
		super(Hero,self).__init__('hero.png')
		self.rect.topleft = 10,50

class Background(object):
    """ Creates background screen and flips the display.  """
    def __init__(self,xres,yres):
        """ Initializes game screen"""
        self.screen = pygame.display.set_mode((xres, yres))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250, 250, 250))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

class View(object):
	def __init__(self):		
		self.background=Background(600,600)
		self.hero=Hero()
		self.allsprites=pygame.sprite.RenderPlain(self.hero)
	def frame(self,data):
		self.background.screen.blit(self.background.background, (0, 0))
		self.hero.topleft=data[0]
		self.allsprites.draw(self.background.screen)
		pygame.display.flip()


if len(sys.argv) != 2:
	print "Usage:", sys.argv[0], "host:port"
	print "e.g.", sys.argv[0], "localhost:31425"
else:
	host, port = sys.argv[1].split(":")
	c = Client(host, int(port))
	view=View()
	while 1:
		c.Loop()
		sleep(0.001)