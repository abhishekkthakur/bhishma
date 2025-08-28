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


## Loading the mesh skeleton
nc = netCDF4.Dataset('database_MoV.e')
var = nc.variables['vals_elem_var1eb1']
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


## Preparing plot
fig, ax = plt.subplots()
p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=1.0)


## Loading and reading the extracted image file
datafile = open('extractedFile.txt', 'r')
datalines = datafile.readlines()
colors = []
for i in datalines:
    a = i.strip('')
    b = a.split()	
    for j in b:
        colors.append(float(j))
datafile.close()

print (colors)
print (len(colors))
print (type(colors))

## Final plotting
p.set_array(np.array(colors))
ax.add_collection(p)
ax.set_xlim([0, 256])
ax.set_ylim([0, 256])
ax.set_aspect('equal')
plt.show()
