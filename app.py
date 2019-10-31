import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import flask
import plotly.graph_objs as go
import os
import glob

app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True


Month_YEARS = ['Dec-2015','Jan-2016', 'April-2016','Oct-2016','Jan-2017', 'April-2017','Oct-2017',
               'Jan-2018', 'April-2018','Jan-2019', 'April-2019','Oct-2019']

image_route='data/forest/'
static_image_route = os.path.abspath(image_route)
list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_route))]

app.layout = html.Div(
    id="root",
    children=[
            html.Div(
                id="header",
                children=[
                    #html.Img(id="logo", src=app.get_asset_url("dash-logo.png")),
                    html.H4(children="Green Cover over Western Area using Satellite Imagery"),
                    html.P(
                        id="description",
                        children="Developed as a joint project between DSTI, Sierra Leone and SpaceSense.ai, Paris",
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Drag the slider to change the month-year:",
                                ),
                                dcc.Slider(
                                    id="years-slider",
                                    min=0,
                                    max=11,
                                    value=4,
                                    marks={i: Month_YEARS[i] for i in range(len(Month_YEARS))
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="graph-container",
                            children=[
                                html.P(id="chart-selector", children="Select chart:"),
                                dcc.Dropdown(
                                options=[{'label': 'Green Ratio', 'value': 'GR'},
                                         {'label': 'NA', 'value': 'VI'}],

                                    value=list_of_images[0],
                                    id="chart-dropdown",
                                    ),
                                ],
                        ),
                        html.Img(
                            id = 'image',
                            className="three columns",
                            style={
                                'height': 4483/10,
                                'width': 4258/10,
                                },


                        ),
                    ],
                ),

            ],
        ),
    ]
)


@app.callback(Output("image", "src"),
              [Input("years-slider",'value')])
             # [Input("years-slider", "value")])
def update_body_image(i):
    print(static_image_route +Month_YEARS[i]+'.png')
    return static_image_route +Month_YEARS[i]+'.png'

@app.server.route('{}<image_path>.png'.format(static_image_route))
def serve_image(image_path):
    image_name = '{}.png'.format(image_path)
    if image_name not in list_of_images:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
    return flask.send_from_directory(static_image_route, image_name)

if __name__ == '__main__':
    app.run_server(debug=True)
