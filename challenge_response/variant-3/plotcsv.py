

import matplotlib.pyplot as plt 
import csv 
  
x = [] 
y = [] 
  
with open('conf.csv','r') as csvfile: 
    lines = csv.reader(csvfile, delimiter=',') 
    for row in lines: 
        x.append(row[3]) 
        y.append(row[2]) 
  
plt.plot(sorted(x), sorted(y), color = 'g', linestyle = 'dashed', 
         marker = 'o')#,label = "Confidence held by agent 2 about agent 1") 
  
plt.xticks(rotation = 25) 
plt.xlabel('Time(s)') 
plt.ylabel('Confidence') 
plt.title('Confidence held by agent 2 about agent 1', fontsize = 20) 
plt.grid() 
plt.legend() 
plt.show() 

