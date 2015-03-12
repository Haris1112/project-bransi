import abc

class Controllable(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def tick(self, time):
		"""For time management, passes time passed"""
		return

	@abc.abstractmethod
	def up(self):
		"""Action when Up key is pressed"""
		return

	@abc.abstractmethod
	def down(self):
		"""Action when Down key is pressed"""
		return

	@abc.abstractmethod
	def left(self):
		"""Action when Left key is pressed"""
		return

	@abc.abstractmethod
	def right(self):
		"""Action when Right key is pressed"""
		return

	@abc.abstractmethod
	def primary(self):
		"""Action when Primary mouse button is pressed"""
		return

	@abc.abstractmethod
	def secondary(self):
		"""Action when Secondary mouse button is pressed"""
		return

	@abc.abstractmethod
	def action(self):
		"""Action when Action key is pressed"""
		return

	@abc.abstractmethod
	def toggle(self):
		"""Action when Toggle key is pressed"""
		return

	@abc.abstractmethod
	def use(self):
		"""Action when Use key is pressed"""
		return

	@abc.abstractmethod
	def buy(self):
		"""Action when Buy key is pressed"""
		return

	@abc.abstractmethod
	def refresh(self):
		"""Action when Refresh key is pressed"""
		return

	@abc.abstractmethod
	def slot1(self):
		"""Action when Slot1 key is pressed"""
		return

	@abc.abstractmethod
	def slot2(self):
		"""Action when Slot2 key is pressed"""
		return

	@abc.abstractmethod
	def slot3(self):
		"""Action when Slot3 key is pressed"""
		return