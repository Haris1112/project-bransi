import relations
import random
import pygame
import math
from gameMath import *
from pygame import Rect
from Controllable import Controllable

# Setup override checker!
def overrides(interface_class):
	def overrider(method):
		assert(method.__name__ in dir(interface_class))
		return method
	return overrider

class ParticleManager:
	particles = []

	def __init__(self):
		pass

	def addParticle(self, particle):
		self.particles.append(particle)

	def update(self, delta):
		for p in self.particles:
			p.update(delta)
			if(p.life <= 0):
				self.particles.remove(p)

class Particle:
	life = 0 # Seconds
	size = 0
	speed = 0
	pos = None
	vel = None

	def __init__(self, life=2, size=0, speed=10, x=0, y=0):
		self.life = life
		self.size = size
		self.speed = speed
		self.pos = Vector2(x, y)
		self.vel = Vector2.randomUnitVector().scalar(self.speed)

	def update(self, time):
		self.pos = self.pos.add(self.vel)
		self.life -= time

class Player(Controllable):
	speed = 0
	size = 0
	x = 0				# unit: tile
	y = 0				# unit: tile

	money = 16000
	health = 10
	armor = 10

	__delta = 0
	__model = None
	__world = None

	def __init__(self, model, world, size, x=0, y=0, speed=1):
		self.__model = model
		self.__world = world
		self.size = size
		self.x = x
		self.y = y
		self.speed = speed

	def shoot(self):
		if(not self.__model.inventory.weapon() == None):
			f = self.__model.inventory.weapon().shoot()
			if f >= 0:
				x = self.__model.mX
				y = self.__model.mY
				pygame.mouse.set_pos((x + random.random()*f - f/2.0, y + random.random()*f - f/2.0))
				damage = 1
				effect = Particle(life=0.1, size=1, speed=2, x=x-32, y=y-32)
				self.__model.particleManager.addParticle(effect)
				self.__world.collide((x, y), damage)
		else:
			f = 0
			x = self.__model.mX
			y = self.__model.mY
			damage = 99
			for z in range(20):
				self.__model.particleManager.addParticle(Particle(size=2, life=0.5, x=x, y=y))
				self.__world.collide((x, y), damage);


	def getBounds(self, xOffset, yOffset):
		return Rect(self.x*self.__model.TILE_SIZE + xOffset, self.y*self.__model.TILE_SIZE + yOffset, self.size, self.size)

	def getAngle(self, mouseX, mouseY):
		pass

	@overrides(Controllable)
	def tick(self, time):
		self.__delta = time

	@overrides(Controllable)
	def up(self):
		if(self.__world.canWalk(int(self.x), int(self.y-self.speed*self.__delta))):
			self.y -= self.speed*self.__delta
			if(self.y < 0):
				self.y = 0

	@overrides(Controllable)
	def down(self):
		if(self.__world.canWalk(int(self.x), int(self.y+self.speed*self.__delta))):
			self.y += self.speed*self.__delta
			if(self.y > len(self.__world.data)):
				self.y = len(self.__world.data) - self.size/32.0

	@overrides(Controllable)
	def left(self):
		if(self.__world.canWalk(int(self.x-self.speed*self.__delta), int(self.y))):
			self.x -= self.speed*self.__delta
			if(self.x < 0):
				self.x = 0

	@overrides(Controllable)
	def right(self):
		if(self.__world.canWalk(int(self.x+self.speed*self.__delta), int(self.y))):
			self.x += self.speed*self.__delta
			if(self.x > len(self.__world.data[0])):
				self.x = len(self.__world.data[0]) - self.size/32.0

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
		self.__model.inventory.nextWeapon()

	@overrides(Controllable)
	def use(self):
		pass

	@overrides(Controllable)
	def buy(self):
		pass

	@overrides(Controllable)
	def refresh(self):
		self.__model.inventory.reload()

	@overrides(Controllable)
	def slot1(self):
		self.__model.inventory.selected_weapon = 0

	@overrides(Controllable)
	def slot2(self):
		self.__model.inventory.selected_weapon = 1

	@overrides(Controllable)
	def slot3(self):
		self.__model.inventory.selected_weapon = 2

class Inventory:
	selected_weapon = 0

	weapons = []
	ammo = []

	def __init__(self):
		# Assault, Pistol, Grenades
		self.weapons = [None, None, None]
		self.ammo = [0, 0, 0]

	def slot(self, id, weapon=None):
		if not weapon == None:
			self.weapons[id] = weapon
		return self.weapons[id]

	def weapon(self):
		return self.weapons[self.selected_weapon]

	def reload(self):
		w = self.weapon()
		if not w == None:
			self.ammo[self.selected_weapon] = w.reload(self.ammo[self.selected_weapon])

	def nextWeapon(self):
		self.selected_weapon += 1
		if self.selected_weapon >= len(self.weapons):
			self.selected_weapon = 0

	def update(self, time):
		for w in self.weapons:
			if(w is not None):
				w.update(time)

class Weapon:
	ammo_type = -1
	reload_time = -1
	reloading = False
	bps = -1 # Bullets per second
	magazine = 0
	magazine_size = 0

	time = 0

	def __init__(self, ammo_type, bps, magazine_size, reload_time):
		self.ammo_type = ammo_type
		self.reload_time = reload_time
		self.bps = bps
		self.magazine = 0
		self.magazine_size = magazine_size

	# Returns -1 	if unable to shoot
	#				else a number which indicates magnitude of recoil
	def shoot(self):
		if(self.time >= 1.0 / self.bps and not self.reloading):
			if(self.magazine > 0):
				self.time = 0
				self.magazine -= 1
				return self.recoil()
			else:
				self.emptyNoise()
				return -1

	def recoil(self):
		return 3

	def emptyNoise(self):
		# TODO Play no ammo noise, *click*
		return

	def reload(self, ammo):
		if(self.reloading or self.magazine == self.magazine_size):
			return ammo
		if(ammo >= self.magazine_size):
			self.time = 0
			self.reloading = True
			self.magazine = self.magazine_size
			ammo -= self.magazine_size
			return ammo
		else:
			self.time = 0
			self.reloading = True
			self.magazine = ammo
			return 0

	def update(self, time):
		self.time += time
		if(self.reloading):
			if(self.time >= self.reload_time):
				self.time = 0
				self.reloading = False

	def __str__(self):
		if(self.reloading):
			percent = int(self.time / self.reload_time * 10)
			return "|" * percent + " " * (10 - percent)
		return str(self.magazine)

class Monster:
	TILE_SIZE = 32

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

	def hurt(self, force):
		if(self.hp > 0):
			self.hp -= force
			if(self.hp <= 0):
				return True
		return False

	def getBounds(self, xOffset, yOffset):
		return Rect(self.position[0]*self.TILE_SIZE + xOffset, self.position[1]*self.TILE_SIZE + yOffset, self.size, self.size)

class World:
	__model = None

	monsterBank = 0
	monsters = []
	level = 0

	width = 0
	height = 0

	data = []
	path_data = []

	def __init__(self, model, width=100, height=100):
		self.__model = model
		self.width = width
		self.height = height
		self.monsters = []
		self.monsterBank = 0
		self.data = [
			[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
			[2,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
			[2,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
			[2,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
			[2,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
			[2,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
			[2,1,1,1,1,1,1,2,1,1,1,1,1,1,2],
			[2,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
			[2,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
			[2,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
			[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
		]

	def reset_path_data(self):
		self.path_data = [
			[128,128,128,128,128,128,128,128,128,128,128,128,128,128,128],
			[128,128,128,128,128,128,128,128,128,128,128,128,128,128,128],
			[128,128,128,128,128,128,128,128,128,128,128,128,128,128,128],
			[128,128,128,128,128,128,128,128,128,128,128,128,128,128,128],
			[128,128,128,128,128,128,128,128,128,128,128,128,128,128,128],
			[128,128,128,128,128,128,128,128,128,128,128,128,128,128,128],
			[128,128,128,128,128,128,128,128,128,128,128,128,128,128,128],
			[128,128,128,128,128,128,128,128,128,128,128,128,128,128,128],
			[128,128,128,128,128,128,128,128,128,128,128,128,128,128,128],
			[128,128,128,128,128,128,128,128,128,128,128,128,128,128,128],
			[128,128,128,128,128,128,128,128,128,128,128,128,128,128,128],
		]

	def collide(self, point, force):
		for m in self.monsters:
			if(m.getBounds(32, 32).collidepoint(point)):
				if(m.hurt(force)):
					self.__model.player.money += m.money
					# TODO: loot calculation

	def canWalk(self, tileX, tileY):
		if(self.data[tileY][tileX] == 2):
			return False
		return True

	def computePathData(self, playerX, playerY):
		t1 = pygame.time.get_ticks()
		self.reset_path_data()

		# Begin with first 'node' as player position
		self.__assignValue(int(playerX), int(playerY), 0)
		t2 = pygame.time.get_ticks()

	def __assignValue(self, x, y, val):
		if(x < 0 or x >= len(self.data[0]) or y < 0 or y >= len(self.data) or self.data[y][x] == 2 or self.path_data[y][x] <= val):
			return
		self.path_data[y][x] = val
		self.__assignValue(x-1, y, val+1)
		self.__assignValue(x+1, y, val+1)
		self.__assignValue(x, y-1, val+1)
		self.__assignValue(x, y+1, val+1)

	def generateMonster(self, monster_level):
		size = random.randrange(10, 20 + 1)
		position = [1, 0]
		hp = relations.linear(monster_level, 1, 42)
		money = relations.linear(monster_level, 1, 1000)
		speed = relations.fastCurve(monster_level, 5, 22)
		loot = self.generateLoot(monster_level)
		m = Monster(size, position, hp, speed, money, loot)
		return m

	# @deprecated
	def generatePositionOutside(self, x, y, width, height, padding=10):
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
		self.level += 1
		self.monsterBank += relations.fastCurve(self.level, 1, 100)

		# Sparkle effect :)
		x = self.__model.player.x*32 #tileSIZE
		y = self.__model.player.y*32 #tileSIZE
		for z in range(10):
			self.__model.particleManager.addParticle(Particle(x=x, y=y))

	# delta is in seconds
	def update(self, delta, target_position):
		if self.monsterBank <= 0 and len(self.monsters) <= 0:
			self.nextLevel()
		elif self.monsterBank > 0:
			for i in range(random.randrange(1,5)):
				self.spawnMonster()
		for monster in self.monsters:
			if(monster.hp <= 0):
				self.monsters.remove(monster)
			else:
				monster.update(delta, target_position)
		self.computePathData(self.__model.player.x, self.__model.player.y)
