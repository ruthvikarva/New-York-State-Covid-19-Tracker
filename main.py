from urllib.request import urlopen
import urllib
import json
import pandas as pd
import plotly.express as px

with urllib.request.urlopen("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json") as url:
    data = json.loads(url.read().decode())
    data['features'] = [x for x in data['features'] if x['properties']['STATE'] == '36']
    county_fips = [x['properties']['GEO_ID'].split("US")[1] for x in data['features'] if x['properties']['STATE'] == '36']
    county_names = [x['properties']['NAME'] for x in data['features'] if x['properties']['STATE'] == '36']

    with urllib.request.urlopen("https://health.data.ny.gov/resource/xdss-u53e.json") as url1:
        data1 = json.loads(url1.read().decode())


        county_new_positives = [int(county['new_positives']) for county in data1 if county['test_date'] == '2020-06-02T00:00:00.000']

        pre_df = {'fips': county_fips, 'County New Positives': county_new_positives, 'county_names': county_names}
        df = pd.DataFrame(pre_df)

        fig = px.choropleth_mapbox(df, geojson=data, locations='fips', color='County New Positives',
                                color_continuous_scale="Viridis",
                                range_color=(0, 200),
                                mapbox_style="carto-positron",
                                zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                                opacity=0.5,
                                hover_name="county_names",
                                hover_data={"County New Positives" : True, "fips" : False},

                                labels={'County New Positives':'County New Positives'}
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()
