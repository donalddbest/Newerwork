import csv
import pandas
import numpy
import matplotlib.pyplot as plt

file = pandas.read_csv('profitfile.csv', header = None)

optimum = file[0:19][0:4]
notoptimum = file[20:39][0:4]

x = [i for i in range(1,6)]
y = [numpy.mean(optimum[:][i]) for i in range(0,5)]
y2 = [numpy.mean(notoptimum[:][i]) for i in range(0,5)]

plt.plot(x,y)
plt.plot(x,y2)
plt.show()
