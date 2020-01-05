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

df_original = pd.read_csv("data/joined.csv", index_col=0)
df = df_original.copy()
clickCount = 0
df_coord = pd.read_csv('data/coordinates.csv', index_col=0)

#### stacked chart ####
trace1 = go.Bar(y = df['City'],
                x = df['Safety Index'],
                name = 'Safety',
                orientation = 'h')
trace2 = go.Bar(y = df['City'],
                x = df['Health Care Index'],
                name = 'Health',
                orientation = 'h')
trace3 = go.Bar(y = df['City'],
                x = df['Cost of Living Index'],
                name = 'Cost of Living',
                orientation = 'h')
trace4 = go.Bar(y = df['City'],
                x = df['Pollution Index'],
                name = 'Pollution',
                orientation = 'h')

data = [trace1, trace2, trace3, trace4]

layout = go.Layout(barmode='stack', xaxis_tickangle=-45, legend_orientation = 'h')
fig_stacked = go.Figure(data, layout)

################# -- map figure -- #############################################

fig_map = go.Figure(data=go.Scattergeo(
        lon = df_coord['lng'],
        lat = df_coord['lat'],
        text = df_coord.index.values,
        mode = 'markers',
        marker_color = "blue",
        marker_size = 5
        ))

fig_map.update_layout( margin = dict(l=0, r=0, t=0, b=0),
                       geo=dict(showframe=False, showcoastlines=False, showcountries=True, countrywidth=0.1))

df_plot = filtering(df, 'Abu Dhabi, United Arab Emirates')
df_plot = df_plot.sort_values("Year")

sca_poll = go.Scatter(x=df_plot["Year"],y=df_plot["Pollution Index"])
sca_costs = go.Scatter(x=df_plot["Year"],y=df_plot["Cost of Living Index"])
sca_health = go.Scatter(x=df_plot["Year"],y=df_plot["Health Care Index"])
sca_safety = go.Scatter(x=df_plot["Year"],y=df_plot["Safety Index"])

fig_lines = make_subplots(rows=1, cols=4,subplot_titles=('Clean Air', 'Cheap Living','Health', 'Safety'))
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
    row=1, col=3
)
fig_lines.add_trace(
    sca_safety,
    row=1, col=4
)

####################################################################################
################# -- template start -- #############################################
####################################################################################

# load external CSS
external_ss = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
app = dash.Dash(__name__, external_stylesheets=external_ss)

app.title = 'Find Your Paradise'

# Bootstrap CSS
# app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

app.layout = html.Div([

        # title div
        html.Div([
            # large title
            html.H1(children = 'Title Placeholder')
        ], id = 'title-div', className = 'row justify-content-md-center',
                 style = {'padding':15, 'margin-bottom':0}),

    # first container holding preferences and map
    html.Div([

        # div holding preferences
        html.Div([
            html.Div(id="df-storage", style={"display": "None"}),
            html.Div([
                html.H2(children = 'Choose your preferences')], style = {'margin-bottom':10,'margin-top':10,'margin-right':10,'margin-left':10, }),
            html.Div([
                html.H5(children = 'Safety')
            ], id = 'first-preference-title', className = 'col'),

            html.Div([
                dcc.Slider(
                    id='slider-safety',
                    min = 0,
                    max = 1,
                    step = 0.1,
                    value = .5
                )
            ], id = 'first-preference', className = 'col', style = {'margin-bottom':10}),

            html.Div([
                html.H5(children = 'Health Care')
            ], id = 'second-preference-title', className = 'col'),

            html.Div([
                dcc.Slider(
                    id='slider-health',
                    min = 0,
                    max = 1,
                    step = 0.1,
                    value = .5
                )
            ], id = 'second-preference', className = 'col', style = {'margin-bottom':10}),

            html.Div([
                html.H5(children = 'Cheap Living')
            ], id = 'third-preference-title', className = 'col'),

            html.Div([
                dcc.Slider(
                    id='slider-costs',
                    min = 0,
                    max = 1,
                    step = 0.1,
                    value = .5
                )
            ], id = 'third-preference', className = 'col', style = {'margin-bottom':10}),

            html.Div([
                html.H5(children = 'Clean Air')
            ], id = 'fourth-preference-title', className = 'col'),

            html.Div([
                dcc.Slider(
                    id='slider-pollution',
                    min = 0,
                    max = 1,
                    step = 0.1,
                    value = .5,
                )
            ], id = 'fourth-preference', className = 'col',  style = {'margin-bottom':10}),

            html.Button('Show All', id='show-all'),

        ], id = 'preferences-div', className = 'col-3 shadow p-4 mb-5 bg-white rounded', style = {'margin-right':20}),

        # map div
        html.Div([
            dcc.Graph(id = 'fig-map',
                    figure = fig_map)
        ], id = 'map-div', className = 'col auto shadow p-8 mb-5 bg-white rounded'),
        ], id = 'first-container', className = 'row', style = {'margin-top':0}),

        html.Div([
            dcc.Graph(id = 'fig-lines',
                    figure = fig_lines)
        ], id = 'chart-div', className = 'col auto shadow p-4 mb-5 bg-white rounded'),

        html.Div([
            html.Div([
                dcc.Graph(id="fig-temp", config={'displayModeBar': False})
            ], className = 'col shadow p-4 mb-5 bg-white rounded', style = {'margin-right':20}),
            html.Div([
                dcc.Graph(id="fig-sun", config={'displayModeBar': False})
            ], className = 'col shadow p-4 mb-5 bg-white rounded', style = {'margin-right':20}),
            html.Div([
                dcc.Graph(id="fig-rain", config={'displayModeBar': False})
            ], className = 'col shadow p-4 mb-5 bg-white rounded')], className="row"),

        html.Div([
            html.Div([
                dcc.Graph(id = 'stacked-graph', figure = fig_stacked)
            ], className = 'col shadow p-4 mb-5 bg-white rounded', id = 'stacked-bar-div')
        ])

    ], id = 'outer-div', className = 'container')

####################################################################################
################# -- template end -- #############################################
####################################################################################


####################################################################################
################# -- callbacks start -- #############################################
####################################################################################

################# -- df storage callback -- #############################################
@app.callback(
    Output('df-storage', 'children'),
    [Input('slider-safety', 'value'),
     Input('slider-health', 'value'),
     Input('slider-costs', 'value'),
     Input('slider-pollution', 'value'),
     Input('show-all', 'n_clicks'),
     ])
def update_df(a,b,c,d,clicks):
    df = df_original.copy()
    df["final_score"] = a * df["Safety Index"] + b * df["Health Care Index"] + c * df["Cost of Living Index"] + d * df["Pollution Index"]
    df_cy = df[df["Year"] == 2019]
    df_cy = df_cy.sort_values("final_score", ascending=False)
    top_ten = df[df["City"].isin(df_cy.head(n=10)["City"].values)]
    global clickCount
    if clicks != None:
        if (clicks > clickCount):
            top_ten = df
            clickCount = clicks


    return top_ten.to_json()

################# -- map callback -- #############################################
@app.callback(
    Output('fig-map', 'figure'),
    [Input("df-storage", "children")])
def update_map(top_ten):
    top_ten = pd.read_json(top_ten)

    coord_tf = df_coord[df_coord.index.isin(top_ten["City"].values)]

    fig_map = go.Figure(data=go.Scattergeo(
        lon = coord_tf['lng'],
        lat = coord_tf['lat'],
        text = coord_tf.index.values,
        mode = 'markers',
        marker_color = "blue",
        marker_size = 10
        ))

    fig_map.update_layout(margin = dict(l=0, r=0, t=0, b=0),dragmode=False ,
                          geo=dict(showframe=False, showcoastlines=False, showcountries=True, countrywidth=0.1))

    return fig_map

################# -- bars callback -- #############################################
@app.callback(
    Output('fig-lines', 'figure'),
    [Input("df-storage", "children"),
     Input("fig-map","clickData")])
def update_bars(top_ten,clickData):
    top_ten = pd.read_json(top_ten)
    if clickData != None:
        top_one = df[df["City"] == clickData["points"][0]["text"]]
        top_one = top_one.sort_values("Year")

    else:
        top_one_city = top_ten.sort_values("final_score", ascending=False).head(n=1)["City"]
        top_one = top_ten[top_ten["City"] == top_one_city.values[0]]

    city = np.unique(top_one["City"].values)[0]
    fig_lines = make_subplots(rows=1, cols=4,subplot_titles=('Clean Air', 'Cheap Living','Health', 'Safety'))
    colors = ['blue', 'cyan', 'magenta',
        "#636efa",  "#00cc96",  "#EF553B", 'brown']

    color_city = 0

    year = top_one["Year"]
    y_poll = top_one["Pollution Index"]
    y_safe = top_one["Safety Index"]
    y_heal = top_one["Health Care Index"]
    y_cost = top_one["Cost of Living Index"]

    fig_lines.add_trace(
        go.Bar(
            x = year,
            y = y_poll,
            name = city,
            showlegend = False,
            marker_color = colors[color_city]
        ),
        row=1, col=1
    )
    fig_lines.add_trace(
        go.Bar(
            x=year,
            y=y_safe,
            name=city,
            showlegend=False,
            marker_color = colors[color_city]
        ),
        row=1, col=4
    )
    fig_lines.add_trace(
        go.Bar(
            x=year,
            y=y_heal,
            name=city,
            showlegend=False,
            marker_color = colors[color_city]
        ),
        row=1, col=3
    )
    fig_lines.add_trace(
        go.Bar(
            x=year,
            y=y_cost,
            name=city,
            marker_color = colors[color_city]
        ),
        row=1, col=2
    )
    fig_lines.update_layout(plot_bgcolor="white",
                            margin=dict(t=110,b=15,r=15,l=15),
                            title=dict(text="Indicators of " + city, y=0.98, x=0.5, xanchor="center", yanchor="top"),
                            showlegend=False,
                            )
    return fig_lines

################# -- sun callback -- #############################################
@app.callback(
    Output('fig-sun', 'figure'),
    [Input("df-storage", "children"),
     Input("fig-map","clickData")])
def update_sun(top_ten,clickData):
    top_ten = pd.read_json(top_ten)
    if clickData != None:
        top_one = df[df["City"] == clickData["points"][0]["text"]]
        top_one = top_one.sort_values("Year")

    else:
        top_one = top_ten.sort_values("final_score", ascending=False).head(n=1)

    city = np.unique(top_one["City"].values)[0]

    df_sun = pd.read_csv("data/sun.csv")
    top_sun = df_sun.loc[df_sun["real_city"] == city]
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    data = []
    for i in range(1,len(months) + 1):
        x = [i for j in range(0, top_sun[months[i-1]].values[0])]
        y = [j + 0.5 + j*0.03 for j in range(0, top_sun[months[i-1]].values[0])]
        data.append(go.Scatter(x=x,y=y,mode="markers", marker=dict(symbol=18, color="yellow", size=11), hoverinfo="none"))
        data.append(go.Scatter(x=x,y=y,mode="markers", marker=dict(symbol="circle", color="yellow", size=10), hoverinfo="none"))

    layout=go.Layout(showlegend=False, plot_bgcolor="white", margin=dict(t=50,b=5,r=5,l=5),
            xaxis=dict(showgrid=False, zeroline=False, ticktext=months, tickvals=[1,2,3,4,5,6,7,8,9,10,11,12]),title=dict(text="Sunny hours per day in " + city),
            yaxis=dict(showgrid=False, zeroline=False, range=[0,18]))

    fig_sun = go.Figure(data, layout)
    return fig_sun

################# -- rain callback -- #############################################
@app.callback(
    Output('fig-rain', 'figure'),
    [Input("df-storage", "children"),
     Input("fig-map","clickData")])
def update_rain(top_ten,clickData):
    top_ten = pd.read_json(top_ten)
    if clickData != None:
        top_one = df[df["City"] == clickData["points"][0]["text"]]
        top_one = top_one.sort_values("Year")

    else:
        top_one = top_ten.sort_values("final_score", ascending=False).head(n=1)
    city = np.unique(top_one["City"].values)[0]

    df_rain = pd.read_csv("data/rain.csv")
    top_rain = df_rain.loc[df_rain["real_city"] == city]

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    data = []
    for i in range(1,len(months) + 1):
        x = [i for j in range(0, top_rain[months[i-1]].values[0])]
        y = [j + 0.5 + j*0.03 for j in range(0, top_rain[months[i-1]].values[0])]
        data.append(go.Scatter(x=x,y=y,mode="markers", marker=dict(symbol="circle", color="blue", size=11), hoverinfo="none"))

    layout=go.Layout(showlegend=False, plot_bgcolor="white", margin=dict(t=50,b=5,r=5,l=5),
            xaxis=dict(showgrid=False, zeroline=False, ticktext=months, tickvals=[1,2,3,4,5,6,7,8,9,10,11,12]),title=dict(text="Rainy days in " + city),
            yaxis=dict(showgrid=False, zeroline=False, range=[0,30]))

    fig_rain = go.Figure(data, layout)
    return fig_rain

################# -- temperature callback -- #############################################
@app.callback(
    Output('fig-temp', 'figure'),
    [Input("df-storage", "children"),
     Input("fig-map","clickData")])
def update_temp(top_ten,clickData):
    top_ten = pd.read_json(top_ten)
    if clickData != None:
        top_one = df[df["City"] == clickData["points"][0]["text"]]
        top_one = top_one.sort_values("Year")

    else:
        top_one = top_ten.sort_values("final_score", ascending=False).head(n=1)
    city = np.unique(top_one["City"].values)[0]

    df_tempe = pd.read_csv("data/temperature.csv")
    top_temp = df_tempe.loc[df_tempe["real_city"] == city]

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    data = []
    x = [j for j in range(1, 13)]
    y = top_temp[months].values[0]
    data.append(go.Scatter(x=x,y=y ,marker=dict(symbol="circle", color="gray", size=8)))

    layout=go.Layout(showlegend=False, plot_bgcolor="white", margin=dict(t=50,b=5,r=5,l=5),
            xaxis=dict(showgrid=False, zeroline=False, ticktext=months, tickvals=[1,2,3,4,5,6,7,8,9,10,11,12]),title=dict(text="Average Temperature in " + city),
            yaxis=dict(showgrid=False, zeroline=False))

    fig_temp = go.Figure(data, layout)
    return fig_temp


################# -- stacked bar callback -- #############################################
@app.callback(
    Output('stacked-graph','figure'),
    [Input("df-storage", "children")])
def update_bars(top_ten):
    top_ten = pd.read_json(top_ten)

    top_ten = top_ten.sort_values("final_score")
    top_ten_cy = top_ten[top_ten["Year"] == 2019]

    trace1 = go.Bar(y = top_ten_cy['City'],
                    x = top_ten_cy['Safety Index'],
                    name = 'Safety',
                    orientation = 'h')
    trace2 = go.Bar(y = top_ten_cy['City'],
                    x = top_ten_cy['Health Care Index'],
                    name = 'Health',
                    orientation = 'h')
    trace3 = go.Bar(y = top_ten_cy['City'],
                    x = top_ten_cy['Cost of Living Index'],
                    name = 'Cost of Living',
                    orientation = 'h')
    trace4 = go.Bar(y = top_ten_cy['City'],
                    x = top_ten_cy['Pollution Index'],
                    name = 'Pollution',
                    orientation = 'h')

    data = [trace1, trace2, trace3, trace4]

    layout=go.Layout(showlegend=False, plot_bgcolor="white", margin=dict(t=50,b=5,r=5,l=5), barmode='stack', xaxis_tickangle=-45, legend_orientation = 'h',
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False))
    fig_stacked = go.Figure(data, layout)
    return fig_stacked



if __name__ == '__main__':
    app.run_server(debug = True)
