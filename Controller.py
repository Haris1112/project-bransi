'''
The Controller

Created: Thursday, February 12, 2014
Author: Haris :)
Website: HappyHaris.com
GitHub: Haris1112
'''

import pygame, sys
from MenuViewer import MenuViewer
from pygame.locals import *

class Controller:
	
	'''
	HARD SETTINGS
	'''
	WIDTH = 540
	HEIGHT = 420
	__SETTINGS_FILE = "settings.txt"
	__keys = {}
	__titleMenuChoices = {}
	__settings = {}

	__model = None
	__view = None
	__controllable = None # input object

	#Controllables
	__titleMenuController = None

	# Statistics
	__fps = 0
	__frames = 0

	__ups = 0
	__updates = 0

	__lastStatisticGatherTime = 0

	def __init__(self, model, view):
		self.__model = model
		self.__view = view

		pygame.init()
		self.__loadSettings(self.__SETTINGS_FILE)

		self.__titleMenuController = MenuViewer("Project Bransi", self.__titleMenuChoices, int(self.__settings['hud_size']), selectorType=1)
		self.__view.ready(self.WIDTH, self.HEIGHT, self.__titleMenuController)
		self.__setState("title")
		
		self.__gameLoop()

	def __newGame(self):
		self.__model.newGame(self.WIDTH, self.HEIGHT)
		self.__setState("game")

	def __gameLoop(self):
		# This is an edited version of the following general game loop:
		# http://entitycrisis.blogspot.ca/2007/07/general-pygame-main-loop.html   
		frame_rate = int(self.__settings['frame_rate'])

		step_size = 1.0 / frame_rate * 1000.0 # ms
		time = step_size / 1000.0 # s
		max_frame_time = 0.1 * 1000 # ms

		now = pygame.time.get_ticks()
		while self.__model.isRunning():
			if QUIT in [e.type for e in pygame.event.get()]:
				print("QUITTED via QUIT event in pygame event pool.")
				break

			T = pygame.time.get_ticks()

			if T - now > max_frame_time:
				now = T - step_size

			while(T - now >= step_size):
				# Update game state (seconds)
				pygame.event.pump() # collect events
				self.__manageInput(time)
				if(self.__model.getState() == "game"):
					self.__model.gameUpdate(time)
				self.__updates += 1
				now += step_size
			else:
				pygame.time.wait(10)

			# Render game state
			# interpolate_time = 1.0 / (step_size / (T - now))
			self.__view.gameRender(self)
			self.__frames += 1

			# Statistics
			T = pygame.time.get_ticks()
			if(T - self.__lastStatisticGatherTime > 1000):
				self.__fps = self.__frames
				self.__ups = self.__updates
				self.__frames = 0
				self.__updates = 0
				self.__lastStatisticGatherTime = T

				# print(("FPS:" + str(self.__fps)), "UPS:" + str(self.__ups))


	def __loadSettings(self, fileName):
		# HARD CODED SETTINGS
		self.__keys = {
			pygame.K_UP 	: self.up,
			pygame.K_w 		: self.up,
			pygame.K_DOWN 	: self.down,
			pygame.K_s 		: self.down,
			pygame.K_LEFT 	: self.left,
			pygame.K_a 		: self.left,
			pygame.K_RIGHT 	: self.right,
			pygame.K_d 		: self.right,
			pygame.K_e 		: self.use,
			pygame.K_q		: self.toggle,
			pygame.K_f 		: self.action,
			pygame.K_b		: self.buy,
			pygame.K_ESCAPE : self.escape,
		}

		self.__titleMenuChoices = {
			"New Game"	:	self.__newGame,
			"Exit"		:	sys.exit,
		}

		array = []
		data = {}

		for line in open(fileName, "r").readlines():
			array = line.split("=")
			# Sanitise
			data[array[0].strip()] = array[1].strip()

		self.__settings = data

	''' INPUT '''
	def __manageInput(self, time):
		if not self.__controllable == None:
			self.__controllable.tick(time)
			inputs = pygame.key.get_pressed()
			for key in self.__keys:
				if inputs[key]:
					self.__keys[key]()
			pos = pygame.mouse.get_pos()
			self.__model.mX = pos[0]
			self.__model.mY = pos[1]					
			mouse = pygame.mouse.get_pressed()
			if mouse[0]:
				self.primary()
			if mouse[1]:
				self.secondary()

		if self.escape():
			self.__model.exit()

	def __setState(self, state):
		print("SETTING STATE:\t" + state)
		if state == "title":
			self.__setControllable(self.__titleMenuController)
			self.__model.setState("title")
			pygame.mouse.set_visible(True)
		if state == "game":
			self.__model.setState("game")
			self.__model.unPause()
			pygame.mouse.set_visible(False)
			self.__setControllable(self.__model.player)
		if state == "gameOver":
			self.__setControllable(None)
			self.__model.setState("gameOver")
			pygame.mouse.set_visible(True)

	def __setControllable(self, controllable):
		print("SETTING CONTROLLABLE\t" + str(type(controllable)))
		self.__controllable = controllable

	def setMousePosition(self, x, y):
		pygame.mouse.set_pos((x, y))

	def getMousePosition(self):
		return pygame.mouse.get_pos()

	def __keyPressed(self, key):
		return pygame.key.get_pressed()[key]

	''' KEYS & MOUSE'''
	def up(self):
		self.__controllable.up()

	def down(self):
		self.__controllable.down()

	def left(self):
		self.__controllable.left()

	def right(self):
		self.__controllable.right()

	def escape(self):
		return self.__keyPressed(pygame.K_ESCAPE)

	def primary(self):
		self.__controllable.primary()

	def secondary(self):
		self.__controllable.secondary()

	def action(self):
		self.__controllable.action()

	def toggle(self):
		self.__controllable.toggle()

	def use(self):
		self.__controllable.use()

	def buy(self):
		self.__controllable.buy()