# Final Project Dashboard
# By Víctor Malumbres

### Modules ###

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

import datetime

import os
import sys

import numpy as np
import json
import pandas as pd

# Data file path
DataFolderPath = 'C:\\Users\\vmalumbres\\OneDrive - Fundacion CIRCE\\Escritorio\\CursoDashboard\\Datasets\\flights'
Data = pd.read_json(os.path.join(DataFolderPath, 'MyDB.json'))

"""
###### Database Processing ######

# Load datasets
AirlinesDf = pd.read_csv(os.path.join(DataFolderPath, 'airlines.csv'))
AirportDf = pd.read_csv(os.path.join(DataFolderPath, 'airports.csv'))
FlightDf = pd.read_csv(os.path.join(DataFolderPath, 'flights.csv'), low_memory=False)

# Wrappling data
FlightDf_wrap = FlightDf.sample(n=10_000)
FlightDf_wrap.drop(['CANCELLATION_REASON','AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY'], axis=1, inplace=True)

# Merge files
MyDB = FlightDf_wrap.merge(AirportDf, how='inner', left_on='ORIGIN_AIRPORT', right_on='IATA_CODE')
MyDB.rename({'AIRPORT':'ORIGIN_AIRPORT_NAME', 'CITY': 'ORIGIN_CITY', 'STATE' : 'ORIGIN_STATE',
             'COUNTRY': 'ORIGIN_COUNTRY', 'LATITUDE':'ORIGIN_LATITUDE', 'LONGITUDE':'ORIGIN_LONGITUDE'}, axis=1, inplace=True)

MyDB_v2 = MyDB.merge(AirportDf, how = 'inner', left_on = 'DESTINATION_AIRPORT', right_on='IATA_CODE')
MyDB_v2.rename({'AIRPORT':'DESTINATION_AIRPORT_NAME', 'CITY': 'DESTINATION_CITY', 'STATE' : 'DESTINATION_STATE',
             'COUNTRY': 'DESTINATION_COUNTRY', 'LATITUDE':'DESTINATION_LATITUDE', 'LONGITUDE':'DESTINATION_LONGITUDE'}, axis=1, inplace=True)

MyDB_v2.drop(['IATA_CODE_x', 'IATA_CODE_y'], axis = 1, inplace = True)

MyDB_v_final = MyDB_v2.merge(AirlinesDf, how='inner', left_on='AIRLINE', right_on='IATA_CODE', suffixes=('_CODE', '_NAME'))
MyDB_v_final.dropna(inplace=True)
MyDB_v_final.head()
MyDB_v_final.to_json(os.path.join(DataFolderPath, 'MyDB.json'))

"""

### DASH SIDE ###

# States dropdown settings
ListOfState = Data.ORIGIN_STATE.unique().tolist()
StateDDSettings = []

for State in ListOfState:
    StateDDSettings.append({'label': State, 'value': State})

# DataTable Settings
ColumnsToDisplay = ['FLIGHT_NUMBER', 'DAY', 'AIRLINE_CODE', 'ORIGIN_CITY', 'DESTINATION_CITY', 'DEPARTURE_DELAY']

# Chart Settings
ChartSettings = {'data': [], 'layout':{'title':'Delay Chart', 'xaxis': {'title': 'Airport'}, 'yaxis': {'title': '% in Delay'}}}

# Slider Settings
SliderSettings = {}

for MonthId in range(12):
    SliderSettings.update({str(MonthId):str(MonthId+1)})

# Map Settings
px.set_mapbox_access_token('pk.eyJ1Ijoidm1hbHVtYnJlcyIsImEiOiJjazhrOGd4bnUwN2ltM3Jubzl6NXpobHVqIn0.2K-4yHXlCjGhZhcH-3zbnQ')

MapSettings = px.line_mapbox(Data, lat="ORIGIN_LATITUDE", lon="ORIGIN_LONGITUDE", color="ORIGIN_AIRPORT", zoom=3, height=300)

MapSettings.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=4, mapbox_center_lat = 41, margin={"r": 0, "t": 0, "l": 0, "b": 0})

# Create a Dash Object
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

app.title = "Final Project"

# Navigation Bar
navbar = dbc.NavbarSimple(
    brand='Flight Delays and Cancellations - 2015',
    color='steelblue',
    dark=False
)

# Body
body = dbc.Container([
    # First Row
    dbc.Row([
        html.Br(),
    ]),

    # Second Row
    dbc.Row([
        # First Column
        dbc.Col([
            # Dropdown
            dcc.Dropdown(
                id="States-Dropdown",
                options=StateDDSettings,
                multi=True,
                searchable=True,
                placeholder='Choose state/s ...'
            )
        ], width=6),

        # Second Column
        dbc.Col([
            # Dropdown
            dcc.Dropdown(
                id="Cities-Dropdown",
                options=[],
                multi=True,
                searchable=True,
                placeholder='Choose city or cities from state/s ...'
            )
        ], width=6)
    ]),

    # Third Row
    dbc.Row([
        html.Br()
    ]),

    # Fourth Row
    dbc.Row([
        # First Column
        dbc.Col([
            # Table
            dt.DataTable(
                id='Table',
                columns=[{'name': column, 'id': column} for column in ColumnsToDisplay],
                data=Data.to_dict('records'),
                style_table={
                    'overflow-x': 'scroll',
                    'overflow-y': 'scroll',
                    'maxHeight': '2000px',
                    'maxWidth': '3000px',
                },
                style_cell={'text-align': 'center'},
                style_header={'font-weight': 'bold', 'background-color': 'steelblue'},
                style_data_conditional=[

                    {
                        'if': {'filter_query': '{DEPARTURE_DELAY} > 0.0'},
                        'background_color': 'red'
                    },
                    {
                        'if': {'filter_query': '{DEPARTURE_DELAY} < 0.0'},
                        'background_color': 'green'
                    }
                ],
                filter_action='native',
                editable=False,
                sort_action='native',
                sort_mode='multi',
                page_size=10,
                page_current=0,

            )

        ], width=6),

        # Second Column
        dbc.Col([
            dcc.Graph(
                id='Chart',
                figure=ChartSettings
            )
        ], width=6)
    ]),

    # Fifth Row
    dbc.Row(
        html.Br(),
    ),
    # Sixth Row
    dbc.Row([
        dcc.Graph(
            id='map',
            figure=MapSettings
        )
    ]),

    # Seventh Row
    dbc.Row(
        html.Br(),
    ),
    # Eight Row
    dbc.Row([
        dbc.Col([
            html.H1("Month")
        ]),
        dbc.Col([
            ## Slider
            dcc.RangeSlider(
                id='slider',
                min=0,
                max=11,
                step=1,
                value=[1, 2],
                marks=SliderSettings
            )
        ], width=10)
    ])
])

# Add to app layout
app.layout = html.Div([navbar, body])


####### Callbacks #########


# Callback for city dropdown
@app.callback(
    [dash.dependencies.Output('Cities-Dropdown', 'options')],
    [dash.dependencies.Input('States-Dropdown', 'value')]
)
def UpdateSettingForCitiesDropdown(States):

    global Data

    try:
        # Split data per states
        DataPerState = Data[Data.ORIGIN_STATE.isin(States)]

        # Get a list of cities from those states
        ListOfCities = DataPerState.ORIGIN_CITY.unique().tolist()
        CitiesDDSettings = []
        for City in ListOfCities:
            CitiesDDSettings.append({'label': City, 'value': City})
    except:
        CitiesDDSettings = []

    return [CitiesDDSettings]



# Callback for DataTable
@app.callback(
    [dash.dependencies.Output('Table', 'data')],
    [dash.dependencies.Input('Cities-Dropdown', 'value')]
)
def UpdateDataFromCities(Cities):

    global Data

    # Logic
    if Cities != None:
        # Split data per cities
        DataPerCities = Data[Data['ORIGIN_CITY'].isin(Cities)]
    else:
        DataPerCities = Data.copy()

    return [DataPerCities.to_dict('records')]

# Callback for Chart
@app.callback(
    [dash.dependencies.Output('Chart', 'figure')],
    [dash.dependencies.Input('Cities-Dropdown', 'value')]
)
def UpdateChartData(Cities):

    global Data

    # Split data per origin cities
    if Cities != None:

        # Split data per cities
        DataPerCities = Data[Data['ORIGIN_CITY'].isin(Cities)]


        ChartSettings = {'data': [{'x':[], 'y':[],'type':'bar','name':'Delay'}], 'layout': {'title': 'Delay Chart', 'xaxis': {'title': 'Airport'}, 'yaxis': {'title': '% in Delay'}}}
    else:
        ChartSettings = {'data': [], 'layout': {'title': 'Delay Chart', 'xaxis': {'title': 'Airport'}, 'yaxis': {'title': '% in Delay'}}}

    return [ChartSettings]


###### Run server ######
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80, debug=True)