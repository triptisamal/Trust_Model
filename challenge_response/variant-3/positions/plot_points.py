import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math 

def legend_without_duplicate_labels(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    ax.legend(*zip(*unique),title="Trust")


def read_file(pos_file):

    import ast

    f=open(pos_file,mode='r')
    lines =  f.read()
    f.close()
    return lines


#t = {'A':(0,1), 'B':(2,3), 'C':(4,5)}

#t=eval(read_file("pos_14.txt")) uncomment later
t=eval(read_file("pos_16.txt")) #comment later
#t=eval(read_file("pos_15.txt")) #comment later

# Import libraries
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
 
 
# Creating dataset
x=[]
y=[]
z=[]
x1=[]
y1=[]
z1=[]
agents=[]
for i in range(16):
    x.append(t[i][0])
    y.append(t[i][1])
    z.append(t[i][2])
    x1.append(t[i][0]+0.5)
    y1.append(t[i][1]+0.5)
    z1.append(t[i][2]+0.5)
    agents.append(i)

 
# Creating figure (only points, without circles of cmap
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
 
# Creating plot
ax.scatter3D(x[0], y[0], z[0],color = "black",s=40,label='$T_{0}(0)$ (self)')
plt.xlim(-1, 4)

##convert csv to xlsx
df = pd.read_csv("../large/conf_trust_0-8.csv")
df.to_excel("conf_trust_0-8.xlsx",index=False)
col = [ "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q"]
for i in range(0,15):
    tr = pd.read_excel("conf_trust_0-8.xlsx", sheet_name='Sheet1',skiprows=14,nrows=1,usecols=col[i]);
    tr_arr = tr.stack().tolist()

    if 0.7 <= tr_arr[0] <= 1:
        cr="blue"
        lbl='$T_{0}(i) \in [0.7,1]$'
    if 0.5 <= tr_arr[0] < 0.7:
        cr="purple"
        lbl='$T_{0}(i) \in [0.5,0.7)$'
    if 0.25 <= tr_arr[0] < 0.5:
        cr="red"
        lbl='$T_{0}(i) \in [0.5,0.7)$'
    if 0.125 <= tr_arr[0] < 0.5:
        cr="green"
        lbl='$T_{0}(i) \in [0.25,0.5)$'
    if tr_arr[0] < 0.125:
        cr="orange"
        lbl='$T_{0}(i) \in [0,0.125)$'
    
    scatter1 = ax.scatter3D(x[i+1], y[i+1], z[i+1],s=40,color = cr,label=lbl)

legend_without_duplicate_labels(ax)
#legend1 = ax.legend(['$T_{0}(0)$ (self)','$T_{0}(i) \in [0.7,1]$','$T_{0}(i) \in [0.5,0.7)$','$T_{0}(i) \in [0.25,0.5)$'], title="Trust")

for i,x, y, z in zip(agents,x, y, z):
    label = '$a_{%d}$:(%d, %d, %d)' % (i,x, y, z)
    ax.text(x, y, z, label,fontsize=12,ha='left', va='top')

#plt.title("Agent $a_0$'s Trust in other agents at a random instant")


 
# show plot
plt.show()
