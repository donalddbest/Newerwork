import csv
import time
import numpy as np
import pandas

df = pandas.read_csv('babies-first-names-1980-1989.csv')
names = df.FirstForename
names = np.unique(names)
names = names[2:len(names)]
recessives = ['Albino','Clown','Axanthic']
codom = ['Pastel', 'Fire', 'Banana']

# np.random.seed(726366)
curtime = time.time() 
capacity = 3
snakes = []
def prediction(age, traits, sex, time):
	"""Not yet implemented, will take those three/four arguments and return the price of the a snake with the given features."""
	print 'prediction is working thus far (for what it is worth)'

class Snake:
	"""This class defines an individual snake and instantiates its genetics"""
	def __init__(self, name, parent1 = 0, parent2 = 0, traits = 0):
		self.name = name
		sexnum = np.random.binomial(size = 1, n = 1, p = .5)[0]
		if (sexnum == 0):
			self.sex = 'Male'
		else:
			self.sex = 'Female'
		self.traits = []
		self.forebears = [self.name]
		self.parents = []
		self.age = 0
		self.price = 0
		if (parent1 or parent2):
			if (not set(parent1.forebears).isdisjoint(parent2.forebears)):
				raise ValueError()
			if (parent1.sex == parent2.sex):
				raise ValueError()

	def add_trait(self, trait):
		self.traits.append(trait)
	
	# def add_parents(self, parent1, parent2):
	# 	self.parents.append(parent1.name)
	# 	self.parents.append(parent2.name)
	def add_forebears(self, parent1, parent2):
		if (parent1.forebears):
			self.forebears.append(parent1.forebears)
		if (parent2.forebears):
			self.forebears.append(parent2.forebears)
		self.forebears.append(parent1.name)
		self.forebears.append(parent2.name)
	def add_price(self):
		self.price = prediction(self.age, self.traits, self.sex, curtime)


snakes.append(Snake('a'))
snakes.append(Snake('b'))

snakes.append(Snake('c'))
snakes.append(Snake('d'))
snakes[2].add_forebears(snakes[0],snakes[1])
snakes[3].add_forebears(snakes[0],snakes[1])

data = list(csv.reader(open('prices.txt')))
for i in range(0,len(data)):
	data[i][1] = float(data[i][1])
	data[i][2] = float(data[i][2])

try:
	print Snake('f',snakes[0],snakes[1]).forebears
except:
	pass