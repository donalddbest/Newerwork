import numpy as np

file = open('snakedat.txt', 'r')
outfile = open('outfile.csv', 'a')

data = file.readlines()
file.close()

listoftypes = []
newdat = []
for line in data:
	words = line.split(',')
	newdat.append(words)
	words = words[1:(len(words)-1)]
	listoftypes = listoftypes + words
listoftypes = list(set(listoftypes)) + ['Sex', 'Price']
lines = np.zeros((193,len(listoftypes)))

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
outfile.write('%s \n' % listoftypes[len(listoftypes)-1])
np.savetxt(outfile,lines, delimiter = ',')

outfile.close()