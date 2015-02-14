import relations
import random
from pygame import Rect
from Controllable import Controllable

# Setup override checker!
def overrides(interface_class):
	def overrider(method):
		assert(method.__name__ in dir(interface_class))
		return method
	return overrider

class Player(Controllable):
	speed = 0
	size = 0
	x = 0
	y = 0

	money = 16000
	health = 10
	armor = 10

	__delta = 0
	__world = None

	def __init__(self, world, size, x=0, y=0, speed=1):
		self.__world = world
		self.size = size
		self.x = x
		self.y = y
		self.speed = speed
	
	def getBounds(self):
		return Rect(self.x, self.y, self.size, self.size)

	def update(self, input, delta, world):
		pass

	def getAim(self, mouseX, mouseY):
		pass

	@overrides(Controllable)
	def tick(self, time):
		self.__delta = time

	@overrides(Controllable)
	def up(self):
		self.y -= self.speed*self.__delta
		if(self.y < 0):
			self.y = 0

	@overrides(Controllable)
	def down(self):
		self.y += self.speed*self.__delta
		if(self.y > self.__world.height):
			self.y = self.__world.height - self.size

	@overrides(Controllable)
	def left(self):
		self.x -= self.speed*self.__delta
		if(self.x < 0):
			self.x = 0

	@overrides(Controllable)
	def right(self):
		self.x += self.speed*self.__delta
		if(self.x > self.__world.width):
			self.x = self.__world.width - self.size

	@overrides(Controllable)
	def primary(self):
		self.shoot()

	@overrides(Controllable)
	def secondary(self):	
		pass

	@overrides(Controllable)
	def action(self):
		pass

	@overrides(Controllable)
	def toggle(self):
		pass

	@overrides(Controllable)
	def use(self):
		pass

	@overrides(Controllable)
	def buy(self):
		pass

class Item:
	pass

class Monster:
	size = 0
	position = []
	hp = 0
	speed = 0
	money = 0
	loot = None
	
	def __init__(self, size, position, hp, speed, money, loot):
		self.size = size
		self.position = position
		self.hp = hp
		self.speed = speed
		self.money = money
		self.loot = loot

	def update(self, delta, target_position):
		t = target_position
		if(self.position[0] < t[0]):
			self.position[0] += self.speed*delta
		if(self.position[0] > t[0]):
			self.position[0] -= self.speed*delta
		if(self.position[1] < t[1]):
			self.position[1] += self.speed*delta
		if(self.position[1] > t[1]):
			self.position[1] -= self.speed*delta

	def getBounds(self):
		return Rect(self.position[0], self.position[1], self.size, self.size)

class World:
	monsterBank = 0
	monsters = []
	level = 0

	player = None
	width = 0
	height = 0

	def __init__(self, width=100, height=100):
		self.width = width
		self.height = height
		self.monsters = []
		self.monsterBank = 0

	def generateMonster(self, monster_level):
		size = random.randrange(10, 20 + 1)
		position = self.generatePositionOutside(0, 0, self.width, self.height)
		hp = relations.linear(monster_level, 1, 42)
		money = relations.linear(monster_level, 1, 1000)
		speed = relations.fastCurve(monster_level, 100, 350)
		loot = self.generateLoot(monster_level)
		m = Monster(size, position, hp, speed, money, loot)
		return m

	def generatePositionOutside(self, x, y, width, height, padding=100):
		w = width
		h = height
		p = padding

		# All rectangles surrounding area given in parameters
		#
		#	[][][]
		#	[]  []
		#	[][][]
		#

		rectangles = [
			#LEFT 	RIGHT 	UP 		DOWN
			[x-p, 	x, 		y-p, 	y],
			[x, 	x+w, 	y-p, 	y],
			[x+w, 	x+w+p, 	y-p, 	y],
			[x-p, 	x, 		y, 		y+h],
			[x+w, 	x+w+p, 	y, 		y+h],
			[x-p, 	x, 		y+h, 	y+h+p],
			[x, 	x+w, 	y+h, 	y+h+p],
			[x+w, 	x+w+p, 	y+h, 	y+h+p],
		]
		rect = random.choice(rectangles)

		x = random.randrange(rect[0], rect[1] + 1)
		y = random.randrange(rect[2], rect[3] + 1)
		
		return [x, y]


	def generateLoot(self, monsterLevel):
		return None # TODO FIXME

	def monstersLeft(self):
		return len(monsters)

	def spawnMonster(self):
		m = self.generateMonster(self.level)
		self.monsters.append(m)
		self.monsterBank -= 1

	def nextLevel(self):
		print("LEVEL: " + str(self.level))
		self.level += 1
		self.monsterBank += relations.fastCurve(self.level, 1, 100)

	# delta is in seconds
	def update(self, delta, target_position):
		if self.monsterBank <= 0 and len(self.monsters) <= 0:
			self.nextLevel()
		elif self.monsterBank > 0:
			for i in range(random.randrange(1,5)):
				self.spawnMonster()
		for monster in self.monsters:
			monster.update(delta, target_position)