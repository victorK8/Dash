# Fifth script
# For exercises
# Script by Víctor Malumbres

### Modules ###

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import datetime

import os
import sys

import numpy as np
import json
import pandas as pd


# Create a Dash Object (Similitudes with flask)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.title = "Bootstrap Example"

# Navigation Bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Menu", header=True),
                dbc.DropdownMenuItem("Dashboard", href="#"),
                dbc.DropdownMenuItem("About me", href="#")
            ]
        )
    ],
    brand='This My Web Page',
    color='red',
    dark=False
)

# Body
body = dbc.Container([
    # Row-1
    dbc.Row([
        dbc.Col([
            html.Div([
                # Alert
                dbc.Alert([
                    "Using bootstrap component:  ",
                    html.A('Alert', href='https://dash-bootstrap-components.opensource.faculty.ai/docs/components/alert/', target='_blank', className='alert-link')
                ], color='danger'),

            ])
        ], width={"size": 6, "offset": 3})
    ]),

    html.Br(),

    # Row-2
    dbc.Row([
        # Col-1
        dbc.Col([
            html.Div([
                # Button
                dbc.Button('button-1', color='primary')
            ])
        ], width={"width": 3, "offset":0}),

        # Col-2
        dbc.Col([
            html.Div([
                # Button
                dbc.Button('button-2', color='primary')
            ])
        ], width={"width": 3, "offset": 3}),

        # Col-3
        dbc.Col([
            html.Div([
                # Button
                dbc.Button('button-3', color='primary')
            ])
        ], width={"width": 3, "offset": 6})

    ]),

    html.Br(),

    # Row-3
    dbc.Row([

        # Col for spiner
        dbc.Col([
            html.Div([
                dbc.Spinner(color='sucess')
            ])
        ]),

        html.Br(),

        # Col for Progress Bar
        dbc.Col([
            html.Div([
                dbc.Progress(
                    id='progress-bar',
                    value=0,
                    max=100,
                    striped=True,
                    animated=True
                ),
                dcc.Interval(
                    id='interval-obj',
                    interval=500,
                    n_intervals=0
                )
            ])
        ], width=8)

    ])
])

# Add to app layout
app.layout = html.Div([navbar, body])


#### Callbacks
@app.callback(
    [dash.dependencies.Output('progress-bar', 'value')],
    [dash.dependencies.Input('interval-obj', 'n_intervals')]
)
def LoadingProgress(n_intervals):
    return min(n_intervals % 102, 100)


# Run server
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80, debug=True)