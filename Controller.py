'''
The Controller

Created: Thursday, February 12, 2014
Author: Haris :)
Website: HappyHaris.com
GitHub: Haris1112
'''

import pygame
from pygame.locals import *

class Controller:
	
	'''
	HARD SETTINGS
	'''
	WIDTH = 540
	HEIGHT = 420
	SETTINGS_FILE = "settings.txt"
	
	__model = None
	__view = None

	__settings = {}

	def __init__(self, model, view):
		self.__model = model
		self.__view = view
		self.__loadSettings(self.SETTINGS_FILE)
		self.__start()

	def __start(self):
		self.__model.begin()
		self.__view.ready(self.WIDTH, self.HEIGHT, int(self.__settings['hud_size']))
		self.__gameLoop()

	def __newGame():
		self.__model.newGame(self.WIDTH, self.HEIGHT)

	def __gameLoop(self):
		# This is an edited version of the following general game loop:
		# http://entitycrisis.blogspot.ca/2007/07/general-pygame-main-loop.html   
		frame_rate = int(self.__settings['frame_rate'])

		step_size = 1.0 / frame_rate * 1000.0 # ms
		max_frame_time = 0.1 * 1000 # ms

		now = pygame.time.get_ticks()
		while self.__model.isRunning():
			if QUIT in [e.type for e in pygame.event.get()]:
				break

			T = pygame.time.get_ticks()

			if T - now > max_frame_time:
				now = T - step_size

			while(T - now >= step_size):
				# Update game state (seconds)
				if(self.__model.state == "game"):
					self.__model.gameUpdate(self, step_size / 1000.0)
				now += step_size
			else:
				pygame.time.wait(10)

			# Render game state
			# interpolate_time = 1.0 / (step_size / (T - now))
			self.__view.gameRender(self)

	def __loadSettings(self, fileName):
		array = []
		data = {}

		for line in open(fileName, "r").readlines():
			array = line.split("=")
			# Sanitise
			data[array[0].strip()] = array[1].strip()

		self.__settings = data

	'''''
	INPUT
	'''''
	def getMouse(self):
		return self.getMousePosition()

	def getMousePosition(self):
		return pygame.mouse.get_pos()

	def __keyPressed(self, key):
		return pygame.key.get_pressed()[key]

	def up(self):
		return self.__keyPressed(pygame.K_UP) or self.__keyPressed(pygame.K_w)

	def down(self):
		return self.__keyPressed(pygame.K_DOWN) or self.__keyPressed(pygame.K_s)

	def left(self):
		return self.__keyPressed(pygame.K_LEFT) or self.__keyPressed(pygame.K_a)

	def right(self):
		return self.__keyPressed(pygame.K_RIGHT) or self.__keyPressed(pygame.K_d)

	def escape(self):
		return self.__keyPressed(pygame.K_ESCAPE)

	def mouse1(self):
		return pygame.mouse.get_pressed()[0]

	def mouse2(self):
		return pygame.mouse.get_pressed()[1]