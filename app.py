import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import Dash,html,dcc
from dash.dependencies import Input, Output

external_stylesheets =[
{
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N",
        "crossorigin": "anonymous"
    }
]
patients=pd.read_csv('IndividualDetails.csv')
total=patients.shape[0]
active=patients[patients["current_status"]=='Hospitalized'].shape[0]
Recovered=patients[patients['current_status']=='Recovered'].shape[0]
deaths=patients[patients['current_status'] == 'Deceased'].shape[0]
options=[
    {'label':'All','value':'All'},
{'label':'Hospitalized','value':'Hospitalized'},
{'label':'Recovered','value':'Recovered'},
{'label':'Deceased','value':'Deceased'}
]
date=patients['diagnosed_date'].value_counts().reset_index()
patients['age']=patients['age'].fillna('missing')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div([
    html.H1("Corona Virus Pandemic",style={'color':'white','text-align':'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Total Cases'),
                    html.H4(total)
                ],className='card-body')
            ],className='card bg-danger text-white ')
        ],className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Active cases'),
                    html.H4(active)
                ],className='card-body')
            ],className='card bg-info text-white')

        ],className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Recovered'),
                    html.H4(Recovered)
                ],className='card-body')
            ],className='card bg-warning text-white')
        ],className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Deaths'),
                    html.H4(deaths)
                ],className='card-body')
            ],className='card bg-success text-white')
        ],className='col-md-3')
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='Line-Plot',
                              figure={'data':[go.Scatter(x=date['diagnosed_date'],y=date['count'],mode='lines')],
                                      'layout':go.Layout(title='day by day Analysis')})
                ],'card-body')
            ],className='card')
        ],className='col-md-6'),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='pie-chart',
                              figure={
                                  'data':[
                                      go.Pie(labels=patients['age'].value_counts().index,values=patients['age'].value_counts().values,
                                             hole=0.4)
                                  ],
                                  'layout':go.Layout(title='Age Distribution')
                              })
                ],className='card-body')
            ],className='card')

        ],className='col-md-6')
    ], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker',options=options,value='All'),
                    dcc.Graph(id='bar')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ], className='row'),

],className='container')
@app.callback(Output('bar','figure'),[Input("picker",'value')])
def update_graph(type):
    if type == 'All':
        pbar = patients['detected_state'].value_counts().reset_index()
    else:
        npat = patients[patients['current_status'] == type]
        pbar = npat['detected_state'].value_counts().reset_index()
    return go.Figure(
        data=[go.Bar(x=pbar['detected_state'],y=pbar['count'])],
        layout=go.Layout(title='states total counts'))



if __name__ == '__main__':
    app.run(debug=True,port=5000)