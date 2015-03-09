import math
import random

class Vector2:
	x = 0
	y = 0

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	@staticmethod
	def randomUnitVector():
		azimuth = random.random() * 2 * math.pi
		return Vector2(math.cos(azimuth), math.sin(azimuth))

	def add(self, vector2):
		return Vector2(self.x + vector2.x, self.y + vector2.y)

	def subtract(self, vector2):
		return Vector2(self.x - vector2.x, self.y - vector2.y)

	def scalar(self, value):
		return Vector2(self.x * value, self.y * value)

	def __str__(self):
		return "({}, {})".format(int(self.x), int(self.y))