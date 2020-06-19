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

class covid:
    #external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
    #app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    # def __init__(self):
    #     today = date.today()
    #     website_date = today.strftime("%Y-%m-%d")
    #     print("Today:" ,website_date)

    today = date.today()
    yesterday = today - timedelta(days=16)
    website_date = today.strftime("%Y-%m-%d")
    yesterday_date = yesterday.strftime("%Y-%m-%d")
    #print("Today:" ,website_date,type(website_date))
    #print("Yesterday:", yesterday_date)


    website="https://health.data.ny.gov/resource/xdss-u53e.json?test_date=" + website_date + "T00:00:00.000"
    with urllib.request.urlopen(website) as url5:
       data5 = json.loads(url5.read().decode())
       date_counter = 0

       if not data5:
            #print('Website is NO DATA, so lets check previous dates')

            while len(data5) == 0:
                date_counter += 1
                website_date = today - timedelta(days = date_counter)

                website="https://health.data.ny.gov/resource/xdss-u53e.json?test_date=" + str(website_date) + "T00:00:00.000"
                with urllib.request.urlopen(website) as url5:
                    data5 = json.loads(url5.read().decode())

            #print("Latest Date:", website_date)

    real_website_date = str(website_date).split('-')
    # print(real_website_date)
    startingday = date(2020, 5, 16)
    print("startingday", startingday)
    enday = startingday + timedelta(days=20)
    print("endday",enday)


    #app=dash.Dash()
    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    #app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div([
        html.Div([
            html.H1("New York State Covid-19 Tracker")],
             className = "row",
            style={'textAlign': "center", "padding-bottom": "30"}),
    html.Div([
        html.Div([
            dcc.Graph(
                id="map",
                style={'height': 670,'width':1050}
            )], className="nine columns"),
        html.Div([
            dcc.DatePickerSingle(
                id='my-date-picker-single',
                min_date_allowed=dt(2020, 3, 2),
                max_date_allowed=dt(int(real_website_date[0]), int(real_website_date[1]), int(real_website_date[2])),
                initial_visible_month=dt(int(real_website_date[0]), int(real_website_date[1]), int(real_website_date[2])),
                date=str(dt(int(real_website_date[0]), int(real_website_date[1]), int(real_website_date[2]))))
        ],className="one column")
    ], className="row")
        # date=str(dt(2020, 6, 10))
    ])

    # app.css.append_css({
    #     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
    # })

    # row2 = html.Div(
    #     [
    #         dbc.Row(dbc.Col(html.Div([
    #             html.H1("New York State Covid-19 Tracker")],
    #             style={'textAlign': "center", "padding-bottom": "30"}))),
    #
    #         dbc.Row(
    #             [
    #                 dbc.Col(html.Div(dcc.Graph(
    #                     id="map",
    #                     style={'height': 700, 'width': 1000}
    #                 ))),
    #                 dbc.Col(html.Div("         ")),
    #                 dbc.Col(html.Div(dcc.DatePickerSingle(
    #                     id='my-date-picker-single',
    #                     min_date_allowed=dt(2020, 3, 2),
    #                     max_date_allowed=dt(int(real_website_date[0]), int(real_website_date[1]),
    #                                         int(real_website_date[2])),
    #                     initial_visible_month=dt(int(real_website_date[0]), int(real_website_date[1]),
    #                                              int(real_website_date[2])),
    #                     date=str(dt(int(real_website_date[0]), int(real_website_date[1]), int(real_website_date[2])))
    #                 ))),
    #             ])
    #     ])
    #
    #
    #
    # app.layout = html.Div(row2)


    @app.callback(
        Output(component_id='map', component_property='figure'),
        [Input(component_id='my-date-picker-single', component_property='date')])

    def update_map(date):
        if date is not None:
            date = dt.strptime(re.split('T| ', date)[0], '%Y-%m-%d')
            date_string = date.strftime('%Y-%m-%d')
            #print(date_string)
#             today = date.today()
#             website_date = today.strftime("%Y-%m-%d")
            #print("Today:" ,website_date)


        with urllib.request.urlopen(
                "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json") as url:
            #print(url)
            data = json.loads(url.read().decode())
            data['features'] = [x for x in data['features'] if x['properties']['STATE'] == '36']

            county_fips = [x['properties']['GEO_ID'].split("US")[1] for x in data['features'] if
                           x['properties']['STATE'] == '36']

            county_names = [x['properties']['NAME'] for x in data['features'] if x['properties']['STATE'] == '36']

            link="https://health.data.ny.gov/resource/xdss-u53e.json?test_date="+date_string+"T00:00:00.000"
            #print(link)


            #covid_website_data = "https://health.data.ny.gov/resource/xdss-u53e.json?test_date=" + website_date + "T00:00:00.000"
            with urllib.request.urlopen(    #covid_website_data) as url1:
                     "https://health.data.ny.gov/resource/xdss-u53e.json?test_date=" + date_string + "T00:00:00.000") as url1:
                data1 = json.loads(url1.read().decode())

                county_new_positives = [int(county['new_positives']) for county in data1]
                cumulative_number_of_positives = [int(county['cumulative_number_of_positives']) for county in data1]
                total_number_of_tests = [int(county['total_number_of_tests']) for county in data1]
                cumulative_number_of_tests = [int(county['cumulative_number_of_tests']) for county in data1]
                #print(county_new_positives)
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
                                           mapbox_style="carto-positron", #carto-positron
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

                fig.update_layout(dragmode = False, margin={"r": 0, "t": 0, "l": 0, "b": 0})

                #token = 'pk.eyJ1IjoicnV0aHZpa2FydmEiLCJhIjoiY2tiYmVxemdnMDBtbTJuczF3NGkzNDFpZyJ9.vljnNz8HP-riFZMH_TuZjQ'
                #fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
                #fig.update_xaxes(fixedrange=True)
                #fig.update_yaxes(fixedrange=True)
                # startingday = datetime.date(2020,5,16)
                # enday = startingday + timedelta(days=1)
                # print("startingday,endday",startingday,enday)
                #df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

                #fig2 = px.line(df, x='Date', y='AAPL.High')
                #fig2.show()
                return fig

    if __name__ =="__main__":
        app.run_server(debug=True)