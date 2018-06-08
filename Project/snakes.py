from __future__ import division
import csv
import time
import numpy as np
import pandas
import math
from pyomo.environ import *


df = pandas.read_csv('babies-first-names-1980-1989.csv')
names = df.FirstForename
names = np.unique(names)
names = names[2:len(names)]
data = list(csv.reader(open('prices.txt')))
for i in range(0,len(data)):
	data[i][1] = float(data[i][1])
	# data[i][2] = float(data[i][2])
traitsfile = open('traitsfile.txt','w')
breedingrule = 0

recessives = ['Albino','Clown','Axanthic']
codom = ['Pastel', 'Fire', 'Banana']

# np.random.seed(726366)
nameindex = 0
curtime = time.time() 
capacity = 15
snakes = []
def prediction(age, traits, sex, time):
	"""Not yet implemented, will take those three/four arguments and return the price of the a snake with the given features."""

class Snake:
	"""This class defines an individual snake and instantiates its genetics"""
	def __init__(self, name, parent1 = 0, parent2 = 0, traits = 0, sex = 0, age = 0):
		self.name = name
		self.numTimesBred = 0
		# Randomly assigns Male or Female to a snake
		if (sex == 0):
			sexnum = np.random.binomial(size = 1, n = 1, p = .5)[0]
			if (sexnum == 0):
				self.sex = 'Male'
				self.numTimesBreedable = 5
				self.ageBreedable = 1
			else:
				self.sex = 'Female'
				self.numTimesBreedable = 1
				self.ageBreedable = 2
		else:
			self.sex = sex
			if (sex == 'Male'):
				self.numTimesBreedable = 5
				self.ageBreedable = 1
			else:
				self.numTimesBreedable = 1
				self.ageBreedable = 2
		self.traits = []
		self.forebears = [self.name]
		self.parents = []
		self.age = age
		self.price = 15
		traitsfromparent1 = []
		traitsfromparent2 = []
		traitlist = []
		# Checks whether you can breed the parents at all and if not kills the initialization
		if (parent1 or parent2):
			# Checks whether you would be inbreeding
			if (not set(parent1.forebears).isdisjoint(parent2.forebears)):
				raise ValueError()
			# Checks whether parents are same sex
			if (parent1.sex == parent2.sex):
				raise ValueError()
			else:
				self.forebears = self.forebears+parent1.forebears+parent2.forebears
		# Instantiation of morphs
		# Checks whether it's a starting snake
		if (traits != 0):
			self.traits = traits
		# Assigns half of the genes from one parent and half from the other.
		else:
			for i in range(0,len(parent1.traits)):
				# Gets morphs from parent1
				if (len(parent1.traits[i]) == 1):
					if (np.random.binomial(size = 1, n = 1, p = .5) == 1):
						traitsfromparent1.append(parent1.traits[i][0])
					else:
						pass
				else:
					traitsfromparent1.append(parent1.traits[i][0])
			for i in range(0,len(parent2.traits)):
				# Gets morphs from parent2
				if (len(parent2.traits[i]) == 1):
					if (np.random.binomial(size = 1, n = 1, p = .5) == 1):
						traitsfromparent2.append(parent2.traits[i][0])
					else:
						pass
				else:
					traitsfromparent2.append(parent2.traits[i][0])
			traitlist = traitsfromparent2+traitsfromparent1
			traitlist.sort()
			i = 0
			while (i<len(traitlist)):
				if (i+1 >= len(traitlist)):
					newtrait = [traitlist[i]]
					self.traits.append(newtrait)
					i = i + 25
					break

				else:
					if traitlist[i] == traitlist[i+1]:
						newtrait = [traitlist[i],traitlist[i+1]]
						i = i+2
					else:
						newtrait = [traitlist[i]]
						i = i+1
					self.traits.append(newtrait)
		# Assigns price to snake
		# In progress
		for i in range(0,len(self.traits)):
			for j in range(0,len(data)):
				if self.traits[i][0] == data[j][0]:
					self.price = self.price + data[j][1]
				else:
					pass



def breed(snake1,snake2):
	"""Given two snakes, determines whether they can breed and if they can possibly generates a clutch and if it generates a clutch generates a variable number of babies."""
	yesno = np.random.binomial(size = 1, n = 1, p = .6)[0]
	if (snake1.numTimesBreedable <= snake1.numTimesBred + 1 or snake2.numTimesBreedable <= snake2.numTimesBred + 1) and (snake1.age>=snake1.ageBreedable and snake2.age>=snake2.ageBreedable) and (snake1.sex != snake2.sex):
		if (yesno == 0):
			pass
		else:
			snake2.numTimesBred = snake2.numTimesBred + 1
			snake1.numTimesBred = snake1.numTimesBred + 1
			numbabies = np.floor(np.random.triangular(2,6,13, 1))
			for i in range(1,numbabies):
				global nameindex
				transitive.append( Snake(names[nameindex], snake1,snake2))
				nameindex = nameindex + 1

def hypobreed(snake1, snake2):
	# Edit this so it actually does expected values!!!!!
	exprev = 0
	traitlist = []
	if (not set(snake1.forebears).isdisjoint(snake2.forebears)):
		return 0
	# Checks whether parents are same sex
	elif (snake1.sex == snake2.sex):
		return 0
		# Make a probability matrix for offspring and a price matrix for that 
	else:
		for trait in snake1.traits:
			traitlist = traitlist + trait
		for i in range(0, len(data)):
			for trait in traitlist:
				if trait == data[i][0]:
					exprev = exprev + .25*data[i][1]
		for trait in snake2.traits:
			traitlist = traitlist + trait
		for i in range(0, len(data)):
			for trait in traitlist:
				if trait == data[i][0]:
					exprev = exprev + .25*data[i][1]
	return exprev + 20
def tick(snakes, transitive):
	"""This function will simulate a year, so will age every snake 1 year and will call breed on the most valuable snakes and decide which snakes to keep and sell down to capacity."""
	for i in range(0, len(snakes)):
		snakes[i].age = snakes[i].age + 1
	smales = sorted([snake for snake in snakes if snake.sex == 'Male'], key = lambda x: x.price, reverse = True)
	sfemales = sorted([snake for snake in snakes if snake.sex == 'Female'], key = lambda x: x.price, reverse = True)
	for i in range(0,len(smales)):
		for j in range(0,len(sfemales)):

			try:
				breed(smales[i],sfemales[j])
				# if smales[i].numTimesBred == smales[i].numTimesBreedable:
				# 	del smales[i]
				# else:
				# 	pass
				# del sfemales[j]

			except:
				pass
	
	if breedingrule == 1:
		if capacity> len(transitive):
			snakes = transitive
		else:
			rand = np.random.randint(0,len(transitive), size = l)
			snakes = [transitive[index] for index in rand]
		return 0
	males = [snake for snake in transitive if snake.sex == 'Male']
	females = [snake for snake in transitive if snake.sex == 'Female']
	if breedingrule == 0:
		utmat = []
		vars = []
		for i in range(0, len(males)):
			utmat.append([])
			for j in range(0, len(females)):
				try:
					utmat[i].append(hypobreed(males[i],females[j]))
				except:
					pass
		utmat = dict(((i+1,j+1), utmat[i][j]) for i in range(len(utmat)) for j in range(len(utmat[0])))
		print utmat
		model = AbstractModel()
		
		model.I = range(len(males))
		model.J = range(len(females))
		# model.revs = Param(model.I, model.J, initialize = utmat)
		model.x = Var(model.I, model.J, domain = Binary)
		model.y = Var(model.I, domain = Binary)
		model.z = Var(model.J, domain = Binary)
		def obj_expression(model):
			return sum(model.x[i,j]*utmat[i,j] for i in model.I for j in model.J) + sum(4000*model.y[i] for i in model.I)+sum(4000*model.z[j] for j in model.J)
		model.OBJ = Objective(rule = obj_expression, sense = maximize)
		def rowx_constraint_rule(model,i):
			return sum(model.x[j] for j in model.J) <= 5
		def colx_constraint_rule(model,j):
			return sum(model.x[i] for i in model.I) <= 1
		def capcons(model):
			return sum(model.y[i] for i in model.I) + sum(model.z[j] for j in model.J) <= 15
		def indycon(model, i):
			return sum(model.x[j] for j in model.J) < 500*(1-model.y)
		def indzcon(model, j):
			return sum(model.x[i] for i in model.I) < 500*(1-z)
		model.row = ConstraintList()
		for i in model.I:
			model.row.add(sum(model.x[i+1,j+1] for j in model.J)<=5)
		model.col = Constraint(model.J, rule = colx_constraint_rule)
		model.capcon = Constraint(model.I, model.J, rule = capcons)
		model.indycon = Constraint(model.I, rule = indycon)
		model.indzcon = Constraint(model.J, rule = indzcon)
		instance = model.create_instance()
		opt = SolverFactory('glpk')
		results = opt.solve(instance)

# Test snakes
snakes.append(Snake('a', sex = 'Male', age = 1, traits = [[recessives[0],recessives[0]],[codom[1]]]))
snakes.append(Snake('b', sex = 'Female', age = 2, traits = [[recessives[0]],[codom[2]]]))
snakes.append(Snake('d', sex = 'Female', age = 2, traits = [[recessives[0]],[codom[2]]]))

snakes.append(Snake('c', sex = 'Male' ,traits = [[recessives[1]],[codom[0],codom[0]]]))
transitive = list(snakes)


tick(snakes, transitive)



