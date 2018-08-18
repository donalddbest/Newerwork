import numpy as np

file = open('../Data/snakedat.txt', 'r')
outfile = open('../Data/outfile.csv', 'a')

# Reads in the data
data = file.readlines()
file.close()

listoftypes = []
newdat = []
# Makes the headers for the eventual output file.
for line in data:
	words = line.split(',')
	newdat.append(words)
	words = words[1:(len(words)-1)]
	listoftypes = listoftypes + words
listoftypes = list(set(listoftypes)) + ['Sex', 'Price']

# Initializes all of the entries to zero.
lines = np.zeros((193,len(listoftypes)))

# Replaces untrue zeroes with 1s.
for i in range(0,len(newdat)):
	for j in range(0,len(listoftypes)):
		for k in range(0,len(newdat[i])):
			if newdat[i][k] == listoftypes[j]:
				lines[i][j] = 1
	if newdat[i][0] == 'Male':
		lines[i][len(listoftypes)-2] = 1
	lines[i][len(listoftypes) - 1] = int(newdat[i][len(newdat[i])-1].rstrip())
for i in range(0, len(listoftypes) -1):
	outfile.write('%s,' % listoftypes[i])

# Writes output to file.
outfile.write('%s \n' % listoftypes[len(listoftypes)-1])
np.savetxt(outfile,lines, delimiter = ',')

outfile.close()