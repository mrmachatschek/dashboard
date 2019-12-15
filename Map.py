import dash
import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

df = pd.read_csv('data/coordinates.csv')


fig = go.Figure(data=go.Scattergeo(
        lon = df['lng'],
        lat = df['lat'],
        text = df['City'],
        mode = 'markers',
        marker_color = "red",
        ))

fig.update_layout(
        title = 'Cities in Project'
    )



app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
])


if __name__ == '__main__':
    app.run_server(debug=True)
