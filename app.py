import dash
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from helpers.key_finder import api_key
from helpers.api_call import *


########### Define a few variables ######

tabtitle = 'Cats'
sourceurl = 'https://docs.thecatapi.com/'
sourceurl2 = 'https://docs.thecatapi.com/api-reference/breeds/breeds-list'
githublink = 'https://github.com/vharkar/405-movie-reviews-api'


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

breeds=[]
names=[]
breeds, names, cats_df = api_get_breeds_list_and_df()

########### Layout

app.layout = html.Div(children=[
        html.Div([
            html.H1(['Which cat is best for your family ?']),
            html.Div([
                html.Div([
                    html.Div([
                       html.H6('Select cat breed:'),
                         dcc.Dropdown(
                           id='breed-drop',
                           options=[{'label': n, 'value': v} for n, v in zip(names, breeds)],
                           value='abys'),
                       html.Br()
                    ], className='three columns'),
                
                    html.Div([
                        html.H6('Country of Origin:'),
                        html.Div(id='origin', children=[])
                    ], className='three columns'),
                    html.Div([
                        html.H6('Temperament:'),
                        html.Div(id='temperament', children=[])
                    ], className='three columns'),
                    html.Div([
                        html.Br(),
                        dcc.Graph(id='ratings')
                    ], className='three columns'),
                
                ], style={ 'padding': '12px',
                           'font-size': '22px',
                            # 'height': '400px',
                           'border': 'thick grey solid',
                           'textAlign': 'left',
                }, className='six columns'),
            ], className='twelve columns'),
        
            html.Br(),

        ], className='twelve columns'),
    
        # Cat Picture
        html.Div([html.Img(id='catpic', style={'height':'50%', 'width':'50%'})]),

        # Output
        html.Div([
            # Footer
            html.Br(),
            html.A('Code on Github', href=githublink, target="_blank"),
            html.Br(),
            html.A("Data Source: Kaggle", href=sourceurl, target="_blank"),
            html.Br(),
            html.A("Data Source: TMDB", href=sourceurl2, target="_blank"),
        ], className='twelve columns'),
    ]
)

########## Callbacks

# TMDB API call
@app.callback([Output('origin', 'children'),
               Output('temperament', 'children'),
               Output('ratings', 'figure'),
               Output('catpic', 'src')],
               Input('breed-drop', 'value'))
def on_select(breed):
   
    breed_attrs_df = cats_df[cats_df['id']==breed][['adaptability',\
                                                  'affection_level',\
                                                  'child_friendly',\
                                                  'dog_friendly',\
                                                  'energy_level',\
                                                  'grooming',\
                                                  'health_issues',\
                                                  'intelligence',\
                                                  'shedding_level',\
                                                  'social_needs',\
                                                  'stranger_friendly']]

    ratings_fig = get_ratings_fig(breed_attrs_df)

    catpic  = cats_df.loc[cats_df['id']==breed][['image.url']].iat[0,0]
    origin  = cats_df.loc[cats_df['id']==breed][['origin']].iat[0,0]
    temperament = cats_df.loc[cats_df['id']==breed][['temperament']].iat[0,0]

    return origin, temperament, ratings_fig, catpic

#@app.callback([Output('movie-title', 'children'),
#                Output('movie-release', 'children'),
#                Output('movie-overview', 'children'),
#                ],
#              [Input('tmdb-store', 'modified_timestamp')],
#              [State('tmdb-store', 'data')])
#def on_data(ts, data):
#    if ts is None:
#        raise PreventUpdate
#    else:
#        return data['title'], data['release_date'], data['overview']


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
