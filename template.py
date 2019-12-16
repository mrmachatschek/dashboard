import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
from dash.dependencies import Input, Output, State

def filtering(df,name,year=0,index=0):
    df = df[df['City'] == name]

    if year == 0:
        df = df[df['City'] == name]

    elif year == year:
        df = df[df['Year'] == year]

    if index == 0:
        df
    elif index == index:
        df = df[index]
    return df

df_original = pd.read_csv("data/qol_indices.csv", index_col=0)
df=df_original.copy()
df_coord = pd.read_csv('data/coordinates.csv', index_col=0)

################# -- map figure -- #############################################


fig_map = go.Figure(data=go.Scattergeo(
        lon = df_coord['lng'],
        lat = df_coord['lat'],
        text = df_coord.index.values,
        mode = 'markers',
        marker_color = "red",
        ))

fig_map.update_layout( margin = dict(l=0, r=0, t=0, b=0),
                       geo=dict(showframe=False, showcoastlines=False, showcountries=True, countrywidth=0.1))

df_plot = filtering(df, 'Abu Dhabi, United Arab Emirates')
df_plot = df_plot.sort_values("Year")

sca_poll = go.Scatter(x=df_plot["Year"],y=df_plot["Pollution Index"])
sca_costs = go.Scatter(x=df_plot["Year"],y=df_plot["Cost of Living Index"])
sca_health = go.Scatter(x=df_plot["Year"],y=df_plot["Health Care Index"])
sca_safety = go.Scatter(x=df_plot["Year"],y=df_plot["Safety Index"])

fig_lines = make_subplots(rows=2, cols=2)
fig_lines.add_trace(
    sca_poll,
    row=1, col=1
)
fig_lines.add_trace(
    sca_costs,
    row=1, col=2
)
fig_lines.add_trace(
    sca_health,
    row=2, col=1
)
fig_lines.add_trace(
    sca_safety,
    row=2, col=2
)

####################################################################################
################# -- template start -- #############################################
####################################################################################

# load external CSS
external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.title = 'Find Your Paradise'

# Bootstrap CSS
# app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

app.layout = html.Div(
    html.Div([
        html.Div([
            html.H1(children = 'Title Placeholder')
        ], id = 'title-div', style = {'margin-left': 20}),

    html.Div([
        html.Div([

            html.Div([
            html.H6(children = 'Safety')
            ], id = 'first-preference-title', className = 'row'),

            html.Div([
                dcc.Slider(
                    id='slider-safety',
                    min = 0,
                    max = 1,
                    step = 0.1,
                    value = .5
                )
            ], id = 'first-preference', className = 'row', style = {'margin-left': 10}),

            html.Div([
                html.H6(children = 'Health Care')
            ], id = 'second-preference-title', className = 'row'),

            html.Div([
                dcc.Slider(
                    id='slider-health',
                    min = 0,
                    max = 1,
                    step = 0.1,
                    value = .5
                )
            ], id = 'second-preference', className = 'row', style = {'margin-left': 10}),

            html.Div([
                html.H6(children = 'Cost of Living')
            ], id = 'third-preference-title', className = 'row'),

            html.Div([
                dcc.Slider(
                    id='slider-costs',
                    min = 0,
                    max = 1,
                    step = 0.1,
                    value = .5
                )
            ], id = 'third-preference', className = 'row', style = {'margin-left': 10}),

            html.Div([
                html.H6(children = 'Pollution')
            ], id = 'fourth-preference-title', className = 'row'),

            html.Div([
                dcc.Slider(
                    id='slider-pollution',
                    min = 0,
                    max = 1,
                    step = 0.1,
                    value = .5
                )
            ], id = 'fourth-preference', className = 'row', style = {'margin-left': 10}),
        ], id = 'preferences-div', className = 'three columns'),

        html.Div([

            dcc.Graph(id = 'fig-map',
                    figure = fig_map)
        ], id = 'map-div', className = 'nine columns'),

    ], id = 'preferences-map', className = 'twelve columns', style = {'margin-left': 20,
                                                                      'margin-right':20}),
    html.Div([
        html.H6(children = 'The analytically best place on earth for you is: '),
        html.Div([
            dcc.Graph(id = 'fig-lines',
                      figure = fig_lines)

        ], id = 'first-right-graph', className = 'twelve columns'),

    ], id = 'map-subtext', className = 'twelve columns'),
    ], id = 'outer-div')
)

####################################################################################
################# -- template end -- #############################################
####################################################################################


####################################################################################
################# -- callbacks start -- #############################################
####################################################################################

################# -- map callback -- #############################################
@app.callback(
    Output('fig-map', 'figure'),
    [Input('slider-safety', 'value'),
     Input('slider-health', 'value'),
     Input('slider-costs', 'value'),
     Input('slider-pollution', 'value'),
     ])
def update_map(a,b,c,d):
    df = df_original.copy()
    df["final_score"] = a * df["Safety Index"] + b * df["Health Care Index"] + c * df["Cost of Living Index"] + d * df["Pollution Index"]
    df_cy = df[df["Year"] == 2019]
    df_cy = df_cy.sort_values("final_score", ascending=False)

    top_five = df_cy.head(n=10)
    coord_tf = df_coord[df_coord.index.isin(top_five["City"].values)]

    fig_map = go.Figure(data=go.Scattergeo(
        lon = coord_tf['lng'],
        lat = coord_tf['lat'],
        text = coord_tf.index.values,
        mode = 'markers',
        marker_color = "red",
        ))

    fig_map.update_layout(margin = dict(l=0, r=0, t=0, b=0),dragmode=False ,
                          geo=dict(showframe=False, showcoastlines=False, showcountries=True, countrywidth=0.1))

    return fig_map

################# -- safety callback -- #############################################
@app.callback(
    Output('fig-lines', 'figure'),
    [Input('slider-safety', 'value'),
     Input('slider-health', 'value'),
     Input('slider-costs', 'value'),
     Input('slider-pollution', 'value'),
     ])
def update_lines(a,b,c,d):
    df["final_score"] = a * df["Safety Index"] + b * df["Health Care Index"] + c * df["Cost of Living Index"] + d * df["Pollution Index"]
    df_temp = df.sort_values("final_score", ascending=False)
    top_five = df_temp[df_temp["Year"] == 2019].head(n=5)
    top_five = top_five.sort_values("final_score", ascending=False)
    top_five = df_temp[df_temp["City"].isin(top_five["City"].values)]

    top_five = top_five.sort_values("Year")
    cities = np.unique(top_five["City"].values)
    fig_lines = make_subplots(rows=2, cols=2)
    colors = ['blue', 'cyan', 'magenta', 
        "#636efa",  "#00cc96",  "#EF553B", 'brown']

    color_city = 0
    for city in cities:

        year = top_five[top_five["City"] == city]["Year"]
        y_poll = top_five[top_five["City"] == city]["Pollution Index"]
        y_safe = top_five[top_five["City"] == city]["Safety Index"]
        y_heal = top_five[top_five["City"] == city]["Health Care Index"]
        y_cost = top_five[top_five["City"] == city]["Cost of Living Index"]

        fig_lines.add_trace(
            go.Scatter(
                x = year,
                y = y_poll,
                name = city,
                showlegend = False,
                mode='lines',
                marker_color = colors[color_city]
            ),
            row=1, col=1
        )
        fig_lines.add_trace(
            go.Scatter(
                x=year,
                y=y_safe,
                name=city,
                showlegend=False,
                mode='lines',
                marker_color = colors[color_city]
            ),
            row=2, col=2
        )
        fig_lines.add_trace(
            go.Scatter(
                x=year,
                y=y_heal,
                name=city,
                showlegend=False,
                mode='lines',
                marker_color = colors[color_city]
            ),
            row=2, col=1
        )
        fig_lines.add_trace(
            go.Scatter(
                x=year,
                y=y_cost,
                name=city,
                mode='lines',
                marker_color = colors[color_city]
            ),
            row=1, col=2
        )
        color_city += 1

        fig.update_layout()
    return fig_lines

if __name__ == '__main__':
    app.run_server(debug = True)
