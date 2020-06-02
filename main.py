import plotly.figure_factory as ff
import chart_studio.plotly as py
import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

scope = ['New York']
df  = pd.read_csv('https://sds-platform-private.s3-us-east-2.amazonaws.com/uploads/P48-Creating-Maps-Minority-Majority.csv')

#df name
df_new = df[df['STNAME'].isin(scope)]

#list values
values = df_new['TOT_POP'].tolist()
fips = df_new['FIPS'].tolist()

colorscale = ['#2daa4b', '#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b',
              '#2daa4b', '#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b',
              '#2daa4b', '#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b',
              '#2daa4b', '#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b',
              '#2daa4b', '#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b',
              '#2daa4b', '#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b',
              '#2daa4b', '#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b',
              '#2daa4b', '#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b',
              '#2daa4b', '#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b','#2daa4b',]

fig = ff.create_choropleth(
      fips = fips, values=values, scope = scope, colorscale = colorscale, round_legend_values = True,
      simplify_county = 0, simplify_state = 0,
      county_outline = {'color': 'rgb(15,15,55)', 'width': 0.5},
      state_outline = {'width': 0.5},
      legend_title = 'Population Per County',
      title = 'New York')


#fig.show()
pyo.plot(fig, filename = 'TEST.html')