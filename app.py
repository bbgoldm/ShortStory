from dash import Dash, html, dcc, callback, no_update, callback_context, ctx
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls
import requests # used for making HTTP requests.  Built on urllib3.

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Short Story Creator", className='custom-div'),

    html.Div(
    [        
        dbc.Input(id="prompt", placeholder="Enter some keywords or a description for your short-story...", type="text"),
        # dbc.FormText("Type something in the box above")
    ],
    className='custom-div'
    ),

    html.Div(
    [
        dbc.Label("Select the length of the story...", html_for="dropdown"),
        dcc.Dropdown(
            id="length",
            options=[
                {'label': 'Short: 50-100 words', 'value': 'short'},
                {'label': 'Medium: 100-150 words', 'value': 'medium'},
                {'label': 'Long: 150-200 words', 'value': 'long'}
            ],
            value='short'
        ),
        dbc.FormText("*Longer stories will take longer time to generate."),
    ],
    className="custom-div",
    ),

    html.Div(
    [
        dbc.Label("Select the genre..."),
        dcc.Dropdown(
        id='genre',
        options=[
            {'label': 'Fantasy', 'value': 'fantasy'},
            {'label': 'Horror', 'value': 'horror'},
            {'label': 'Mystery', 'value': 'mystery'},
            {'label': 'Romance', 'value': 'romance'},
            {'label': 'Sci-Fi', 'value': 'sci-fi'},
            {'label': 'Thriller', 'value': 'thriller'}
        ],
        value='fantasy'
        ),
    ],
    className="custom-div",
    ),

    html.Div(
    [
        dbc.Button("Generate Story!", id='button',color="primary", className="me-1 left-margin"),
    ]
    ),

     html.Div(
        # dls is a spinner generator while waiting for story to load
        # https://dash-loading-spinners.sproodlebuzz.co.uk/
        dls.Pacman(
            [html.Div(id='output')],
            color="#3800D1",
            speed_multiplier=1,
            width=100,
        )
    ,style={'width':'50%','marginTop':'40px', 'marginBottom':'40px'}
    ),

    html.Div(
    [
        dbc.FormText("Not satisfied with your story?"),
        dbc.Button("Regenerate Story!", color='primary', className="me-1")
    ]
    , id='regenerate_button', style={'display': 'none'}),

])

# Callback to generate a user story
@app.callback(
    Output('output', 'children'),
    [Input('button', 'n_clicks'),
    Input("regenerate_button", "n_clicks")],
    [State('prompt', 'value'), State('length', 'value'), State('genre', 'value')],
    prevent_initial_call=True)
def update_output(n_clicks, regen_nclicks, prompt, length, genre):
    if not prompt:
        return 'Error: Please enter a prompt'
    if not length:
        return 'Error: Please select a length'
    if not genre:
        return 'Error: Please select a genre'
    try:
        # synchronous get request.  Another version that is async, aiohttp.
        response = requests.get('http://localhost:8000/openai', params={'prompt': prompt, 'length': length, 'genre': genre})
        if response.status_code == 200:
            return response.json()['choices'][0]['text']
        else:
            return 'Error'
    except requests.exceptions.RequestException as e:
        raise e

# Callback to display the Regenerate Button after story is generated
@app.callback(
    Output("regenerate_button", "style"),
    [Input("output","children")],
)
def update_regenerate_button(children):
    if children and ("Error" not in children):
        return {"display": "block"}
    else:
        return {"display": "none"}



if __name__ == '__main__':
    app.run_server(debug=True)