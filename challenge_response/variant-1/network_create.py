import networkx as nx
from networkx import grid_graph
import globalvars
import plotly.graph_objects as go
import random
from random import randint
import matplotlib.pyplot as plt
from itertools import combinations
from mpl_toolkits.mplot3d import Axes3D
import pylab
import numpy as np



def generate_random_3Dgraph(n_nodes, radius, seed=None):

    if seed is not None:
        random.seed(seed)
   
    node_loc = [{'x':0, 'y':0, 'z':0} for i in range(0,globalvars.number_of_nodes+1)]

    #wireless range: infinite
    #4 units of distance is 100 feet

    
   
    if globalvars.topology == 0: #Perfect Lattice
        n = 0
        side = int((globalvars.number_of_nodes+1)**(1.0/3))
        print(side)
        while n < globalvars.number_of_nodes:
           # for i in range(1,side+1):
           #     for j in range(1,side+1):
           #         for k in range(1,side+1):
           #             print(i,j,k)
           #             node_loc[n]['x'] = i
           #             node_loc[n]['y'] = j
           #             node_loc[n]['z'] = k
           node_loc[n]['x'] = randint(1,globalvars.number_of_nodes);
           node_loc[n]['y'] = randint(1,globalvars.number_of_nodes);
           node_loc[n]['z'] = randint(1,globalvars.number_of_nodes);
           n += 1


    # Generate a dict of positions
    position = {i: (node_loc[i]['x'], node_loc[i]['y'], node_loc[i]['z']) for i in range(n_nodes)}
    
    # Create random 3D network
    globalvars.G = nx.random_geometric_graph(n_nodes, radius, pos=position)
    
    
    globalvars.pos = nx.get_node_attributes(globalvars.G, 'pos')

    for u, v in combinations(globalvars.G, 2):
        globalvars.G.add_edge(u, v)
    
    print("NUMBER OF NODES = ",len(globalvars.G.nodes))

    return globalvars.G



def network_plot_3D(G, angle, save=False):

    # Get node positions
    globalvars.pos = nx.get_node_attributes(G, 'pos')
    # Get number of nodes
    n = G.number_of_nodes()
    # Get the maximum number of edges adjacent to a single node
    #edge_max = max([G.degree(i) for i in range(n)])

    # Define color range proportional to number of edges adjacent to a single node
 #   colors = [plt.cm.plasma(G.degree(i)/edge_max) for i in range(n)] 

    # 3D network plot
    with plt.style.context(('ggplot')):
        
        fig = plt.figure(figsize=(10,7))
        ax = Axes3D(fig)
        
        # Loop on the pos dictionary to extract the x,y,z coordinates of each node
        for key, value in globalvars.pos.items():
            xi = value[0]
            yi = value[1]
            zi = value[2]
            
            # Scatter plot
            ax.scatter(xi, yi, zi, s=20+20*G.degree(key), edgecolors='k', alpha=0.7)
            #ax.scatter(xi, yi, zi, c=colors[key], s=20+20*G.degree(key), edgecolors='k', alpha=0.7)
        
        # Loop on the list of edges to get the x,y,z, coordinates of the connected nodes
        # Those two points are the extrema of the line to be plotted
        for i,j in enumerate(G.edges()):

            x = np.array((globalvars.pos[j[0]][0], globalvars.pos[j[1]][0]))
            y = np.array((globalvars.pos[j[0]][1], globalvars.pos[j[1]][1]))
            z = np.array((globalvars.pos[j[0]][2], globalvars.pos[j[1]][2]))
        
        # Plot the connecting lines
            ax.plot(x, y, z, c='black', alpha=0.5)
    
    # Set the initial view
    ax.view_init(30, angle)

    # Hide the axes
    ax.set_axis_off()

    #plt.show()
    
    return



def create_sim_map():
    '''Map of the network with information about which flashlights are on or off'''
        
    #define data structure for the map maintained by the simulator
    globalvars.sim_map = [{'agent_id':i, 'position':(0,0,0), 'flash_light':0} for i in range(globalvars.number_of_nodes)]

    #create network
    
    n = globalvars.number_of_nodes  
    G = generate_random_3Dgraph(n_nodes=n, radius=0.25, seed=1)
    
    #plotting
   # network_plot_3D(G,0, save=False)

    x_nodes = [globalvars.pos[key][0] for key in globalvars.pos.keys()]
    y_nodes = [globalvars.pos[key][1] for key in globalvars.pos.keys()]
    z_nodes = [globalvars.pos[key][2] for key in globalvars.pos.keys()]

    for i in range(globalvars.number_of_nodes):
      #  globalvars.sim_map[i]['agent_id'] = i
        globalvars.sim_map[i]['position'] = (x_nodes[i],y_nodes[i],z_nodes[i])
      #  globalvars.sim_map[i]['flashlight'] = 0
    print("This is the current map:",globalvars.sim_map)



