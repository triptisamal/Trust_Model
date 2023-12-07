import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

#fig = plt.figure(figsize=(4,4))

#ax = fig.add_subplot(111, projection='3d')

fig = plt.figure(figsize=(4,4))

ax = fig.add_subplot(111, projection='3d')

ax.scatter(0,0,0) # plot the point (2,3,4) on the figure
ax.scatter(0,3,0) # plot the point (2,3,4) on the figure
ax.scatter(0,2,0) # plot the point (2,3,4) on the figure

plt.show()

