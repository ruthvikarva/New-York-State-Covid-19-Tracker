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

class Covid:
    conn = sqlite3.connect('Covid.db')
    curs = conn.cursor()

    curs.execute('select date from corona order by date desc limit 1')
    today=curs.fetchall()
    unixDate = str(date.fromtimestamp(today[0][0]))
    print(today,unixDate)
    real_website_date = str(unixDate).split('-')

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
                )], className="nine columns"),
            html.Div([
                dcc.DatePickerSingle(
                    id='my-date-picker-single',
                    min_date_allowed=dt(2020, 3, 2),
                    max_date_allowed=dt(int(real_website_date[0]), int(real_website_date[1]),
                                        int(real_website_date[2])),
                    initial_visible_month=dt(int(real_website_date[0]), int(real_website_date[1]),
                                             int(real_website_date[2])),
                    date=date(int(real_website_date[0]), int(real_website_date[1]), int(real_website_date[2])))
            ], className="one column")
        ], className="row")
        # date=str(dt(2020, 6, 10))
    ])

    @app.callback(
        Output(component_id='map', component_property='figure'),
        [Input(component_id='my-date-picker-single', component_property='date')])

    def update_map(date):
        date_time_obj = datetime.strptime(date, '%Y-%m-%d')
        unixTime = int(time.mktime(date_time_obj.timetuple()))

        conn = sqlite3.connect('Covid.db')
        curs = conn.cursor()
        str_unixTime=str(unixTime)
        #query="select count(date) from corona where date = %s",(unixTime)
        t=(unixTime,)
        curs.execute('SELECT COUNT(Date) FROM CORONA WHERE Date = ?',t)
        count=curs.fetchall()
        print(count)
        #if ourdate is not None:
            #date = dt.strptime(re.split('T| ', ourdate)[0], '%Y-%m-%d')
            #unixDate=date(ourdate)
            #print("date: ",unixDate)
            #unixTime = int(time.mktime(date.timetuple()))
            #unixDate = date.fromtimestamp(unixTime)
            #date_string = date.strftime('%Y-%m-%d')
    if __name__ == "__main__":
        app.run_server(debug=True)

