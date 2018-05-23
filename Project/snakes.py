import csv
import time
import numpy as np
import pandas
import math

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
kept = []
def prediction(age, traits, sex, time):
	"""Not yet implemented, will take those three/four arguments and return the price of the a snake with the given features."""
	print 'prediction is working thus far (for what it is worth)'

class Snake:
	"""This class defines an individual snake and instantiates its genetics"""
	def __init__(self, name, parent1 = 0, parent2 = 0, traits = 0, sex = 0, age = 0):
		self.name = name
		if (not sex):
			sexnum = np.random.binomial(size = 1, n = 1, p = .5)[0]
			if (sexnum == 0):
				self.sex = 'Male'
			else:
				self.sex = 'Female'
		self.traits = []
		self.forebears = [self.name]
		self.parents = []
		self.age = age
		self.price = 0
		if (parent1 or parent2):
			if (not set(parent1.forebears).isdisjoint(parent2.forebears)):
				raise ValueError()
			if (parent1.sex == parent2.sex):
				raise ValueError()
		if (traits):
			self.traits = traits
	# def add_parents(self, parent1, parent2):
	# 	self.parents.append(parent1.name)
	# 	self.parents.append(parent2.name)
	def add_forebears(self, parent1, parent2):
		if (parent1.forebears):
			self.forebears= self.forebears + parent1.forebears
		if (parent2.forebears):
			self.forebears= self.forebears + parent2.forebears
		# self.forebears.append(parent1.name)
		# self.forebears.append(parent2.name)
	def add_price(self):
		self.price = prediction(self.age, self.traits, self.sex, curtime)

def breed(snake1,snake2):
	yesno = np.random.binomial(size = 1, n = 1, p = .6)[0]
	if (yesno == 0):
		pass
	else:
		numbabies = np.floor(np.random.triangular(2,6,13, 1))
		for i in range(1,numbabies):
			snakes.append( Snake(names[i], snake1,snake2))

snakes.append(Snake('a', sex = 'Male', age = 1, traits = [[recessives[0],recessives[0]],[codom[1],codom[1]]]))
snakes.append(Snake('b', sex = 'Female', age = 1))

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
try:
	breed(snakes[0],snakes[1])
except:
	pass
try:
	print(snakes[0].traits)
except:
	pass


