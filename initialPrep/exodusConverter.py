## Importing necessary libraries
import netCDF4
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import matplotlib
from warnings import filterwarnings
filterwarnings(action='ignore', category=DeprecationWarning, message='`np.bool` is a deprecated alias')


## Loading dataset
#nc = netCDF4.Dataset('newmov_T600K_out.e-s404')
nc = netCDF4.Dataset('database_MoV.e')
#print (nc.variables)



## This is for color map
var = nc.variables['vals_elem_var1eb1']
#var = nc.variables['node_num_map']
print ('Total simulation timesteps: {}'.format(len(var)))    # This gives you total simulation timesteps
colors = []
counter = 0
for i in var[10000:10001]:
    for j in i:
        counter = counter + 1
        colors.append(j)
#print (counter)
#print (type(colors))

## Extracting x, and y coordinates and combining them into polygon patches
X = nc.variables['coordx']
#print (X)
Y = nc.variables['coordy']
#print (Y)
connect = nc.variables['connect1']
#print (connect[0:8])
xy = np.array([X[:], Y[:]]).T
#print (xy.shape)
patches = []
counter = 0
for coords in xy[connect[:]-1]:
    quad = Polygon(coords, True)
    patches.append(quad)
    counter = counter + 1
print ('Total number of pixels: {}'.format(counter))

print (colors)
print (len(colors))
print (type(colors))
    
## Making plot
fig, ax = plt.subplots()
p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=1.0)
p.set_array(np.array(colors))
ax.add_collection(p)
ax.set_xlim([0, 256])
ax.set_ylim([0, 256])
ax.set_aspect('equal')
plt.show()
