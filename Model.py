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
	__running = False
	state = ""

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

	def begin(self):
		self.state = "title"
		self.__running = True

	def newGame(self, width, height):
		self.player = Player(10, speed = 100)
		self.world = World(width, height)
		self.monsters = []
		self.__running = True

	def isRunning(self):
		return self.__running

	# delta is the change of time in seconds
	def gameUpdate(self, controller, delta):
		if controller.escape():
			self.__running = False
			print("done")
		self.player.update(controller, delta, self.world)
		pass

	def getState(self):
		return self.state