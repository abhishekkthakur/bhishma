## Importing necessary libraries
import netCDF4
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import matplotlib
import random
from csv import reader
from warnings import filterwarnings
filterwarnings(action='ignore', category=DeprecationWarning, message='`np.bool` is a deprecated alias')


## Loading and reading the csv file
time = []
alpha_ppt = []
beta_ppt = []
te = []
x_alpha = []
x_beta = []
with open('database_MoV.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    for b in csv_reader:
        time.append(float(b[0]))
        alpha_ppt.append(float(b[4]))
        beta_ppt.append(float(b[5]))
        te.append(float(b[7]))
        x_alpha.append(float(b[1]))
        x_beta.append(float(b[2]))

## Loading dataset
nc = netCDF4.Dataset('database_MoV.e')

## This is for color map
var = nc.variables['vals_elem_var1eb1']
print ('Total simulation timesteps: {}'.format(len(var)))    # This gives you total simulation timesteps
counter = 0
datafile = open('compiledMoV.txt', 'w')
while (counter < len(time)):
    datafile.write('\n')
    datafile.write(str(time[counter]) + '\t' + str(alpha_ppt[counter]) + '\t' + str(beta_ppt[counter]) + '\t' + str(te[counter]) + '\t' + str(x_alpha[counter]) + '\t' + str(x_beta[counter]) + '\t')
    for i in var[counter:counter+1]:
        for j in i:
            #print (counter)
            datafile.write(str(j) + '\t')
        #datafile.write('\n')
    print (counter)
    counter = counter + 25	## This integer represents the interval at which images has to be extracted from the *.e file.

datafile.close()



'''
## Extracting x, and y coordinates and combining them into polygon patches
X = nc.variables['coordx']
Y = nc.variables['coordy']
connect = nc.variables['connect1']
xy = np.array([X[:], Y[:]]).T
patches = []
counter = 0
for coords in xy[connect[:]-1]:
    quad = Polygon(coords, True)
    patches.append(quad)
    counter = counter + 1
print ('Total number of pixels: {}'.format(counter))

## Making plot
fig, ax = plt.subplots()
p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=1.0)

## trying with random colors
#randomColors = np.random.random_sample(size = 65536)
#randomColors = randomColors.tolist()
#print (randomColors)
#print (len(randomColors))
#print (type(randomColors))

## Trying with a rough datafile
#randomColors = []
#datafile = open('roughList.txt', 'r')
#datalines = datafile.readlines()
#for i in datalines:
#    a = i.strip()
#    b = a.split()
#    randomColors.append(float(b[0]))
#datafile.close()

p.set_array(np.array(colors))
ax.add_collection(p)
ax.set_xlim([0, 128])
ax.set_ylim([0, 128])
ax.set_aspect('equal')
plt.show()
'''
