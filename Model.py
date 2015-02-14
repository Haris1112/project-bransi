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
		self.player = Player(10, speed=100)
		self.monsters = []
		self.state = "game"

	def isRunning(self):
		return self.__running

	# delta is the change of time in seconds
	def gameUpdate(self, controller, delta):
		if controller.escape():
			self.__running = False
		self.player.update(controller, delta, self.world)

	def setState(self, state):
		self.__state = state

	def getState(self):
		return self.__state

	def exit(self):
		self.__running = False
