# Third script 
# For exercises
# Script by Víctor Malumbres 

### Modules ###

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import plotly.graph_objects as go

import datetime 

import os
import sys

import numpy as np
import json
import pandas as pd

##### Managing Local files #####

# Data file path
FilePath = 'C:\\Users\\vmalumbres\\OneDrive - Fundacion CIRCE\\Escritorio\\CursoDashboard\\Datasets\\crimes-in-boston\\crime_30K.csv'

# Open file as Dataframe
Data = pd.read_csv(FilePath, encoding='Latin-1')

##### Dashboard #####

# Add css Style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Create a Dash Object (Similitudes with flask)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Change Web Title
app.title = "Exercise"

##### Check List Settings

# Get years &  sort them
ListOfYears = Data.YEAR.unique().tolist()
ListOfYears.sort()

# Create CheckList Options
CheckListOptions = []

for year in ListOfYears:
    Option = {'label': str(year), 'value': year}
    CheckListOptions.append(Option)

#### Dropdown Settings
ListOfLabelsForDropdown = Data.UCR_PART.unique().tolist()
ListOfLabelsForDropdown = ListOfLabelsForDropdown[:-1] # For removing nan value

DropdownOptions = []

for LabelForDropdown in ListOfLabelsForDropdown:
    Option = {'label': LabelForDropdown, 'value': LabelForDropdown }
    DropdownOptions.append(Option)

#### Chart Settings

# x-values
ListOfDistricts = Data.DISTRICT.unique().tolist()

# y-values
N_CrimesForEachDistrict = []

for District in ListOfDistricts:
    DataSplittedPerDistrict = Data[Data['DISTRICT'].isin([District])]
    N_CrimesInThatDistrict = DataSplittedPerDistrict.shape[0]
    N_CrimesForEachDistrict.append(N_CrimesInThatDistrict)

# Add values to settings
ChartSettings = {'data': [{'x':ListOfDistricts, 'y':N_CrimesForEachDistrict, 'type':'bar', 'name':'Number Of Crimes'}],
                 'layout': {'title':'Crimes in Boston', 'xaxis': {'title': 'District'}, 'yaxis': {'title':'Number Of Crimes'}}}


#### Slider Settings

ListOfMonths = Data.MONTH.unique().tolist()
ListOfMonths.sort()

SliderMarks = dict()

for Month, MonthId in zip(ListOfMonths, range(len(ListOfMonths))):
    Mark = {MonthId: {'label':'Month ' + str(Month), 'style': {'font-size':'20px'}}}
    SliderMarks.update(Mark)

#### Some table settings
ColumnsToShow = ['INCIDENT_NUMBER', 'OFFENSE_DESCRIPTION', 'DISTRICT', 'OCCURRED_ON_DATE', 'DAY_OF_WEEK', 'UCR_PART', 'Location']


#### Add layout (HMTL, CSS & Javascript)
app.layout = html.Div(children=[

    # Encabezado principal
    html.H1(" DASHBOARD SOBRE LOS CRÍMENES DE BOSTON ", style={'font-size':'50px', 'text-align': 'center'}),
    html.Br(),

    # Tabs
    dcc.Tabs(
       id='Tabs',
       children=[
           dcc.Tab(id='Tab-1', label='Estadísticas', value='statistics', style={'font-size':'30px'}, children=[
               html.Div([
                   # Título
                   html.Br(),
                   html.Br(),
                   html.H1(" Estadísticas De Crímenes de Boston", style={'text-align': 'center'}),
                   html.Br(),

                   # Checkbox & Dropdown
                   html.Div([
                       html.Div(children=[
                           dcc.Checklist(
                               id='checklist',
                               options=CheckListOptions,
                               value=[ListOfYears[0]],
                               labelStyle={'font-size':'25px', 'display':'inline-block', 'text-align': 'center', 'padding':'2%'},
                           )
                        ], className='six columns'),

                       html.Div(children=[
                            dcc.Dropdown(
                                id="dropdown",
                                placeholder='Choose UCR part ...',
                                searchable=True,
                                options=DropdownOptions,
                                multi=True,
                                value=['Other']

                            )
                        ], className ='six columns')

                   ], className='row'),

                   # Chart & Slider
                   html.Div(children=[
                       html.Div(children=[
                           # Chart
                           html.Br(),
                           dcc.Graph(
                               id='Chart',
                               figure=ChartSettings
                           ),
                       ], className='twelve columns'),
                       html.Div(children=[
                           # RangeSlider
                           html.Br(),
                           dcc.RangeSlider(
                               id='Slider',
                               min=0,
                               max=len(ListOfMonths) - 1,
                               step=1,
                               marks=SliderMarks,
                               value=[0, 2]
                           )
                       ], className='eleven columns'),
                   ], className='row')

               ], className='row')

           ]),

           dcc.Tab(id='Tab-2', label='Tabla de datos', value='datatable', style={'font-size':'30px'}, children=[
               html.Div(children=[
                   # Title
                   html.Div(children=[
                       html.Br(),
                       html.H1('DataBase', style={'text-align': 'center'}),
                       html.Br()
                   ], className='row'),

                   # Tabla
                   html.Div(children=[
                       dt.DataTable(
                           id='table',
                           columns=[{'name': column, 'id': column} for column in ColumnsToShow],
                           data=Data[ColumnsToShow].to_dict('records'),
                           style_cell={'text-align': 'center'},
                           style_header={'font-weight': 'bold', 'background-color': '#F8F8FF', 'max-width':'250px', 'overflow-x':'scroll'},
                           filter_action='native',
                           sort_action='native',
                           sort_mode='multi',
                           page_size=15,
                           page_current=0,
                           row_selectable='multi',
                           style_data_conditional=[
                               {    # If row_idx is odd, set row color as grey
                                   'if': {'row_index': 'odd'},
                                   'background_color': '#FFF8DC'
                               },
                               {    # If vandalism in offense_descrption, set row color as green
                                   'if': {'filter_query': '{OFFENSE_DESCRIPTION} eq VANDALISM'},
                                   'background_color': '#8FBC8F'
                               },
                               {  # If saturday in offense_description, set row color as green
                                   'if': {'column_id': 'DAY_OF_WEEK', 'filter_query': '{DAY_OF_WEEK} eq Saturday'},
                                   'background_color': '#CD5C5C'
                               },
                               {  # If sunday in offense_descrption, set row color as green
                                   'if': {'column_id': 'DAY_OF_WEEK', 'filter_query': '{DAY_OF_WEEK} eq Sunday'},
                                   'background_color': '#CD5C5C'
                               }
                           ],
                           style_table={'overflow-x': 'scroll'},
                       )
                   ], className='row')
               ], className='row')
           ])
       ]
    )
    # Store for update chart data
    #dcc.Store()
 ])


#### ______ Callbacks ______ #####
@app.callback(
    [dash.dependencies.Output('Chart', 'figure')],
    [dash.dependencies.Input('checklist', 'value'),
     dash.dependencies.Input('dropdown', 'value'),
     dash.dependencies.Input('Slider', 'value')]
)

def UpdateChart(Year, Part, MonthRange):

    # Get data
    global Data

    # New Json for chart settings
    NewChartSettings = dict()

    # Split data per month, year and Part
    DataPerMonth = Data[Data['MONTH'].isin([MonthKey for MonthKey in range(MonthRange[1])])]
    DataPerYear = DataPerMonth[DataPerMonth['YEAR'].isin(Year)]
    DataPerYearAndPart = DataPerYear[DataPerYear['UCR_PART'].isin(Part)]

    # x-values
    ListOfDistricts = Data.DISTRICT.unique().tolist()

    # y-values
    N_CrimesForEachDistrict = []

    for District in ListOfDistricts:
        DataSplittedPerDistrict = DataPerYearAndPart[DataPerYearAndPart['DISTRICT'].isin([District])]
        N_CrimesInThatDistrict = DataSplittedPerDistrict.shape[0]
        N_CrimesForEachDistrict.append(N_CrimesInThatDistrict)

    # Add values to settings
    NewChartSettings = {
        'data': [{'x': ListOfDistricts, 'y': N_CrimesForEachDistrict, 'type': 'bar', 'name': 'Number Of Crimes'}],
        'layout': {'title': 'Crimes in Boston', 'xaxis': {'title': 'District'}, 'yaxis': {'title': 'Number Of Crimes'}}}

    return [NewChartSettings]

# Run server
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80, debug=True)
