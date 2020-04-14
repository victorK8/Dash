# Example to add Dash app to Flask server backed
# Script by Víctor Malumbres (Based on Dash Documentation)

import flask
import dash
import dash_html_components as html

server = flask.Flask(__name__)

@server.route('/')
def index():
    return 'Hello Flask app'

# Create app with dash (Backend settings from Flask server)
app = dash.Dash( __name__,server=server,  routes_pathname_prefix='/DashAppURL/')

# Add to Dash App an layout
app.layout = html.Div("My Dash app")

# Run Server
if __name__ == '__main__':
    server.run_server(host='0.0.0.0', port=80, debug=True)