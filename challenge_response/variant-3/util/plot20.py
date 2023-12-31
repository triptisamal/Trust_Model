import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("confidence_plots-2.xlsx")
#df = df.dropna()
print(df['t20'])

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Plot data
ax.plot(df['t20'], df['20'],marker='o',markersize=2)
for xy in zip(df['t20'], df['20']):
  plt.annotate('(%.4f, %.4f)' % xy, xy=xy,rotation=45)
# Set labels
ax.set_xlabel('Time (s)')
ax.set_ylabel('Confidence')

# Set title
ax.set_title('Refresh period=15 s. Data point is shown for each time agent 0 reads the confidence in its database')
fig.suptitle('Plots for confidence held by agent 2 about position of agent 0 over 2 refresh periods.')
#array=df['t02'].values.tolist()
#array1=df['02'].values.tolist()
#plt.xticks(array)
#plt.yticks([0.008,1, 2, 15,16,17,18,19,20])
plt.xlim([0,31])
plt.ylim([-1, 25])

# Show plot
plt.show()

