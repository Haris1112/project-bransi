'''
The Model

Created: Thursday, February 12, 2014
Author: Haris :)
Website: HappyHaris.com
GitHub: Haris1112
'''

from entity import *

class Model:

	# Game state
	__running = True
	__paused = True
	__state = ""

	# Game data
	player = None
	world = None
	particleManager = None
	inventory = None

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
		self.world = World(self, width, height)
		self.player = Player(self, self.world, 10, x=(width/2-5), y=(height/2-5), speed=250)
		self.inventory = Inventory()

		# Give initial items
		self.inventory.ammo = [90, 36, 5]
		weapon1 = Weapon(0, 15, 30, 2)
		weapon2 = Weapon(1, 4, 12, 1)
		weapon3 = None
		self.inventory.slot(0, weapon1)
		self.inventory.slot(1, weapon2)
		self.inventory.slot(2, weapon3)

		self.particleManager = ParticleManager()
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
			self.inventory.update(delta)
			self.particleManager.update(delta)

	def setState(self, state):
		self.__state = state

	def getState(self):
		return self.__state

	def exit(self):
		self.__running = False