from urllib.request import urlopen
import urllib
import json
import pandas as pd
import plotly.express as px
import re
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import date, timedelta, datetime
import dash_bootstrap_components as dbc
import sqlite3
from datetime import datetime as dt, date, timedelta
import time
import numpy as np
import plotly.graph_objs as go

class Covid:

    today=date.today()
    #today = date(2020,6,22)
    conn = sqlite3.connect('Covid.db')
    curs = conn.cursor()

    unixtoday=int(time.mktime(today.timetuple()))

    curs.execute('select date from corona order by date desc limit 1')
    dbtoday = curs.fetchall()
    datedifference = (unixtoday - dbtoday[0][0]) // 86400
    print(" DIFFERENCE:", datedifference)
    db_insert_date=dbtoday[0][0]
    # db_insert_human_date = date.fromtimestamp(db_insert_date)
    # print(db_insert_human_date)

    county = ['Albany', 'Allegany', 'Bronx', 'Broome', 'Cattaraugus', 'Cayuga', 'Chautauqua', 'Chemung', 'Chenango',
              'Clinton', 'Columbia', 'Cortland', 'Delaware', 'Dutchess', 'Erie', 'Essex', 'Franklin', 'Fulton',
              'Genesee',
              'Greene', 'Hamilton', 'Herkimer', 'Jefferson', 'Kings', 'Lewis', 'Livingston', 'Madison', 'Monroe',
              'Montgomery',
              'Nassau', 'New York', 'Niagara', 'Oneida', 'Onondaga', 'Ontario', 'Orange', 'Orleans', 'Oswego', 'Otsego',
              'Putnam', 'Queens', 'Rensselaer', 'Richmond', 'Rockland', 'Saratoga', 'Schenectady', 'Schoharie',
              'Schuyler',
              'Seneca', 'St. Lawrence', 'Steuben', 'Suffolk', 'Sullivan', 'Tioga', 'Tompkins', 'Ulster', 'Warren',
              'Washington',
              'Wayne', 'Westchester', 'Wyoming', 'Yates']

    county_value=['AY','ALY']
    dropdown_names=[dict(label=x, value=y) for x, y in zip(county, county)]
    print("dropdown: ",dropdown_names)
    while(db_insert_date <= unixtoday):
        db_insert_date += 86400
        db_insert_human_date = date.fromtimestamp(db_insert_date)
        website = "https://health.data.ny.gov/resource/xdss-u53e.json?test_date=" + str(db_insert_human_date) + "T00:00:00.000"
        with urllib.request.urlopen(website) as url:
            data6 = json.loads(url.read().decode())
            if len(data6)==62:
                county_new_positives = [int(county['new_positives']) for county in data6]
                cumulative_number_of_positives = [int(county['cumulative_number_of_positives']) for county in data6]
                total_number_of_tests = [int(county['total_number_of_tests']) for county in data6]
                cumulative_number_of_tests = [int(county['cumulative_number_of_tests']) for county in data6]
               # print(db_insert_date,db_insert_human_date)
                for i in range(62):
                    curs.execute(
                        "INSERT INTO CORONA(Date, County, Positives_Today, Cumulative_Positive, Tests_Performed_Today, Cumulative_Tests) VALUES(?,?,?,?,?,?)",
                        (db_insert_date, county[i], county_new_positives[i], cumulative_number_of_positives[i],
                         total_number_of_tests[i], cumulative_number_of_tests[i]))
                    conn.commit()

    curs.execute('select date from corona order by date desc limit 1')
    real_website_date = curs.fetchall()
    real_website_date_human=date.fromtimestamp(real_website_date[0][0])
    print("real website:",real_website_date_human)

    website_date = str(real_website_date_human).split('-')
    sample_date=['2020-03-02','2020-03-05','2020-03-07','2020-03-09']
    sample_vals=[10,20,3]
    df2=pd.read_excel(
    "https://github.com/chris1610/pbpython/blob/master/data/salesfunnel.xlsx?raw=True"
)
    pv = pd.pivot_table(df2, index=['Name'], columns=["Status"], values=['Quantity'], aggfunc=sum, fill_value=0)
    trace1 = go.Bar(x=pv.index, y=pv[('Quantity', 'declined')], name='Declined')
    #trace2 = go.Bar(x=sample_date, y=pv[('Quantity', 'pending')], name='Pending')
    trace2 = go.Bar(x=sample_date, y=sample_vals, name='Pending')
    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    # app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div([
        html.Div([
            html.H1("New York State Covid-19 Tracker")],
            className="row",
            style={'textAlign': "center", "padding-bottom": "30"}),
        html.Div([
            html.Div([
                dcc.Graph(
                    id="map",
                    style={'height': 670, 'width': 1050}
                )], className="eight columns"),
            html.Div([
                dcc.DatePickerSingle(
                    style={'height': 400,'width':800},
                    id='my-date-picker-single',
                    min_date_allowed=dt(2020, 3, 2),
                    max_date_allowed=dt(int(website_date[0]), int(website_date[1]),
                                        int(website_date[2])),
                    initial_visible_month=dt(int(website_date[0]), int(website_date[1]),
                                             int(website_date[2])),
                    date=date(int(website_date[0]), int(website_date[1]), int(website_date[2]))),

                dcc.Dropdown(
                    id="dropdown",
                    options=dropdown_names,
                    value='Albany',
                    placeholder="Select a County")
            ], className="three columns"),
            # html.Div([
            #     dcc.Dropdown(
            #         options=[
            #             {'label': 'New York City', 'value': 'NYC'},
            #             {'label': 'Montreal', 'value': 'MTL'},
            #             {'label': 'San Francisco', 'value': 'SF'}
            #         ],
            #         placeholder="Select a city",
            #         style={'height': 300}
            #     )
            # ], className="one column"),
        ], className="row"),
        html.Div([html.Div([
            dcc.Graph(
                id="histogram",
                    figure = {
                    'data': [trace1],
                    'layout':
                    go.Layout(title='Order Status by Customer', barmode='stack')}
            )
        ], className="six columns"),
        html.Div([
            dcc.Graph(
                id="histogram2",
                figure={
                    'data': [trace2],
                    'layout':
                        go.Layout(title='Order Status by Customer', barmode='stack')}
            )
        ], className="six columns")
        # date=str(dt(2020, 6, 10))
            ],className="Row"),
        html.Div([
            html.Div(id="test")
        ])
    ])

    @app.callback(
        Output(component_id='map', component_property='figure'),
        [Input(component_id='my-date-picker-single', component_property='date')])

    def update_map(date):
        print("date:",date)
        date_time_obj = datetime.strptime(date, '%Y-%m-%d')
        unixTime = int(time.mktime(date_time_obj.timetuple()))
        print("unix: ",unixTime)
        # unixTime = int(time.mktime(date.timetuple()))
        # print("unix time",unixTime)
        conn = sqlite3.connect('Covid.db')
        curs = conn.cursor()
        str_unixTime=str(unixTime)
        #query="select count(date) from corona where date = %s",(unixTime)
        t=unixTime,
        print("t:",t[0])
        time2 = t[0],
        curs.execute('SELECT COUNT(Date) FROM CORONA WHERE Date = ?',time2)
        count=curs.fetchall()
        print(count)
        with urllib.request.urlopen(
                "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json") as url:
            # print(url)
            data = json.loads(url.read().decode())
            data['features'] = [x for x in data['features'] if x['properties']['STATE'] == '36']

            county_fips = [x['properties']['GEO_ID'].split("US")[1] for x in data['features'] if
                           x['properties']['STATE'] == '36']

            county_fips=sorted(county_fips)

            county_names = [x['properties']['NAME'] for x in data['features'] if x['properties']['STATE'] == '36']
            county_names=sorted(county_names)
        if count[0][0]==62:
            curs.execute('SELECT Positives_Today FROM Corona where date = ?',time2)
            conp=curs.fetchall()

            curs.execute('SELECT Cumulative_Positive FROM Corona where date = ?',time2)
            cunp=curs.fetchall()

            curs.execute('SELECT Tests_Performed_Today FROM Corona where date = ?',time2)
            tnt=curs.fetchall()

            curs.execute('SELECT Cumulative_Tests FROM Corona where date = ?',time2)
            cnt=curs.fetchall()

            county_new_positives=[]
            cumulative_number_of_positives=[]
            total_number_of_tests=[]
            cumulative_number_of_tests=[]

            for i in range(62):
                county_new_positives.append(conp[i][0])
                cumulative_number_of_positives.append(cunp[i][0])
                total_number_of_tests.append(tnt[i][0])
                cumulative_number_of_tests.append(cnt[i][0])

            pre_df = {
                'fips': county_fips,
                'County New Positives': county_new_positives,
                'county_names': county_names,
                'Cumulative Positives': cumulative_number_of_positives,
                'Test Cases Today': total_number_of_tests,
                'Cumulative Tests': cumulative_number_of_tests
            }

            df = pd.DataFrame(pre_df)

            fig = px.choropleth_mapbox(df, geojson=data, locations='fips', color='County New Positives',
                                       color_continuous_scale="geyser",
                                       mapbox_style="carto-positron",  # carto-positron
                                       zoom=6.2, center={"lat": 42.940339, "lon": -76.428082},
                                       opacity=0.5,
                                       hover_name="county_names",
                                       hover_data={
                                           "County New Positives": True,
                                           'Cumulative Positives': True,
                                           'Test Cases Today': True,
                                           'Cumulative Tests': True,
                                           "fips": False,
                                       },

                                       labels={'County New Positives': 'County New Positives'}
                                       )

            # fig.update_layout(title=dict(font=dict(size=28), x=0.5, xanchor='center'),
            # margin=dict(l=60, r=60, t=50, b=50))

            fig.update_layout(dragmode=False, margin={"r": 0, "t": 0, "l": 0, "b": 0})

            return fig

    @app.callback(
        Output(component_id='test', component_property='children'),
        [Input(component_id='dropdown', component_property='value')])

    def update_histogram(options):
        print("options: ",options)
        name=options,
        print("name:",name)
        conn = sqlite3.connect('Covid.db')
        curs = conn.cursor()
        curs.execute('Select * from Corona where County=?',name)
        conp = curs.fetchall()
        print("query: ",conp)



    if __name__ == "__main__":
        app.run_server(debug=True)

