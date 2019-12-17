import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
from dash.dependencies import Input, Output, State

df = pd.read_csv("data/sun.csv")


data = [go.Scatter(x=[1,2,3],y=[1,2,3], marker=dict(symbol="circle", color="yellow"))]

fig = go.Figure(data)

fig.show()