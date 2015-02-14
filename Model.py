'''
The Model

Created: Thursday, February 12, 2014
Author: Haris :)
Website: HappyHaris.com
GitHub: Haris1112
'''

from entity import Player, Monster, World

class Model:

	# Game state
	__running = True
	__paused = True
	__state = ""

	# Game data
	player = None
	world = None

	# Input data
	up = False
	down = False
	left = False
	right = False
	mX = 0
	mY = 0

	def __init__(self):
		pass

	def newGame(self, width, height):
		self.world = World(width, height)
		self.player = Player(self.world, 10, x=(width/2-5), y=(height/2-5), speed=250)
		self.state = "game"
		self.__pause = False

	def isRunning(self):
		return self.__running

	def isPaused(self):
		return self.__paused

	def unPause(self):
		self.__paused = False

	# delta is the change of time in seconds
	def gameUpdate(self, delta):
		if not self.__paused:
			self.world.update(delta, (self.player.x, self.player.y))

	def setState(self, state):
		self.__state = state

	def getState(self):
		return self.__state

	def exit(self):
		self.__running = False
