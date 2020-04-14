# First script 
# Example of how Dash works
# Some charts, settings as json, etc.
# Script by Víctor Malumbres (Teacher Abraham Requena)

import dash
import dash_core_components as dcc
import dash_html_components as html

# Load a list of style (.css files)
# codeopen.io is a web where you can take html & css styles
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Create a Dash Object (Similitudes with flask)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Json file for Graph Settings
FigureSettings = {
    
    "data":[
        {"x":[0,1,2,3,4], "y":[5,5,5,5,5], "type":"line", "name":"Line-1"},
        {"x":[0,1,2,3,4], "y":[10,10,15,15,15], "type":"scatter", "name":"Line2"}
    ],

    "layout": {"title":"My First Chart with Dash"}
    
}

# Add to our app a layout (HTML)
#
# html.Div ==> <div> ... </div>
app.layout = html.Div([
    html.H1("¡Hola mundo!"),
    html.Br(),
    dcc.Graph(
        id='My first chart',
        figure=FigureSettings
    )
])


if __name__ == "__main__":
    app.run_server(port=80, debug=True)


