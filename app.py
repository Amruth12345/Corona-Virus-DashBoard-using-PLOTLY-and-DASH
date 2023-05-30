import numpy as np
import pandas as pd
import dash
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


external_stylesheets = [    {        'href' : "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",        'rel' : "stylesheet",        'integrity' : "sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC",        'crossorigin' : "anonymous"    }]

patients = pd.read_csv('IndividualDetails.csv')

total = patients.shape[0]
Active = patients[patients['current_status'] == 'Hospitalized'].shape[0]
Recovered = patients[patients['current_status'] == 'Recovered'].shape[0]
Deaths = patients[patients['current_status'] == 'Deceased'].shape[0]


pbar = patients['detected_state'].value_counts()
ybl = pbar.tolist()
xam = pbar.index.tolist()



options = [    {'label': 'ALL', 'value': 'All'},    {'label': 'Hospitalized', 'value': 'Hospitalized'},    {'label': 'Recovered', 'value': 'Recovered'},    {'label': 'Deceased', 'value': 'Deceased'}]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Corona Virus Report', style={'color': '#248389', 'text-align': 'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Total cases', className='text-light'),
                    html.H4(total, className='text-light')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Active', className='text-light'),
                    html.H4(Active, className='text-light')
                ], className='card-body')
            ], className='card bg-info')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Recovered', className='text-light'),
                    html.H4(Recovered, className='text-light')
                ], className='card-body')
            ], className='card bg-success')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Deaths', className='text-light'),
                    html.H4(Deaths, className='text-light')
                ], className='card-body')
            ], className='card bg-secondary')
        ], className='col-md-3')
    ], className='row'),
    html.Div([], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker', options=options, value='ALL'),
                    dcc.Graph(id='bar')
                ], className='card-body')
            ], className='card')
        ], className='col-md-12')
    ], className='row')

], className='container')


@app.callback(Output('bar', 'figure'), [Input('picker', 'value')],prevent_initial_call=False)
def update_graph(fun):
    if fun == 'ALL':
        return {'data': [go.Bar(x=xam, y=ybl)], 'layout': go.Layout(title="State Total Count")}
    else:
        npat = patients[patients['current_status'] == fun]
        pbar = npat['detected_state'].value_counts()
        yb = pbar.tolist()
        xa = pbar.index.tolist()
        return {'data': [go.Bar(x=xa, y=yb)],
                'layout': go.Layout(title="State Total Count")}


if __name__ == "__main__":
    app.run_server(debug = True)