import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("conf_trust_0-1.xlsx")
#df = df.dropna()
#print(df['t20'])

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Plot data

ax.plot(df['time'], df['confidence'],marker='o',color='green',markersize=2, label='First Position')
ax.plot(df['time1'], df['confidence1'],marker='o',color='blue',markersize=2, label='Second Position')



# Set labels
ax.set_xlabel('Time (s)',fontsize=25)
ax.set_ylabel('Confidence',fontsize=25)

# Set title
#ax.set_title('Refresh period=15 s. Data point is shown for each time agent 0 reads the confidence in its database')
#fig.suptitle('Plots for confidence held by agent 2 about position of agent 1 over 10 Refresh Periods')
#array=df['t02'].values.tolist()
#array1=df['02'].values.tolist()
#plt.xticks(array)
#plt.yticks([0.008,1, 2, 15,16,17,18,19,20])
plt.xlim([0,300])
plt.ylim([-1, 25])

plt.yticks(fontsize=16)
plt.xticks(fontsize=16)
ax.legend(fontsize="22")
# Show plot
plt.show()

