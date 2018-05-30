import csv
import time
import numpy as np
import pandas
import math

df = pandas.read_csv('babies-first-names-1980-1989.csv')
names = df.FirstForename
names = np.unique(names)
names = names[2:len(names)]
data = list(csv.reader(open('prices.txt')))
for i in range(0,len(data)):
	data[i][1] = float(data[i][1])
	# data[i][2] = float(data[i][2])

recessives = ['Albino','Clown','Axanthic']
codom = ['Pastel', 'Fire', 'Banana']

# np.random.seed(726366)
curtime = time.time() 
capacity = 20
snakes = []
transitive = []
def prediction(age, traits, sex, time):
	"""Not yet implemented, will take those three/four arguments and return the price of the a snake with the given features."""
	print 'prediction is working thus far (for what it is worth)'

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
				transitive.append( Snake(names[i], snake1,snake2))

def tick(snakes, transitive):
	"""This function will simulate a year, so will age every snake 1 year and will call breed on the most valuable snakes and decide which snakes to keep and sell down to capacity."""
	for i in range(0, len(snakes)):
		snakes[i].age = snakes[i].age + 1
	for i in range(0,len(snakes)):
		for j in range(0,len(snakes)):
			try:
				breed(snakes[i],snakes[j])
			except:
				pass
	# The next two lines filter males and females so the optimal male to female ratio can be used.
	males = [snake for snake in transitive if snake.sex == 'Male']
	females = [snake for snake in transitive if snake.sex == 'Female']

	sorted(transitive, key = lambda snake: snake.price, reverse = True)
	# if len(transitive)>capacity:
	# 	for i in range(0, len(transitive)-capacity):
	# 		print('Need to sell %s' % transitive[capacity+i].name)

# Test snakes
snakes.append(Snake('a', sex = 'Male', age = 1, traits = [[recessives[0],recessives[0]],[codom[1]]]))
snakes.append(Snake('b', sex = 'Female', age = 2, traits = [[recessives[0]],[codom[2]]]))
snakes.append(Snake('d', sex = 'Female', age = 2, traits = [[recessives[0]],[codom[2]]]))

snakes.append(Snake('c', parent1 = snakes[0], parent2 = snakes[1]))


try:
	tick(snakes, transitive)
except:
	pass


