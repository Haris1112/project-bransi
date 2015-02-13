import pygame
from pygame import Color, Surface
from pygame.font import Font

class MenuViewer:
	
	__i = 0
	__title = ""
	__choices = []

	__defaultTitleFont = None
	__defaultMenuFont = None

	__defaultTitleColor = None
	__defaultMenuColor = None

	__selectorType = 0

	# SelectorType1
	__padding = " "
	__selector = "> "
	__selector2 = " >"

	#SelectorType2
	__selector3 = "[]"

	def __init__(self, title="", choices=[], hud_size = 12, selectorType=1):
		self.__choices = choices
		self.__i = 0
		self.__selectorType = selectorType
		self.__defaultTitleFont = pygame.font.SysFont("monospace", hud_size*1.7))
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
		if self.__i >= len(self.__choices):
			self.__i = 0

	def prevChoice(self):
		self.__i -= 1
		if self.__i < 0
			self.__i = len(self.__choices) - 1

	def setIndex(self, index):
		if not index >= len(self.__choices) and not index < 0
			self.__i = index

	def getTitle(self):
		return self.__title.title()

	def getIndex(self):
		return self.__i

	def __getSelectString(self, string):
		if self.__selectorType == 1:
			return __defaultSelector + __padding + string
		elif self.__selectorType == 2:
			return __selector3[0] + __padding + string + __padding + __selector3[1]

	def getMenuSurface(self, titleFont=None, menuFont=None, titleColor=None, menuColor=None):
		tFont = self.__defaultTitleFont
		mFont = self.__defaultMenuFont
		tColor = self.__defaultTitleColor
		mColor = self.__defaultMenuColor
		if not titleFont == None:
			tFont = titleFont
		if not menuFont == None:
			mFont = menuFont
		if not titleColor == None:
			tColor = titleColor
		if not menuColor == None:
			mColor = menuColor

		surface = Surface((9001, 9001))

		tLabel = tFont.render(self.getTitle(), 1, tColor)
		mLabel = []
		i = 0
		while i < mLabel.
		for choice in self.__choices:
			mLabel.append(mFont.render(choice, 1, mColor))

		surface.blit(tLabel, (0, 0))
		i = 0
		while i < len(mLabel):
			if i == self.__i:
				
			i += 1


		return surface