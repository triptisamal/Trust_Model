from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import sys

refresh_period = int(sys.argv[1])
number_of_refresh_period = int(sys.argv[2])

#convert csv to xlsx
df = pd.read_csv("./conf_trust_0-2.csv")
df.to_excel("conf_trust_0-2-org.xlsx", index=False)

##handling duplicates
#sort in decsending order according to confidence
df = df.sort_values(by='confidence', ascending=False)
#drop duplicates for column "time" 
df = df.drop_duplicates(subset='time', keep="first")
df = df.sort_values(by='time', ascending=True)

df.to_excel("conf_trust_0-2.xlsx", index=False)
plt.figure()          

df_time = pd.read_excel("conf_trust_0-2.xlsx", sheet_name='Sheet1', usecols="A")
df_confidence = pd.read_excel("conf_trust_0-2.xlsx", sheet_name='Sheet1', usecols="B")
df_trust_01 = pd.read_excel("conf_trust_0-2.xlsx", sheet_name='Sheet1', usecols="C")
df_trust_02 = pd.read_excel("conf_trust_0-2.xlsx", sheet_name='Sheet1', usecols="D")

conf_arr = df_confidence.stack().tolist()
trust_arr_01 = df_trust_01.stack().tolist()
trust_arr_02 = df_trust_02.stack().tolist()
time_arr = df_time.stack().tolist()


conf = []
trust_01 = []
trust_02 = []
time = []
#count number of rows until you get 2 refresh periods
rows = 0
i = 0

time_total = refresh_period*number_of_refresh_period

while i < len(time_arr):
    if time_arr[i] == time_total:
        break
    rows += 1
    i += 1

for i in range(rows):
    conf.append(conf_arr[i])
    trust_01.append(trust_arr_01[i])
    trust_02.append(trust_arr_02[i])
    time.append(time_arr[i])


#menMeans = (20, 35, 30, 35, 27)
#menStd = (2, 3, 4, 1, 2)

width = 0.2       # the width of the bars
N=len(conf)
ind = np.array(time)
plt.ylim(0.0, 1.3)
plt.bar(ind,trust_01, width, color='r', alpha=0.5,label='$T_{j}(k)$')
plt.bar(ind+width,trust_02, width, color='b', alpha=0.5, label='$T_{j}(i)$')

plt.ylabel('Trust',fontsize=25)      
#plt.ylabel('Trust $T_{i}(j)$')      
plt.xlabel('Time (s)',fontsize=25)      
plt.legend(fontsize="22")

x = time
y = conf

plt.xticks(np.arange(min(x), max(x), 1),rotation=45,fontsize=16)
plt.yticks(fontsize=16)


axes2 = plt.twinx()

axes2.plot(x, y, color='k', marker='o',markersize=4,label='$C_{j}(p_{it})$')
axes2.set_ylim(0, 23)
y_ticks=axes2.get_yticks()
axes2.set_yticklabels(y_ticks, fontsize=16)
axes2.set_ylabel('Confidence',fontsize=25)
axes2.legend(loc='upper left',fontsize="25")

#axes2.set_title('$a_{0}$ can directly verify $a_{1}$, but not $a_{2}$.Trust $T_{0}(1)$ is generated from physical verification of position of $a_{1}$ by $a_{0}$.Trust $T_{0}(2)$ is generated from agreement between $a_{1}$ and $a_{2}$.\n$R = 15 s$.$P_{v} = 20$',fontsize=15)
#plt.suptitle('Variation of Confidence without physical verification',fontsize=24)
plt.show()
