import pandas as pd

# The read_csv is reading the csv file into Dataframe

df = pd.read_csv("./conf_trust_0-2.csv")

# then to_excel method converting the .csv file to .xlsx file.

df.to_excel("conf_trust_0-2.xlsx", index=False)



