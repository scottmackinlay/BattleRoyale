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
		self.position=[0,0]
		self.name = "anonymous"
		Channel.__init__(self, *args, **kwargs)
	
	def Close(self):
		self._server.DelPlayer(self)
	
	##################################
	### Network specific callbacks ###
	##################################

	def Network_move(self,data):
		print str(data['move'])+self.name
		self._server.SendToAll({
			"action": "message",
			'message':data['move'],
			'who':self.name})
	
	def Network_name(self, data):
		self.name = data['name']
		self._server.SendPlayers()

class Serve(Server):
	channelClass = ClientChannel
	
	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.players = WeakKeyDictionary()

		print 'Server launched'
	
	def Connected(self, channel, addr):
		self.AddPlayer(channel)
	
	def AddPlayer(self, player):
		print "New Player" + str(player.addr)
		self.players[player] = True
		self.SendPlayers()
		print "players", [p for p in self.players]
	
	def DelPlayer(self, player):
		print "Deleting Player" + str(player.addr)
		del self.players[player]
		self.SendPlayers()
	
	def SendPlayers(self):
		self.SendToAll({"action": "players", "players": [p.name for p in self.players]})
	
	def SendToAll(self, data):
		[p.Send(data) for p in self.players]
	
	def Launch(self):
		while True:
			self.Pump()
			sleep(0.0001)

class Game(object):
	def __init__(self):
		self.players=[]





# get command line argument of server, port
if len(sys.argv) != 2:
	print "Usage:", sys.argv[0], "host:port"
	print "e.g.", sys.argv[0], "localhost:31425"
else:
	host, port = sys.argv[1].split(":")
	s = Serve(localaddr=(host, int(port)))
	s.Launch()
