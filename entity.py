from pygame import Rect

class Player:
	
	speed = 0
	size = 0
	x = 0
	y = 0

	money = 16000
	health = 100
	armor = 100

	def __init__(self, size, start_x=0, start_y=0, speed=1):
		self.size = size
		self.x = start_x
		self.y = start_y
		self.speed = speed
	
	def getBounds(self):
		return Rect(self.x, self.y, self.size, self.size)

	def update(self, input, delta, world):
		if input.down():
			self.y += self.speed*delta
			if(self.y > world.height):
			 self.y = world.height - self.size
		if input.up():
			self.y -= self.speed*delta
			if(self.y < 0):
				self.y = 0
		if input.left():
			self.x -= self.speed*delta
			if(self.x < 0):
				self.x = 0
		if input.right():
			self.x += self.speed*delta
			if(self.x > world.width):
				self.x = world.width - self.size

	def getAim(self, mouseX, mouseY):
		pass

class Monster:
	pass

class World:
	monsters = None
	level = 0

	width = 0
	height = 0

	def __init__(self, width, height):
		self.width = width
		self.height = height
		monsters = []

	def monstersLeft(self):
		return len(monsters)