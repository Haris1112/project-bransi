'''
The View

Created: Thursday, February 12, 2014
Author: Haris :)
Website: HappyHaris.com
GitHub: Haris1112
'''

import pygame
from pygame import Rect, Color

class View:

	__model = None
	__surface = None

	# Screens
	titleMenu = None
	
	# Colours
	black = Color(15, 15 ,15, 255)
	gray = Color(105, 105, 105, 255)
	white = Color(240, 240, 240, 255)
	bloodred = Color(240, 30, 30, 255)
	bloodorange = Color(230, 220, 30, 255)
	
	# Fonts
	font = None
	font2 = None
	selector1 = "> "

	# Timing
	i = 0
	last = 0

	def __init__(self, model):
		self.__model = model

	def ready(self, width, height, titleMenu):
		self.__surface = pygame.display.set_mode((width, height))
		self.titleMenu = titleMenu

	def gameRender(self, controller):
		screen = self.__surface
		mouse = controller.getMousePosition()

		# Clear surface
		screen.fill((0, 0, 0))

		if self.__model.getState() == "title" and not self.titleMenu == None:
			screen.blit(self.titleMenu.getMenuSurface(), (0, 0))
		elif self.__model.getState() == "game":
			pygame.draw.rect(screen, self.gray, self.__model.player.getBounds())
			pygame.draw.rect(screen, self.bloodred, Rect(mouse[0], mouse[1], 2, 2))
		else: # Game Over
			label = self.font.render("Game-Over", 1, self.bloodorange)
			screen.blit(label, (10, 100))

		pygame.display.flip()