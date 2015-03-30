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

	WIDTH = 0
	HEIGHT = 0

	# Map
	xOffset = 32
	yOffset = 32

	# Screens
	titleMenu = None
	
	# Colours
	black = Color(15, 15 ,15, 255)
	gray = Color(105, 105, 105, 255)
	white = Color(240, 240, 240, 255)
	bloodred = Color(240, 30, 30, 255)
	bloodyellow = Color(230, 220, 30, 255)
	bloodorange = Color(200, 200, 50, 255)
	marble = Color(195, 190, 178, 255)
	darkmarble = Color(130, 130, 112, 255)

	tiles = {
		1:	Color(40, 124, 40, 255),
		2: 	Color(70, 70, 71, 255),
	}
	
	# Fonts
	__font12 = None
	__font16 = None

	# Timing
	i = 0
	last = 0

	def __init__(self, model):
		self.__model = model

	def ready(self, width, height, titleMenu):
		self.WIDTH = width
		self.HEIGHT = height
		self.__surface = pygame.display.set_mode((width, height))
		self.titleMenu = titleMenu

		self.__font12 = pygame.font.SysFont("monospace", 12)
		self.__font16 = pygame.font.SysFont("monospace", 16)

	def gameRender(self, controller):
		screen = self.__surface
		mouse = controller.getMousePosition()

		# Clear surface
		screen.fill((0, 0, 0))

		if self.__model.getState() == "title" and not self.titleMenu == None:
			screen.blit(self.titleMenu.getMenuSurface(), (0, 0))
		elif self.__model.getState() == "game":
			#Draw Map
			data = self.__model.world.data
			r = None
			for i in range(len(data)):
				for j in range(len(data[0])):
					r = Rect(j*32 + self.xOffset, i*32 + self.yOffset, 32, 32)
					pygame.draw.rect(screen, self.tiles[data[i][j]], r)


			#Draw Monsters
			for monster in self.__model.world.monsters:
				pygame.draw.rect(screen, self.darkmarble, monster.getBounds(self.xOffset, self.yOffset))

			#Draw Particles
			for p in self.__model.particleManager.particles:
				pygame.draw.circle(screen, self.bloodorange, (int(p.pos.x)+self.xOffset, int(p.pos.y)+self.yOffset), int(p.size))

			# Draw Player, Cursor
			pygame.draw.rect(screen, self.marble, self.__model.player.getBounds(self.xOffset, self.yOffset))
			pygame.draw.rect(screen, self.bloodred, Rect(mouse[0], mouse[1], 2, 2))

			# Draw HUD
			health = self.__font12.render("|"*self.__model.player.health, 1, self.bloodred)
			armor = self.__font12.render("|"*self.__model.player.armor, 1, self.bloodyellow)
			money = self.__font16.render("${:,}".format(self.__model.player.money), 1, self.white)

			weaponID = self.__model.inventory.selected_weapon
			ammo = self.__model.inventory.slot(weaponID)
			ammoMax = self.__model.inventory.ammo[weaponID]
			weapon = self.__font12.render(str(ammo) + " / " + str(ammoMax), 1, self.white)
			numMonsters = self.__font16.render(str(len(self.__model.world.monsters)), 1, self.white)

			screen.blit(money, (10, 10))
			screen.blit(health, (10, 10 + money.get_height()))
			screen.blit(armor, (10, 10 + health.get_height() + money.get_height()))
			screen.blit(weapon, (self.WIDTH - weapon.get_width() - 10, self.HEIGHT - weapon.get_height() - 10))
			screen.blit(numMonsters, (10, self.HEIGHT - numMonsters.get_height() - 10))

			# DEBUG
			print("FPS" + str(controller.getFPS()))
			lbl = self.__font16.render("FPS " + str(controller.getFPS()), 1, self.white)
			pos = (32*0, 32*17)
			screen.blit(lbl, pos)
			
			#path_data = self.__model.world.path_data
			#for i in range(len(path_data)):
			#	for j in range(len(path_data[0])):
			#		lbl = self.__font16.render(str(path_data[i][j]), 1, self.white)
			#		pos = (j*32, i*32)
			#		screen.blit(lbl, pos)


		elif self.__model.getState() == "gameOver": # Game Over
			label = self.__font16.render("Game-Over", 1, self.bloodyellow)
			screen.blit(label, (10, 100))

		pygame.display.flip()