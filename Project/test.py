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
data = list(csv.reader(open('newprices.csv')))
data = data[1:(len(data)-1)]
for i in range(0,len(data)):
	data[i][1] = float(data[i][1])
print data