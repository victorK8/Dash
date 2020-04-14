# Fourth script
# For Datatable Examples
# Script by Víctor Malumbres

### Modules ###

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table as dt

import datetime

import os
import sys

import numpy as np
import json
import pandas as pd

##### Managing Local files #####

# Data file path
FilePath = 'C:\\Users\\vmalumbres\\OneDrive - Fundacion CIRCE\\Escritorio\\CursoDashboard\\Datasets\\cursos.csv'

# Open file as Dataframe
Data = pd.read_csv(FilePath, encoding='Latin-1')

##### Dashboard #####

# Add css Style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Create a Dash Object (Similitudes with flask)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Change title
app.title = 'Datatable Examples'

# Layout
app.layout = html.Div(children=[
    dt.DataTable(
        id='table',
        columns=[{'name': column, 'id': column} for column in Data.columns],
        data=Data.to_dict('records'),
        style_table={
            'overflow-x':'scroll',
            'overflow-y': 'scroll',
            'maxHeight': '2000px',
            'maxWidth': '2200px',
            'border':'solid red thin'
        },
        #fixed_columns={'headers':True, 'data':2},
        #fixed_rows={'headers':True, 'data':2},
        style_cell={'text-align':'center'},
        style_header={'font-weight':'bold', 'background-color': '#FFA07A'},
        style_data_conditional=[
            {
                'if':{'row_index':'odd'},
                'background_color':'#ADD8E6'
            },
            {
                'if':{'column_id':'puntuacion','filter_query':'{puntuacion} le 3.0'},
                'background_color':'#ADD8E2'
            }
        ],
        filter_action='native',
        editable=True,
        sort_action='native',
        sort_mode='multi',
        page_size=3,
        page_current=0,
        row_deletable=True,
        row_selectable='multi'
    )
], className='six columns')

# Run server
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80, debug=True)