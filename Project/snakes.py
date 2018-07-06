from __future__ import division
import csv
import time
import numpy as np
import pandas
import math
from pyomo.environ import *
from collections import Counter
from collections import defaultdict

# Unneccesarily gets a list of names to give to snakes
df = pandas.read_csv('babies-first-names-1980-1989.csv')
names = df.FirstForename
names = np.unique(names)
names = names[2:len(names)]

# Brings the gene prices from the file called newprices.csv
data = list(csv.reader(open('newprices.csv')))
data = data[1:(len(data)-1)]
for i in range(0,len(data)):
	data[i][1] = float(data[i][1])
	# data[i][2] = float(data[i][2])

# Connects to the file that will hold the data on profits
profitfile = open('newprofitfile.csv', "a")

# This tells the program which rule it should use to keep snakes
breedingrule = 0

# Tells how many years will be simulated
numyearssimulated = 7

# The traits the program will work with
recessives = ['Pied']
codom = ['Pastel', 'Fire', 'Banana','Enchi','Mojave','GHI','YellowBelly']
dom = ['Pinstripe']


# np.random.seed(726366)
# Has the number for the name a snake will get
nameindex = 0 

# The holding capacity for snakes
capacity = 15

snakes = []

# The probability a pairing will result in a clutch
p = .6


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

		# Will keep track of the snakes related to the current one so there is no inbreeding
		self.forebears = [self.name]
		self.parents = []

		# Needed so a snake won't breed when it's too young
		self.age = age
		if (self.sex == 'Male'):
			self.price = 34.47
		else:
			self.price = 41.68
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
		for i in range(0,len(self.traits)):
			for j in range(0,len(data)):
				if self.traits[i][0] == data[j][0]:
					self.price = self.price + data[j][1]
				else:
					pass

def breed(snake1,snake2):
	"""Given two snakes, determines whether they can breed and if they can possibly generates a clutch and if it generates a clutch generates a variable number of babies."""
	global p
	yesno = np.random.binomial(size = 1, n = 1, p = p)[0]
	if (snake1.numTimesBreedable >= snake1.numTimesBred + 1 and snake2.numTimesBreedable >= snake2.numTimesBred + 1) and (snake1.age>=snake1.ageBreedable and snake2.age>=snake2.ageBreedable) and (snake1.sex != snake2.sex):
		if (yesno == 0):
			pass
		else:
			snake2.numTimesBred = snake2.numTimesBred + 1
			snake1.numTimesBred = snake1.numTimesBred + 1
			# Working on getting a better distribution for clutch sizes
			numbabies = np.floor(np.random.triangular(3,6,14, 1))
			for i in range(1,numbabies):
				global nameindex
				# Actually uses the Snake class to instantiate the clutch size determined
				transitive.append( Snake(names[nameindex], snake1,snake2))
				nameindex = nameindex + 1

def hypobreed(snake1, snake2):
	# Calculates the expected value of the offspring from a given pairing
	exprev = 0
	traitlist = []
	# Checks whether the snakes would inbreed and if so we don't want to breed them
	if (not set(snake1.forebears).isdisjoint(snake2.forebears)):
		return 0
	# Checks whether parents are same sex
	elif (snake1.sex == snake2.sex):
		return 0
	# Calculates the expected revenue
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
		if(snake2.age >= 1):
			exprev = exprev + 1
	return exprev + 38

def hypobreedg(snake1,snake2):
	# Checks whether the snakes would inbreed and if so we don't want to breed them
	weightvec = ['Pinstripe','Spider','YellowBelly','Pastel','Enchi','Mojave','Fire','Banana','GHI','Pied']
	if (not set(snake1.forebears).isdisjoint(snake2.forebears)):
		return 0
	# Checks whether parents are same sex
	elif (snake1.sex == snake2.sex):
		return 0
	else:
		mtraits = []
		ftraits = []
		for i in range(0,len(snake1.traits)):
			mtraits = mtraits + snake1.traits[i]
		for i in range(0,len(snake2.traits)):
			ftraits = ftraits + snake2.traits[i]
		traitlist = mtraits + ftraits
		mdict = Counter(mtraits)
		fdict = Counter(ftraits)
		for key in mdict:
			if(mdict[key] == 2):
				mdict[key] = .5
			else:
				mdict[key] = .375
		for key in fdict:
			if(fdict[key] == 2):
				fdict[key] = .5
			else:
				fdict[key] = .33
		newdict = mdict+fdict
		for key in newdict:
			for i in range(0,len(weightvec)):
				if(key == weightvec[i]):
					newdict[key] = newdict[key]*(len(weightvec)+i)/len(weightvec)
		return sum(newdict.itervalues())

				
def tick(transitive):
	"""This function will simulate a year, so will age every snake 1 year and will use different breeding rules to decide which snakes to breed and decide which snakes to keep and sell down to capacity. Really does most of the work."""
	global snakes
	for i in range(0, len(snakes)):
		snakes[i].age = snakes[i].age + 1
		snakes[i].numTimesBred = 0
	if(breedingrule < 2):
		males = [snake for snake in snakes if snake.sex == 'Male']
		females = [snake for snake in snakes if snake.sex == 'Female']
		utmat = []
		vars = []
		for i in range(0, len(males)):
			# Makes a 2d array of expected revenue from pairings
			utmat.append([])
			for j in range(0, len(females)):
				try:
					utmat[i].append(hypobreed(males[i],females[j]))
				except:
					pass
		utmat = dict(((i+1,j+1), utmat[i][j]) for i in range(len(utmat)) for j in range(len(utmat[0])))

		# Makes and solves the integer program with pyomo
		modelr = ConcreteModel()
		modelr.I = range(len(males))
		modelr.J = range(len(females))
		modelr.x = Var(modelr.I, modelr.J, domain = Binary)
		
		def obj_expression(modelr):
			return 6*sum(sum(modelr.x[i,j]*utmat[i+1,j+1] for j in modelr.J) for i in modelr.I)
		modelr.OBJ = Objective(rule = obj_expression, sense = maximize)
		# def capcons(model):
		# 	return sum(model.y[i] for i in model.I) + sum(model.z[j] for j in model.J) <= capacity
		modelr.row = ConstraintList()
		for i in modelr.I:
			modelr.row.add(sum(modelr.x[i,j] for j in modelr.J)<=5)
		modelr.col = ConstraintList()
		for j in modelr.J:
			modelr.row.add(sum(modelr.x[i,j] for i in modelr.I)<=1)
		# model.capcon = Constraint(model.I, model.J, rule = capcons)
		# model.indycon = ConstraintList()
		# for i in model.I:
		# 	model.indycon.add(sum(model.x[i,j] for j in model.J)<= 500*model.y[i])
		# model.indzcon = ConstraintList()
		# for j in model.J:
		# 	model.indzcon.add(sum(model.x[i,j] for i in model.I)<= 500*model.z[j])
		opt = SolverFactory('cbc')
		opt.options['threads'] = 16
		results = opt.solve(modelr)
		for i in modelr.I:
			for j in modelr.J:
				if(modelr.x[i,j].value == 1):
					breed(males[i],females[j])

	if breedingrule == 2:
		# This breeding rule breeds and keeps snakes to maximize the number of weighted genes in snakes.
		gmales = [snake for snake in snakes if snake.sex == 'Male']
		gfemales = [snake for snake in snakes if snake.sex == 'Female']
		utmat = []
		vars = []
		for i in range(0, len(gmales)):
			# Makes a 2d array of weighted number of genes from pairings
			utmat.append([])
			for j in range(0, len(gfemales)):
				# try:
				utmat[i].append(hypobreedg(gmales[i],gfemales[j]))
				# except:
				# 	pass
		utmat = dict(((i+1,j+1), utmat[i][j]) for i in range(len(utmat)) for j in range(len(utmat[0])))
		modelg = ConcreteModel()
		modelg.I = range(len(gmales))
		modelg.J = range(len(gfemales))
		modelg.x = Var(modelg.I, modelg.J, domain = Binary)
		
		def obj_expressiong(modelg):
			return sum(sum(modelg.x[i,j]*utmat[i+1,j+1] for j in modelg.J) for i in modelg.I)
		modelg.OBJ = Objective(rule = obj_expressiong, sense = maximize)
		
		modelg.row = ConstraintList()
		for i in modelg.I:
			modelg.row.add(sum(modelg.x[i,j] for j in modelg.J)<=5)
		modelg.col = ConstraintList()
		for j in modelg.J:
			modelg.row.add(sum(modelg.x[i,j] for i in modelg.I)<=1)
		
		opt = SolverFactory('cbc')
		opt.options['threads'] = 16
		resultsg = opt.solve(modelg)
		for i in modelg.I:
			for j in modelg.J:
				if(modelg.x[i,j].value == 1):
					breed(gmales[i],gfemales[j])

		newmales = [snake for snake in transitive if snake.sex == 'Male']
		newfemales = [snake for snake in transitive if snake.sex == 'Female']
		utmat = []
		vars = []
		for i in range(0, len(newmales)):
			# Makes a 2d array of expected revenue from pairings
			utmat.append([])
			for j in range(0, len(newfemales)):
				try:
					utmat[i].append(hypobreedg(newmales[i],newfemales[j]))
				except:
					pass
		utmat = dict(((i+1,j+1), utmat[i][j]) for i in range(len(utmat)) for j in range(len(utmat[0])))
		modeln = ConcreteModel()
		modeln.I = range(len(newmales))
		modeln.J = range(len(newfemales))
		modeln.x = Var(modeln.I, modeln.J, domain = Binary)
		modeln.y = Var(modeln.I, domain = Binary)
		modeln.z = Var(modeln.J, domain = Binary)
		def obj_expressionn(modeln):
			return sum(sum(modeln.x[i,j]*utmat[i+1,j+1] for j in modeln.J) for i in modeln.I)
		modeln.OBJ = Objective(rule = obj_expressionn, sense = maximize)
		def capconsn(modeln):
			return sum(modeln.y[i] for i in modeln.I) + sum(modeln.z[j] for j in modeln.J) <= capacity
		modeln.row = ConstraintList()
		for i in modeln.I:
			modeln.row.add(sum(modeln.x[i,j] for j in modeln.J)<=5)
		modeln.col = ConstraintList()
		for j in modeln.J:
			modeln.row.add(sum(modeln.x[i,j] for i in modeln.I)<=1)
		modeln.capcon = Constraint(modeln.I, modeln.J, rule = capconsn)
		modeln.indycon = ConstraintList()
		for i in modeln.I:
			modeln.indycon.add(sum(modeln.x[i,j] for j in modeln.J)<= 500*modeln.y[i])
		modeln.indzcon = ConstraintList()
		for j in modeln.J:
			modeln.indzcon.add(sum(modeln.x[i,j] for i in modeln.I)<= 500*modeln.z[j])
		opt = SolverFactory('cbc')
		opt.options['threads'] = 16
		resultsn = opt.solve(modeln)
		keptindexm = [i for i in modeln.I if modeln.y[i].value == 1]
		keptindexf = [j for j in modeln.J if modeln.z[j].value == 1]
		keptm = [newmales[item] for item in keptindexm]
		keptf = [newfemales[item] for item in keptindexf]
		sellindexm = [i for i in modeln.I if modeln.y[i].value == 0]
		sellindexf = [j for j in modeln.J if modeln.z[j].value == 0]
		sellm = [newmales[item] for item in sellindexm]
		rev = 0
		for i in range(0,len(sellm)):
			rev = rev + sellm[i].price
		sellf = [newfemales[item] for item in sellindexf]
		for i in range(0,len(sellf)):
			rev = rev + sellf[i].price
		snakes = keptm + keptf
		return rev - 80*len(snakes)
		
		

	# if breedingrule == 1:
	# 	# This breeding rule chooses arbitrary snakes to keep and sells off the rest.
		
	# 	if capacity>= len(transitive):
	# 		snakes = list(transitive)
	# 		return -80*len(snakes)
	# 	else:
	# 		rand = np.random.randint(0,len(transitive), size = capacity)
	# 		snakes = [transitive[index] for index in rand]
	# 		sellsnakes = [transitive[index] for index in range(0,len(transitive)) if index not in rand]
	# 		rev = 0
	# 		for i in range(0, len(sellsnakes)):
	# 			rev = rev + sellsnakes[i].price
	# 		return rev - 80*len(snakes)
	males = [snake for snake in transitive if snake.sex == 'Male']
	females = [snake for snake in transitive if snake.sex == 'Female']
	if breedingrule == 0:
		# This breeding rule does the 'Optimal' way to choose which snakes to keep
		
		utmat = []
		vars = []
		for i in range(0, len(males)):
			# Makes a 2d array of expected revenue from pairings
			utmat.append([])
			for j in range(0, len(females)):
				try:
					utmat[i].append(hypobreed(males[i],females[j]))
				except:
					pass
		utmat = dict(((i+1,j+1), utmat[i][j]) for i in range(len(utmat)) for j in range(len(utmat[0])))

		# Makes and solves the integer program with pyomo
		model = ConcreteModel()
		model.I = range(len(males))
		model.J = range(len(females))
		model.x = Var(model.I, model.J, domain = Binary)
		model.y = Var(model.I, domain = Binary)
		model.z = Var(model.J, domain = Binary)
		def obj_expression(model):
			return 6*sum(sum(model.x[i,j]*utmat[i+1,j+1] for j in model.J) for i in model.I) + sum(-80*model.y[i] for i in model.I)+sum(-80*model.z[j] for j in model.J)
		model.OBJ = Objective(rule = obj_expression, sense = maximize)
		def capcons(model):
			return sum(model.y[i] for i in model.I) + sum(model.z[j] for j in model.J) <= capacity
		model.row = ConstraintList()
		for i in model.I:
			model.row.add(sum(model.x[i,j] for j in model.J)<=5)
		model.col = ConstraintList()
		for j in model.J:
			model.row.add(sum(model.x[i,j] for i in model.I)<=1)
		model.capcon = Constraint(model.I, model.J, rule = capcons)
		model.indycon = ConstraintList()
		for i in model.I:
			model.indycon.add(sum(model.x[i,j] for j in model.J)<= 500*model.y[i])
		model.indzcon = ConstraintList()
		for j in model.J:
			model.indzcon.add(sum(model.x[i,j] for i in model.I)<= 500*model.z[j])
		opt = SolverFactory('cbc')
		opt.options['threads'] = 16
		results = opt.solve(model)
		
		# Uses the results of the integer program to actually keep and sell the recomended snakes
		keptindexm = [i for i in model.I if model.y[i].value == 1]
		keptindexf = [j for j in model.J if model.z[j].value == 1]
		keptm = [males[item] for item in keptindexm]
		keptf = [females[item] for item in keptindexf]
		sellindexm = [i for i in model.I if model.y[i].value == 0]
		sellindexf = [j for j in model.J if model.z[j].value == 0]
		sellm = [males[item] for item in sellindexm]
		rev = 0
		for i in range(0,len(sellm)):
			rev = rev + sellm[i].price
		sellf = [females[item] for item in sellindexf]
		for i in range(0,len(sellf)):
			rev = rev + sellf[i].price
		snakes = keptm + keptf
		return rev - 80*len(snakes)


def initsnakes():
	"""This function initializes the original set of snakes"""
	global snakes
	global transitive
	snakes = []
	snakes.append(Snake('a', sex = 'Male', age = 1, traits = [[recessives[0],recessives[0]],[codom[1]]]))
	snakes.append(Snake('b', sex = 'Female', age = 2, traits = [[recessives[0]],[codom[2]]]))
	snakes.append(Snake('d', sex = 'Female', age = 2, traits = [[recessives[0]],[codom[2]]]))
	snakes.append(Snake('e', sex = 'Male', age = 1, traits = [[recessives[0],recessives[0]],[codom[1]]]))
	snakes.append(Snake('f', sex = 'Female', age = 2, traits = [[recessives[0]],[codom[2]]]))
	snakes.append(Snake('g', sex = 'Female', age = 2, traits = [[recessives[0]],[codom[1]]]))
	snakes.append(Snake('h', sex = 'Female', age = 2, traits = [[recessives[0]],[codom[0]]]))
	snakes.append(Snake('i', sex = 'Female', age = 2, traits = [[recessives[0]],[codom[1]]]))
	snakes.append(Snake('j', sex = 'Female', age = 2, traits = [[dom[0]],[codom[1]]]))
	snakes.append(Snake('k', sex = 'Female', age = 2, traits = [[dom[0],dom[0]],[codom[0]],[codom[2]]]))
	snakes.append(Snake('l', sex = 'Female', age = 2, traits = [[codom[3]],[codom[3]],[codom[2]]]))
	snakes.append(Snake('m', sex = 'Female', age = 2, traits = [[codom[4]],[codom[5],codom[5]],[codom[2]]]))
	snakes.append(Snake('n', sex = 'Female', age = 2, traits = [[codom[5],codom[5]]]))
	snakes.append(Snake('o', sex = 'Female', age = 2, traits = [[codom[6],codom[6]]]))
	snakes.append(Snake('c', sex = 'Male' ,age = 1, traits = [[codom[5]],[codom[0],codom[0]]]))
	transitive = list(snakes)


# The following simulates the system and puts the results in profitfile
for j in range(0,30):
	nameindex = 0
	breedingrule = 2
	initsnakes()
	profit = []
	for i in range(0,numyearssimulated):
		profit.append(tick(transitive))
		transitive = list(snakes)
	for item in profit:
		profitfile.write("%s, " % item)
	profitfile.write('%s,' % breedingrule)
	profitfile.write('%s\n' % p)
	print '0'
	nameindex = 0
	# breedingrule = 1
	# initsnakes()
	# profit = []
	# for i in range(0,numyearssimulated):
	# 	profit.append(tick(transitive))
	# 	transitive = list(snakes)
	# for item in profit:
	# 	profitfile.write("%s, " % item)
	# profitfile.write('%s,' % breedingrule)
	# profitfile.write('%s\n' % p)
	# nameindex = 0
	breedingrule = 0
	initsnakes()
	profit = []
	for i in range(0,numyearssimulated):
		profit.append(tick(transitive))
		transitive = list(snakes)
	for item in profit:
		profitfile.write("%s, " % item)
	profitfile.write('%s,' % breedingrule)
	profitfile.write('%s\n' % p)
	print j



