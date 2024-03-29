import plotly.express as px
import pandas as pd

df = pd.read_excel("conf_trust_0-2.xlsx", sheet_name='Sheet1', usecols="B,C,D")

fig = px.parallel_coordinates(df, color="confidence", labels={"trust": "Trust",
                "confidence": "Confidence", },
                             color_continuous_scale=px.colors.diverging.RdYlGn,
                             color_continuous_midpoint=2)

fig.update_layout(
    plot_bgcolor = 'white',
    paper_bgcolor = 'white',
    font = dict(size=19),
    yaxis_range=[0,20]
)
fig.show()
