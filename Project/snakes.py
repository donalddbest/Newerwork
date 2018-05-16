import numpy as np

np.random.seed(726366)

class Snake:
	"""This class defines an individual snake and instantiates it's genetics"""
	def __init__(self, name):
		self.name = name
		sexnum = np.random.binomial(size = 1, n = 1, p = .5)[0]
		if (sexnum == 0):
			self.sex = 'Male'
		else:
			self.sex = 'Female'
		self.traits = []
		self.forebears = []
		self.parents = []
		self.age = 0
	def add_trait(self, trait):
		self.traits.append(trait)
	
	def add_parents(self, parent1, parent2):
		self.parents.append(parent1.name)
		self.parents.append(parent2.name)
	def add_forebears(self, parent1, parent2):
		if (parent1.forebears):
			self.forebears.append(parent1.forebears)
		if (parent2.forebears):
			self.forebears.append(parent2.forebears)
		self.forebears.append(parent1.name)
		self.forebears.append(parent2.name)
		self.add_parents(parent1, parent2)

r = Snake('Justine')
l = Snake('Jim')

m = Snake('j')
m.add_forebears(r, l)