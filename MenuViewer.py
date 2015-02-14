import pygame
from pygame import Color, Surface
from pygame.font import Font
from Controllable import Controllable

# Setup override checker!
def overrides(interface_class):
	def overrider(method):
		assert(method.__name__ in dir(interface_class))
		return method
	return overrider

"""
This class needs to be refactored: it acts as a view and controller...
"""
class MenuViewer(Controllable):
	__i = 0
	__title = ""
	# Choices is a dictionary which contains menu options and corresponding methods
	# i.e.	{"New Game", newGame } -> where new game is a method
	__choices = {}

	__hud_size = 0

	__defaultTitleFont = None
	__defaultMenuFont = None

	__defaultTitleColor = None
	__defaultMenuColor = None

	__selectorType = 0
	__allowLooping = False

	# SelectorType1
	__padding = " "
	__selector = ["> ", " >"]

	#SelectorType2
	__selector2B = ["[", " "] # before content
	__selector2A = ["]", " "] # after content

	#Timer
	__timer = 0
	__acceptInput = True
	__thresh = 0.3 # s

	__blinkTimer = 0
	__blinkThresh = 0.25 # s
	__currMode = 0
	__maxMode = 2

	def __init__(self, title, choices, hud_size=12, selectorType=1, allowLooping=False):
		self.__choices = choices
		self.__i = 0
		self.__title = title
		self.__hud_size = hud_size
		self.__selectorType = selectorType
		self.__allowLooping = allowLooping
		self.__defaultTitleFont = pygame.font.SysFont("monospace", int(hud_size*1.7))
		self.__defaultMenuFont = pygame.font.SysFont("monospace", hud_size)
		self.__defaultTitleColor = Color(170, 170, 170, 255)
		self.__defaultMenuColor = Color(160, 160, 160, 255)

	def setTitle(self, title):
		self.__title = title

	def setChoices(self, choices):
		self.__choices = choices

	def setPadding(self, padding):
		self.__padding = padding

	def nextChoice(self):
		self.__i += 1
		maxI = len(self.__choices)
		if self.__i >= maxI:
			if self.__allowLooping:
				self.__i = 0
			else:
				self.__i = maxI - 1

	def prevChoice(self):
		self.__i -= 1
		if self.__i < 0:
			if(self.__allowLooping):
				self.__i = len(self.__choices) - 1
			else:
				self.__i = 0

	def setIndex(self, index):
		if not index >= len(self.__choices) and not index < 0:
			self.__i = index

	def setInputThreshold(self, threshold):
		self.__thresh = threshold

	def getTitle(self):
		return self.__title.title()

	def getIndex(self):
		return self.__i

	def select(self):
		func = self.__choices.values()[self.__i]
		func()

	def nextCursorFrame(self):
		self.__currMode += 1
		if(self.__currMode >= self.__maxMode):
			self.__currMode = 0

	def __getUnselectedString(self, string):
		if self.__selectorType == 1:
			return " " * len(self.__selector[0]) + self.__padding + string
		elif self.__selectorType == 2:
			return " " * len(self.__selector[0]) + string
		elif self.__selectorType == 3:
			return " " * len(self.__selector2B[0]) + self.__padding + string + self.__padding + " " * len(self.__selector2A[0])
		elif self.__selectorType == 4:
			return self.__padding + self.__selector2B[0] + string + self.__selector2A[0] + self.__padding

	def __getSelectString(self, string):
		if self.__selectorType == 1:
			return self.__selector[self.__currMode] + self.__padding + string
		elif self.__selectorType == 2:
			return self.__selector[self.__currMode] + self.__padding + string
		elif self.__selectorType == 3:
			return self.__selector2B[self.__currMode] + self.__padding + string + self.__padding + self. __selector2A[self.__currMode]
		elif self.__selectorType == 4:
			return self.__selector2B[self.__currMode] + self.__padding + string + self.__padding + self.__selector2A[self.__currMode]

	def getMenuSurface(self, titleFont=None, menuFont=None, titleColor=None, menuColor=None):
		surface = Surface((9001, 9001))

		if not self.getTitle() == "":
			tFont = self.__defaultTitleFont
			tColor = self.__defaultTitleColor
			if not titleFont == None:
				tFont = titleFont
			if not titleColor == None:
				tColor = titleColor

			tLabel = tFont.render(self.getTitle(), 1, tColor)
			surface.blit(tLabel, (0, 0))


		if not len(self.__choices) == 0:
			mFont = self.__defaultMenuFont
			mColor = self.__defaultMenuColor
			if not menuFont == None:
				mFont = menuFont
			if not menuColor == None:
				mColor = menuColor

			mLabels = []
			for i, key in enumerate(self.__choices):
				txt = key
				if i == self.__i:
					txt = self.__getSelectString(txt)
				else:
					txt = self.__getUnselectedString(txt)
				mLabels.append(mFont.render(txt, 1, mColor))

			offsetY = 0
			if not self.getTitle() == "":
				offsetY = tLabel.get_height()

			for idx, lbl in enumerate(mLabels):
				surface.blit(lbl, (0, offsetY + self.__hud_size*idx))

		return surface

	@overrides(Controllable)
	def tick(self, time):
		self.__timer += time
		self.__blinkTimer += time
		if not self.__acceptInput and self.__timer >= self.__thresh:
			self.__acceptInput = True
			self.__timer = 0
		if self.__blinkTimer >= self.__blinkThresh:
			self.__blinkTimer = 0
			self.nextCursorFrame()

	@overrides(Controllable)
	def up(self):
		if(self.__acceptInput):
			self.prevChoice()
			self.__acceptInput = False

	@overrides(Controllable)
	def down(self):
		if(self.__acceptInput):
			self.nextChoice()
			self.__acceptInput = False

	@overrides(Controllable)
	def left(self):
		if(self.__acceptInput):
			self.prevChoice()
			self.__acceptInput = False

	@overrides(Controllable)
	def right(self):
		if(self.__acceptInput):
			self.nextChoice()
			self.__acceptInput = False

	@overrides(Controllable)
	def primary(self):
		pass

	@overrides(Controllable)
	def secondary(self):	
		pass

	@overrides(Controllable)
	def action(self):
		self.select()

	@overrides(Controllable)
	def toggle(self):
		pass

	@overrides(Controllable)
	def use(self):
		self.select()

	@overrides(Controllable)
	def buy(self):
		pass