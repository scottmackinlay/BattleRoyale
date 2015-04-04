import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener

# This example uses Python threads to manage async input from sys.stdin.
# This is so that I can receive input from the console whilst running the server.
# Don't ever do this - it's slow and ugly. (I'm doing it for simplicity's sake)
from thread import *
import pygame
from pygame.locals import *
pygame.init()

class Client(ConnectionListener):
	def __init__(self, host, port):
		self.Connect((host, port))
		print "client started"
		# get a name from the user before starting
		print "Enter your name: ",
		connection.Send({"action": "name", "name": stdin.readline().rstrip("\n")})

		self.screen = pygame.display.set_mode((100, 100))
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((250, 250, 250))
		self.screen.blit(self.background, (0, 0))
		pygame.display.flip()
	
	def Loop(self):
		connection.Pump()
		self.Pump()
		for event in pygame.event.get():
			if event.type == KEYUP and (event.key == K_LEFT 
				or event.key == K_RIGHT
				or event.key == K_UP
				or event.key == K_DOWN):
				connection.Send({'action':'move','move':[0,0]})
			if event.type == KEYDOWN and event.key == K_LEFT:
				connection.Send({'action':'move','move':[-1,0]})
			if event.type == KEYDOWN and event.key == K_RIGHT:
				connection.Send({'action':'move','move':[1,0]})
			if event.type == KEYDOWN and event.key == K_UP:
				connection.Send({'action':'move','move':[0,1]})
			if event.type == KEYDOWN and event.key == K_DOWN:
				connection.Send({'action':'move','move':[0,-1]})	
	#######################################
	### Network event/message callbacks ###
	#######################################
	
	def Network_players(self, data):
		print "*** players: " + ", ".join([p for p in data['players']])
	
	def Network_message(self, data):
		print data['who'] + ": " + str(data['message'])

	# built in stuff

	def Network_connected(self, data):
		print "You are now connected to the server"
	
	def Network_error(self, data):
		print 'error:', data['error'][1]
		connection.Close()
	
	def Network_disconnected(self, data):
		print 'Server disconnected'
		exit()

if len(sys.argv) != 2:
	print "Usage:", sys.argv[0], "host:port"
	print "e.g.", sys.argv[0], "localhost:31425"
else:
	host, port = sys.argv[1].split(":")
	c = Client(host, int(port))
	while 1:
		c.Loop()
		sleep(0.001)