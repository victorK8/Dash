# Second script 
# Use of different components
# Script by Víctor Malumbres (Teacher Abraham Requena)

import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime 

# Add Style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Create a Dash Object (Similitudes with flask)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Slider marks json
MySliderMarks = dict()

for i in range(0, 11, 1):
    MySliderMarks.update({i:str(i) + " [uds.]"})

# Range Slider marks json
MyRangeSliderMarks = dict()

for i in range(0, 101, 5):
    MyRangeSliderMarks.update({i:str(i) + " %"})


# HTML Layout
app.layout = html.Div([
 
    html.H1(" Main Components "),   # <h1> Main Components </h1>
    html.Br(),                    # <br></br>
    html.P(" Explain of main components of Dash ", style={"font-size":"20px"}), # <p1>  Explain of main components of Dash </p1>  Linked to .css component
    html.Br(),                    # <br></br>

    html.H2(" Dropdown "),        # <h2> Dropdown </h2>
    html.Br(),                    # <br></br>
    html.Div([                    # <div> Dropdown </div>
        dcc.Dropdown(             # Dropdown
            id = "dropdown-example",
            options = [
                {"label": "city-1", "value":"Zaragoza"},
                {"label": "city-2", "value":"Madrid"},
                {"label": "city-3", "value":"Alfaro"}
            ],
            placeholder = "Choose ...",
            multi = True,
            searchable = True,
            value =  "Madrid",
            disabled = False,
            className = 'six columns'
        )
    ],className="row"),
    html.Br(),                    # <br></br>

    html.H3(" Slider "),          # <h3> Slider </h3>
    html.Br(),                    # <br></br>
    html.Div([                    # <div> Slider </div>
        dcc.Slider(
            id = "slider-example",
            min = 0,
            max = 10,
            step = 1,
            marks = MySliderMarks,
            value = 5,
            updatemode = "mouseup",
            className = "nine columns"
        )
    ],className="row"),
    html.Br(),                    # <br></br>

    html.H4(" Range Slider "),   # <h4> Range Slider </h4>
    html.Br(),                    # <br></br>
    html.Div([                     # <div> Range Slider </div>
        dcc.RangeSlider(
            id = "range-slider-example",
            min = 0,
            max = 100,
            step = 5,
            marks = MyRangeSliderMarks,
            value = [50,60],
            pushable = 10,
            className = 'nine columns'
        )
    ],className="row") ,
    html.Br(),                    # <br></br>

    html.H5(" Input "),           # <h5> Input </h5>
    html.Br(),                    # <br></br>
    html.Div([                    # <div> Input </div>
        dcc.Input(
            id = "input-example",
            placeholder = "Write some comment (Máx. of 250 characters) ...",
            type = "text",
            maxLength = 250,
            autoFocus = True,
            debounce = True,
            className = 'five columns'
        )
    ],className="row"),
    html.Br(),                     # <br></br>

    html.H6(" Text Area, Checkbox, Radio Item "),        # <h6> Text Area </h6>
    html.Br(),                    # <br></br>
    html.Div(id = 'TextArea-Checkbox-RadioItem', children = [   # <div> Text Area, Checkbox, Radio Item</div>
        html.P("Text Area"),
        html.Br(),
        dcc.Textarea(
            id = "text-area-example",
            lang = "gb",
            placeholder = "Write here (500 char as max.)",
            maxLength = 500,
            cols = 50,
            rows = 10,
            readOnly = False,
            title = "Your Text",
            draggable = True
        ),
        html.P("Check List"),
        html.Br(),
        dcc.Checklist(
            id = "checklist-example",
            options = [{"label": "Temperature","value":20},{"label": "Humidity","value":50},{"label": "Pressure","value":1000}],
            value = [20]
        ),
        html.P("Radio Items"),
        html.Br(),
        dcc.RadioItems(
            id = "radio-items-example",
            options = [{"label": "Temperature","value":20},{"label": "Humidity","value":50},{"label": "Pressure","value":1000}],
            value = 20
        )
    ],className="row"),
    html.Br(),                     # <br></br>

    html.Div(id = 'Button-Dates-Markdown', children = [   # <div> Button-Dates-Markdown</div>
        html.P("Button"),
        html.Br(),
        html.Button(
            "Sent",
            id = "button-example",
            draggable = "True",
            contentEditable = "False",
            n_clicks = 0,
            n_clicks_timestamp = -1
        ),

        html.P("Date Picker Single"),
        html.Br(),
        dcc.DatePickerSingle(
            id = "date-single-example",
            min_date_allowed = datetime.datetime(2020,3,1),
            max_date_allowed = datetime.datetime.today(),
            date = datetime.datetime.today(),
            clearable = False,
            with_portal = True,
            display_format = "DD/MM/YYYY",
            stay_open_on_select = True,
            first_day_of_week = 1
        ),

        html.P("Date Picker Range"),
        html.Br(),
        dcc.DatePickerRange(
            id = "date-range-example",
            start_date_placeholder_text = " Choose date for going ...",
            end_date_placeholder_text = " Choose date for returning ...",
            minimum_nights = 5,
            with_portal = True,
            display_format = "DD/MM/YYYY",
            stay_open_on_select = True,
            first_day_of_week = 1,
        ),

        html.P("Markdown"),
        html.Br(),
        dcc.Markdown(
            id = "markdown-example",
            children = "hola"
        ),

    ],className="row"),
    html.Br(),                     # <br></br>

    html.Div(id = 'Upload-Pestañas-Gráficas', children = [   # <div> Upload-Pestañas-Gráficas </div>
        html.P("Upload"),
        html.Br(),
        dcc.Upload(
            id = "upload_example",
            children = ['Drag your files'],
            disabled = False,
            max_size = 1000,
            min_size = 50,
            multiple = True,
            style = {"width":'50%', "height":'60px', "lineHeight": '60px', "borderWidth": '1px', "borderStyle": 'dash', 'borderRadius':'5px', "textAlign":'center', "margin":"10px"}
        ),

        html.P("Tabs"),
        html.Br(),
        dcc.Tabs(
            id = "tabs-example",
            children = [
                dcc.Tab(
                    id = 'tab-1',
                    value = 'Madrid',
                    label = 'Ciudades'
                ),
                 dcc.Tab(
                    id = 'tab-2',
                    value = 'Ebro',
                    label = 'Ríos'
                )
            ]
            ),

        html.P("Chart"),
        html.Br(),
        dcc.Graph(

        ),

    ],className="row"),
    html.Br(),                     # <br></br>

])


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80, debug=True)

