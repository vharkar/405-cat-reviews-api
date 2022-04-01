import dash
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from helpers.key_finder import api_key
from helpers.api_call import *
from helpers.vader import sentiment_scores

########### Define a few variables ######

tabtitle = 'Cats'
sourceurl = 'https://docs.thecatapi.com/'
sourceurl2 = 'https://docs.thecatapi.com/api-reference/breeds/breeds-list'
githublink = 'https://github.com/vharkar/405-cat-reviews-api'


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
                        html.H6('Description:'),
                        html.Div(id='description', children=[])
                    ], className='six columns')
                
                ], style={ 'padding': '12px',
                           'font-size': '22px',
                            # 'height': '400px',
                           'border': 'thick grey solid',
                           'textAlign': 'left',
                }, className='six columns')
                
            ], className='twelve columns'),

        ], className='twelve columns'),
              
        # Cat Ratings Graph
        html.Div([
                html.Br(),
                dcc.Graph(id='ratings')
        ], style={ 'align': 'center'}, className='six columns'),
    
        # Recommendation
        html.Div([
                html.Br(),
                html.H6('Recommendation as a family pet:'),
                html.Div(id='recommendation', children=[])
        ], style={ 'align': 'center'}, className='six columns'),
    
        # Cat Picture
        html.Div([
            html.Br(),
            html.Img(id='catpic', style={'height':'50%', 'width':'50%'})
        ], style={ 'align': 'center'}, className='eight columns'),

        # Output
        html.Div([
            # Footer
            html.Br(),
            html.A('Code on Github', href=githublink, target="_blank"),
            html.Br(),
            html.A("Data Source", href=sourceurl, target="_blank"),
            html.Br(),
            html.A("API", href=sourceurl2, target="_blank"),
        ], className='twelve columns'),
    ]
)

########## Callbacks

# TMDB API call
@app.callback([Output('origin', 'children'),
               Output('temperament', 'children'),
               Output('description', 'children'),
               Output('recommendation', 'children'),
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
    breed_attrs_df.reset_index(inplace=True)
    ratings_fig = get_ratings_fig(breed_attrs_df)

    description = cats_df.loc[cats_df['id']==breed][['description']].iat[0,0]
    recommendation = sentiment_scores(description)
    
    catpic  = cats_df.loc[cats_df['id']==breed][['image.url']].iat[0,0]
    origin  = cats_df.loc[cats_df['id']==breed][['origin']].iat[0,0]
    temperament = cats_df.loc[cats_df['id']==breed][['temperament']].iat[0,0]

    return origin, temperament, description, recommendation, ratings_fig, catpic


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
