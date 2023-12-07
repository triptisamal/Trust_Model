import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("confidence_plots-0.xlsx")
#df = df.dropna()
#print(df['t02'])

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Plot data
ax.plot(df['t10'], df['10'],marker='o',markersize=2)
#for xy in zip(df['t10'], df['10']):
#  plt.annotate('(%.4f, %.4f)' % xy, xy=xy,rotation=45)

#for xy in zip(df['trust02'],df['trust20']):
#  plt.annotate('(%f,%f)' % xy, xy=xy)
# Set labels
ax.set_xlabel('Time (s)', fontsize=19)
ax.set_ylabel('Confidence',fontsize=19)

# Set title
#ax.set_title('Refresh Period=15 s, Direct Verification Score = 20, Confidence Threshold = 5, Verifiability between a_i and a_j = 1',fontsize=18)
#fig.suptitle('Plots for Confidence held by a_j about position of a_i over 6 Refresh Periods.',fontsize=24)
#array=df['t02'].values.tolist()
#array1=df['02'].values.tolist()
#plt.xticks(array)
#plt.yticks([0.008,1, 2, 15,16,17,18,19,20])
plt.xlim([0,90])
plt.ylim([-1, 25])

# Show plot
plt.show()

