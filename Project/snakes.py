import csv

import numpy as np

np.random.seed(726366)

def prediction(age, traits, sex, time):
	"""Not yet implemented, will take those three arguments and return the price of the a snake with the given features."""
	print 'prediction is working thus far (for what it is worth)'

class Snake:
	"""This class defines an individual snake and instantiates its genetics"""
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
		self.price = 0
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
	def add_price(self):
		self.price = prediction(self.age, self.traits, self.sex, time)


r = Snake('Justine')
l = Snake('Jim')

m = Snake('j')
m.add_forebears(r, l)
data = list(csv.reader(open('prices.txt')))
for i in range(0,len(data)):
	data[i][1] = float(data[i][1])
	data[i][2] = float(data[i][2])
