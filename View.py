'''
The View

Created: Thursday, February 12, 2014
Author: Haris :)
Website: HappyHaris.com
GitHub: Haris1112
'''

import pygame
from pygame import Rect, Color
from pygame.font import Font

class View:

	__model = None
	__surface = None
	
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

	def ready(self, width, height, hudsize):
		pygame.init()
		self.__surface = pygame.display.set_mode((width, height))
		pygame.mouse.set_visible(False)
		self.font = pygame.font.SysFont("monospace", hudsize)
		self.font2 = pygame.font.SysFont("monospace", int(hudsize*1.7))


	def gameRender(self, controller):
		screen = self.__surface
		mouse = controller.getMouse()

		# Clear surface
		screen.fill((0, 0, 0))

		if self.__model.getState() == "title":
			if(controller.up()):
				self.i = 0
			elif(controller.down()):
				self.i = 1

			text1 = "Project Anbris"
			label = self.font2.render(text1, 1, self.bloodorange)
			screen.blit(label, (10, 100))

			text2 = ""
			text3 = ""

			color2 = self.gray
			color3 = self.gray

			now = pygame.time.get_ticks()
			if(now - self.last) > 500:
				self.last = now
				if(self.selector1 == "> "):
					self.selector1 = " >"
				else:
					self.selector1 = "> "

			if self.i == 0:
				text2 = self.selector1 + " New game"
				text3 = "  Exit"
				color2 = self.white
			else:
				text2 = "  New Game"
				text3 = self.selector1 + " Exit"
				color3 = self.white

			label2 = self.font.render(text2, 1, color2)
			screen.blit(label2, (10, 300))

			label3 = self.font.render(text3, 1, color3)
			screen.blit(label3, (10, 340))

		elif self.__model.getState() == "game":
			pygame.draw.rect(screen, self.gray, self.__model.player.getBounds())
			pygame.draw.rect(screen, self.bloodred, Rect(mouse[0], mouse[1], 2, 2))
		else: # Game Over
			label = self.font.render("Game-Over", 1, self.bloodorange)
			screen.blit(label, (10, 100))

		pygame.display.flip()