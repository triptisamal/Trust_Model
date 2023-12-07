import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("trust_02.xlsx")
#df = df.dropna()
#print(df['t02'])

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Plot data
ax.plot(df['time'], df['trust'],marker='o',markersize=2)
#for xy in zip(df['time'], df['trust']):
#  plt.annotate('(%.4f, %.4f)' % xy, xy=xy,rotation=45)
# Set labels
ax.set_xlabel('Time (s)')
ax.set_ylabel('Trust')

# Set title
#ax.set_title('Refresh period=15 s. Data point is shown for each time agent 0 reads/writes the confidence in its database')
#fig.suptitle('Plots for trust held by agent 0 for agent 2 over 2 refresh periods.')
#array=df['t02'].values.tolist()
#array1=df['02'].values.tolist()
#plt.xticks(array)
#plt.yticks([0.008,1, 2, 15,16,17,18,19,20])
plt.xlim([0,150])
plt.ylim([0, 1])

# Show plot
plt.show()

