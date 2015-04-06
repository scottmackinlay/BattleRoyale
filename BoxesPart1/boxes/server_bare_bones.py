import sys
from time import sleep, localtime
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from weakref import WeakKeyDictionary

class ClientChannel(Channel):
	"""
	This is the server representation of a single connected client.
	"""
	def __init__(self, *args, **kwargs):
		self.pos=[0,0]
		self.move=[0,0]
		Channel.__init__(self, *args, **kwargs)
	
	def Close(self):
		self._server.DelPlayer(self)

	def Network_move(self,data):
		self.move=data['move']

class Serve(Server):
	channelClass = ClientChannel

	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		print 'Server launched'
	
	def Connected(self, channel, addr):
		channel.Send({'action':'setup',
			'screenSize':model.screenSize,
			'playerSize':model.playerSize,
			'zombieSize':model.zombieSize})
		model.AddPlayer(channel)
	
	def DelPlayer(self, player):
		model.DelPlayer(player)

	def SendToAll(self, data):
		[p.Send(data) for p in model.players]

	def Update(self):
		model.Update()
		self.SendToAll({'action':'update',
			'update':[[p.pos for p in model.players],model.zombieList]})
	
	def Launch(self):
		while True:
			self.Pump()
			self.Update()
			sleep(0.01)

class Model(object):
	def __init__(self):
		self.screenSize=(500,500)
		self.playerSize=32
		self.zombieSize=16
		self.players=WeakKeyDictionary()
		self.zombieList=[[10,10],[50,50]]

	def AddPlayer(self,channel):
		self.players[channel] = True
		print 'person added!'

	def DelPlayer(self,player):
		del self.players[player]
		print 'person deleted!'

	def Update(self):
		for player in self.players:
			player.pos[0]+=player.move[0]
			player.pos[1]+=player.move[1]

	def AddZombies(self):
		for z in range(10):
			pass

# get command line argument of server, port
if len(sys.argv) != 2:
	print "Usage:", sys.argv[0], "host:port"
	print "e.g.", sys.argv[0], "localhost:31425"
else:
	host, port = sys.argv[1].split(":")
	s = Serve(localaddr=(host, int(port)))
	model=Model()
	s.Launch()
