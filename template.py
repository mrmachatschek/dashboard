import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
from dash.dependencies import Input, Output, State

def city_only(cities):
    newlist = []
    for city in cities:
        city = city.split(',')[0]
        newlist.append(city)
    return newlist

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

df_original = pd.read_csv("data/joined_continent.csv", index_col=0)
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
        marker_color = "#0091D5",
        marker_size = 7
        ))

fig_map.update_layout(margin = dict(l=0, r=0, t=0, b=0),
                        dragmode=False,
                        geo=dict(
                            showland = True,
                            scope = "world", # can be updated when continent is
                            landcolor = "#DADADA",
                            subunitcolor = "rgb(255, 255, 255)",
                            coastlinecolor = "rgb(255, 255, 255)",
                            countrycolor = "rgb(255, 255, 255)",
                            showlakes = True,
                            lakecolor = "rgb(255, 255, 255)",
                            showsubunits = True,
                            showcountries = True,
                            framecolor = "rgb(255, 255, 255)",
                            #resolution = 50,
                            countrywidth=0.1,
                        ))

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



app.layout = html.Div([

    html.Div(id="df-storage", style={"display": "None"}),

    # title div
    html.Div([
        html.H1(children = 'Title Placeholder')
        ], id = 'title-div', className = 'row justify-content-md-center', style = {'padding':15, 'margin-bottom':0}),

    # first container holding first page
    html.Div([
        # div holding preferences
        html.Div([
            html.Div([
                html.Div([
                    html.H2(children = 'Choose your preferences')], style = {'margin-bottom':5,'margin-top':10,'margin-right':10,'margin-left':10, }),
                    html.Div(["Choose the importance of the following factors. You can limit results to a certain continent."], style = {'margin-bottom':10,'margin-top':10,'margin-right':10,'margin-left':10 }),

                html.Div([
                    dcc.Dropdown(
                    id='dropdown-continent',
                    options=[
                        {'label':'Asia','value':'Asia'},
                        {'label':'Oceania','value':'Oceania'},
                        {'label':'North America','value':'North America'},
                        {'label':'Europe','value':'Europe'},
                        {'label':'South America','value':'South America'},
                        {'label':'Africa','value':'Africa'}
                    ],
                    value="Continent",
                    placeholder="Filter by Continent",
                    )
                ], className="col",style = {'margin-bottom':15}),

                html.Div([
                    html.H5(children = 'Safety')
                ], id = 'first-preference-title', className = 'col'),

                html.Div([
                    dcc.Slider(
                        id='slider-safety',
                        min = 0,
                        max = 1,
                        step = 0.1,
                        value = .5,
                        marks ={0:"",1:""}
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
                        value = .5,
                        marks ={0:"",1:""}
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
                        value = .5,
                        marks ={0:"",1:""}
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
                        marks={
                                0:{'label': 'not important', "style":{"margin-left":21}},
                                1: {'label': 'important'},
                            }
                    )
                ], id = 'fourth-preference', className = 'col', style = {'margin-bottom':10}),


                html.Div([html.Button('Show All', id='show-all')], style={"display":"None"}),
            ], id = 'preferences-div', className = 'col-3 shadow p-4 mr-4 mb-5 bg-white rounded'),
            html.Div([
                html.Div([html.Div([html.H4("Your city is")],),html.Div([html.H4("...")],id="box-city", style={"font-size":25, "font-weight":"bold"})], className = 'h-auto shadow mb-3 p-4 bg-white rounded'),
                html.Div([html.Div([html.H4("Average Temperature")]),html.Div([html.H4("...")], id="box-temp", style={"font-size":30, "font-weight":"bold"})], className = 'h-auto shadow mb-3 p-4 bg-white rounded'),
                html.Div([html.Div([html.H4("Rainy days per year")]),html.Div([html.H4("...")], id="box-rain", style={"font-size":30, "font-weight":"bold"})], className = 'h-auto shadow mb-3 p-4 bg-white rounded'),
                html.Div([html.Div([html.H4("Sunny hours per day")]),html.Div([html.H4("...")], id="box-sun", style={"font-size":30, "font-weight":"bold"})], className = 'h-auto shadow mb-3 p-4 bg-white rounded'),

            ],className="col mr-2"),

            # map div
            html.Div([
                dcc.Graph(id = 'fig-map',
                        figure = fig_map)
            ], id = 'map-div', className = 'col-7 shadow mb-5 bg-white rounded'),
        ], id = 'second-main-row', className = 'row ml-2 mr-2'),

        html.Div([
            dcc.Graph(id = 'fig-lines',figure = fig_lines,style={'width': '100%'})
        ],className="row shadow p-4 mb-5 mr-2 ml-2 bg-white rounded"),

        html.Div([
            html.Div([
                dcc.Graph(id = 'stacked-graph', figure = fig_stacked)
            ], className = 'col-4 shadow p-4 mb-4 mr-4 bg-white rounded', id = 'stacked-bar-div'),
            html.Div([
                dcc.Graph(id = 'dots-graph')
            ], className="col  shadow p-4 mb-4 bg-white rounded")
        ], id = 'chart-div', className = 'row ml-2 mr-2'),

        html.Div([
            html.Div([
                dcc.Graph(id="fig-temp", config={'displayModeBar': False})
            ], className = 'col shadow p-4 mb-5 mr-4 bg-white rounded'),
            html.Div([
                dcc.Graph(id="fig-sun", config={'displayModeBar': False})
            ], className = 'col shadow p-4 mb-5 mr-4 bg-white rounded'),
            html.Div([
                dcc.Graph(id="fig-rain", config={'displayModeBar': False})
            ], className = 'col shadow p-4 mb-5 bg-white rounded')], className="row mr-2 ml-2"),
    ], id = 'outer-div', className = 'mb-2 mr-2 ml-2 p-1')
],className="bg-light")

####################################################################################
################# -- template end -- #############################################
####################################################################################


####################################################################################
################# -- callbacks start -- #############################################
####################################################################################

################# -- continent callback -- #############################################
@app.callback(
    Output('fig-map', 'clickData'),
    [Input('dropdown-continent', 'value')])
def reset_clickData(n_clicks):
    return None


@app.callback(
    Output('dropdown-continent', 'value'),
    [Input('show-all', 'n_clicks')])
def cleardrop(clicks):
    if clicks != None:
        return None
################# -- df storage callback -- #############################################
@app.callback(
    Output('df-storage', 'children'),
    [Input('slider-safety', 'value'),
     Input('slider-health', 'value'),
     Input('slider-costs', 'value'),
     Input('slider-pollution', 'value'),
     Input('dropdown-continent', 'value'),
     ])
def update_df(a,b,c,d,continent):
    global df
    df = df_original.copy()
    global selected
    selected = continent
    df["final_score"] = a * df["Safety Index"] + b * df["Health Care Index"] + c * df["Cost of Living Index"] + d * df["Pollution Index"]
    df["saf"] = a
    df["hea"] = b
    df["cos"] = c
    df["pol"] = d

    df_cy = df[df["Year"] == 2019]
    df_cy = df_cy.sort_values("final_score", ascending=False)
    top_ten = df[df["City"].isin(df_cy.head(n=10)["City"].values)]

    if (continent!= None):
        top_ten = df[df["Continent"] == continent]
        df = top_ten

    return top_ten.to_json()

################# -- map callback -- #############################################
@app.callback(
    Output('fig-map', 'figure'),
    [Input("df-storage", "children")])
def update_map(top_ten):
    global df
    top_ten = pd.read_json(top_ten)
    top_ten = top_ten.sort_values("final_score", ascending=False)
    top_ten["place"] = 7
    city = top_ten.head(1).iloc[0]["City"]
    print(city)
    top_ten.loc[top_ten["City"]==city,"place"] = 2
    coord_tf = df_coord[df_coord.index.isin(top_ten["City"].values)]

    coord_tf = pd.merge(coord_tf, top_ten, how='right',left_on="City", right_on="City")

    fig_map = go.Figure(data=go.Scattergeo(
        lon = coord_tf['lng'],
        lat = coord_tf['lat'],
        text = coord_tf['City'],
        mode = 'markers',
        marker = dict(
            size = 7,
            autocolorscale =False,
            colorscale = 'Rainbow',
            cmin = 0,
            color = coord_tf['place'], #coord_tf["final_score"]
            cmax = 8,

        )))

    fig_map.update_layout(margin = dict(l=0, r=0, t=0, b=0),
                        dragmode=False ,
                        geo=dict(
                            showland = True,
                            scope = "world", # can be updated when continent is
                            landcolor = "#DADADA",
                            subunitcolor = "rgb(255, 255, 255)",
                            coastlinecolor = "rgb(255, 255, 255)",
                            countrycolor = "rgb(255, 255, 255)",
                            showlakes = True,
                            lakecolor = "rgb(255, 255, 255)",
                            showsubunits = True,
                            showcountries = True,
                            framecolor = "rgb(255, 255, 255)",
                            #resolution = 50,
                            countrywidth=0.1,
                        ))

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

    year = top_one["Year"].copy()
    year.sort_values(inplace=True)

    top_one["Pollution Change"] = 0
    top_one["Safety Change"] = 0
    top_one["Health Care Change"] = 0
    top_one["Cost of Living Change"] = 0

    prev = 0
    for i in year:
        if prev != 0:
            top_one.loc[top_one["Year"] == i,"Pollution Change"] = (((
                top_one.loc[top_one["Year"] == i].iloc[0]["Pollution Index"] -
                top_one.loc[top_one["Year"] == prev].iloc[0]["Pollution Index"])*100)/
                top_one.loc[top_one["Year"] == prev].iloc[0]["Pollution Index"])

            top_one.loc[top_one["Year"] == i,"Safety Change"] = (((
                top_one.loc[top_one["Year"] == i].iloc[0]["Safety Index"] -
                top_one.loc[top_one["Year"] == prev].iloc[0]["Safety Index"])*100)/
                top_one.loc[top_one["Year"] == prev].iloc[0]["Safety Index"])

            top_one.loc[top_one["Year"] == i,"Health Care Change"] = (((
                top_one.loc[top_one["Year"] == i].iloc[0]["Health Care Index"] -
                top_one.loc[top_one["Year"] == prev].iloc[0]["Health Care Index"])*100)/
                top_one.loc[top_one["Year"] == prev].iloc[0]["Health Care Index"])

            top_one.loc[top_one["Year"] == i,"Cost of Living Change"] = (((
                top_one.loc[top_one["Year"] == i].iloc[0]["Cost of Living Index"] -
                top_one.loc[top_one["Year"] == prev].iloc[0]["Cost of Living Index"])*100)/
                top_one.loc[top_one["Year"] == prev].iloc[0]["Cost of Living Index"])
        prev = i

    y_poll = top_one["Pollution Change"]
    y_safe = top_one["Safety Change"]
    y_heal = top_one["Health Care Change"]
    y_cost = top_one["Cost of Living Change"]
    year = top_one["Year"]

    fig_lines.add_trace(
        go.Bar(
            x = year,
            y = y_poll,
            name = city,
            showlegend = False,
            marker_color = 'rgb(118,0,29)' #use this for negative change
        ),
        row=1, col=1
    )
    fig_lines.add_trace(
        go.Bar(
            x=year,
            y=y_safe,
            name=city,
            showlegend=False,
            marker_color = 'rgb(118,0,29)'
        ),
        row=1, col=4
    )
    fig_lines.add_trace(
        go.Bar(
            x=year,
            y=y_heal,
            name=city,
            showlegend=False,
            marker_color = '#0091d5' # use this for positive change
        ),
        row=1, col=3
    )
    fig_lines.add_trace(
        go.Bar(
            x=year,
            y=y_cost,
            name=city,
            marker_color = '#0091d5'
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
    top_ten = top_ten.sort_values("final_score")
    top_ten_cy = top_ten[top_ten["Year"] == 2019]

    if clickData != None:
        top_one = df[df["City"] == clickData["points"][0]["text"]]
        top_one = top_one.sort_values("Year")

    else:
        top_one = top_ten.sort_values("final_score", ascending=False).head(n=1)

    cities = np.unique(top_ten_cy["City"].values)
    df_sun = pd.read_csv("data/sun.csv")
    df_sun = df_sun[df_sun["real_city"].isin(cities)]

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    data = []
    y = city_only(df_sun['real_city'].values)

    for i in range(1,len(months) + 1):
        x = [i for j in range(1,len(df_sun['real_city'].values) + 1)]
        size = df_sun[months[i-1]] #scaling the scatter dots

        data.append(go.Scatter(x=x, y = y, mode="markers", marker=dict(symbol=18, color="#FFAE00", size=size*1.5), hoverinfo="none"))
        data.append(go.Scatter(x=x, y = y, mode="markers", marker=dict(symbol="circle", color="#FFAE00", size=size,
                                                                       line=dict(width=1,color='#FFAE00')), hoverinfo="none"))



    layout=go.Layout(showlegend=False, plot_bgcolor="white", margin=dict(t=50,b=5,r=5,l=5),
            xaxis=dict(showgrid=False, zeroline=False, ticktext=months, tickvals=[1,2,3,4,5,6,7,8,9,10,11,12]),title=dict(text="Daily Sun Hours by City and Month"),
            yaxis=dict(showgrid=False, zeroline=False))

    fig_sun = go.Figure(data, layout)
    return fig_sun

################# -- rain callback -- #############################################
@app.callback(
    Output('fig-rain', 'figure'),
    [Input("df-storage", "children"),
     Input("fig-map","clickData")])
def update_rain(top_ten,clickData):
    top_ten = pd.read_json(top_ten)
    top_ten = top_ten.sort_values("final_score")
    top_ten_cy = top_ten[top_ten["Year"] == 2019]

    if clickData != None:
        top_one = df[df["City"] == clickData["points"][0]["text"]]
        top_one = top_one.sort_values("Year")

    else:
        top_one = top_ten.sort_values("final_score", ascending=False).head(n=1)

    cities = np.unique(top_ten_cy["City"].values)

    df_rain = pd.read_csv("data/rain.csv")
    df_rain = df_rain[df_rain["real_city"].isin(cities)]

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    data = []
    y = city_only(df_rain['real_city'].values)

    for i in range(1,len(months) + 1):
        x = [i for j in range(1,len(df_rain['real_city'].values) + 1)]
        size = df_rain[months[i-1]]

        data.append(go.Scatter(x=x, y = y, mode="markers", marker=dict(symbol="circle", color="#0091D5", size=size), hoverinfo="none"))

    layout=go.Layout(showlegend=False, plot_bgcolor="white", margin=dict(t=50,b=5,r=5,l=5),
            xaxis=dict(showgrid=False, zeroline=False, ticktext=months, tickvals=[1,2,3,4,5,6,7,8,9,10,11,12]),title=dict(text="Rainy Days by City and Month"),
            yaxis=dict(showgrid=False, zeroline=False))

    fig_rain = go.Figure(data, layout)
    return fig_rain

################# -- temperature callback -- #############################################
@app.callback(
    Output('fig-temp', 'figure'),
    [Input("df-storage", "children"),
     Input("fig-map","clickData")])
def update_temp(top_ten,clickData):
    top_ten = pd.read_json(top_ten)
    top_ten = top_ten.sort_values("final_score")
    top_ten_cy = top_ten[top_ten["Year"] == 2019]

    if clickData != None:
        top_one = df[df["City"] == clickData["points"][0]["text"]]
        top_one = top_one.sort_values("Year")

    else:
        top_one = top_ten.sort_values("final_score", ascending=False).head(n=1)

    cities = np.unique(top_ten_cy["City"].values)

    df_temp = pd.read_csv("data/temperature.csv")
    df_temp = df_temp[df_temp['real_city'].isin(cities)]


    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    x = [j for j in range(1, 13)]
    y = city_only(df_temp['real_city'].values)
    z = df_temp[months].values


    annotations = go.Annotations()
    for n, row in enumerate(z):
        for m, val in enumerate(row):
            annotations.append(go.Annotation(text=str(z[n][m]), x=x[m], y=y[n], font=dict(color = 'white'),
                                         xref='x1', yref='y1', showarrow=False))

    layout=go.Layout(showlegend=False, plot_bgcolor="white", margin=dict(t=50,b=5,r=5,l=5),
            xaxis=dict(showgrid=False, zeroline=False, ticktext=months, tickvals=[1,2,3,4,5,6,7,8,9,10,11,12]),title=dict(text="Average Temperature by City and Month"),
            yaxis=dict(showgrid=False, zeroline=False))

    fig_temp = go.Figure(data = go.Heatmap(z = z, x = x, y = y, xgap = 1, ygap = 1, colorscale = 'RdBu',
                                           reversescale=True, colorbar=dict(thickness = 10, xpad = 0, ypad = 0),
                                           zmid = 5),
                         layout = layout)
    # fig_temp.update_layout(annotations = annotations) # uncomment this in case we want to show annotations on the heatmap
    return fig_temp


################# -- stacked bar callback -- #############################################
@app.callback(
    Output('stacked-graph','figure'),
    [Input("df-storage", "children")])
def update_stackbar(top_ten):
    top_ten = pd.read_json(top_ten)

    top_ten = top_ten.sort_values("final_score",ascending=False)
    top_ten_cy = top_ten[top_ten["Year"] == 2019]
    max = top_ten_cy.head(1).iloc[0]["final_score"]
    top_ten_cy = top_ten_cy.sort_values("final_score")
    top_ten_cy['Safety Index - 1'] = ((top_ten_cy['Safety Index'] * top_ten_cy['saf']) / max)*100
    top_ten_cy['Health Care Index - 1'] = ((top_ten_cy['Health Care Index'] * top_ten_cy['hea']) / max)*100
    top_ten_cy['Cost of Living Index - 1'] = ((top_ten_cy['Cost of Living Index'] * top_ten_cy['cos']) / max)*100
    top_ten_cy['Pollution Index - 1'] = ((top_ten_cy['Pollution Index'] * top_ten_cy['pol']/ max))*100
    trace1 = go.Bar(y = city_only(top_ten_cy['City']),
                    x = top_ten_cy['Safety Index - 1'],
                    name = 'Safety',
                    orientation = 'h',
                    marker_color = '#001126')
    trace2 = go.Bar(y = city_only(top_ten_cy['City']),
                    x = top_ten_cy['Health Care Index - 1'],
                    name = 'Health',
                    orientation = 'h',
                    marker_color = '#16536e')
    trace3 = go.Bar(y = city_only(top_ten_cy['City']),
                    x = top_ten_cy['Cost of Living Index - 1'],
                    name = 'Cost of Living',
                    orientation = 'h',
                    marker_color = '#489eba')
    trace4 = go.Bar(y = city_only(top_ten_cy['City']),
                    x = top_ten_cy['Pollution Index - 1'],
                    name = 'Pollution',
                    orientation = 'h',
                    marker_color = '#b3c9d9')

    data = [trace1, trace2, trace3, trace4]

    layout=go.Layout(showlegend=False, title="Top cities compared", plot_bgcolor="white", margin=dict(t=50,b=5,r=5,l=5), barmode='stack', xaxis_tickangle=-45, legend_orientation = 'h',
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False))
    fig_stacked = go.Figure(data, layout)
    return fig_stacked

################# -- dots callback -- #############################################
@app.callback(
    Output('dots-graph','figure'),
    [Input("df-storage", "children")])
def update_dots(top_ten):
    top_ten = pd.read_json(top_ten)

    top_ten = top_ten.sort_values("final_score")
    top_ten_cy = top_ten[top_ten["Year"] == 2019]
    min_ind = min(top_ten_cy[["Pollution Index", "Safety Index","Cost of Living Index", "Health Care Index"]].min().values)

    data = []

    #initial colors by Michael
    colors = ["rgb(195,54,44)","rgb(255,134,66)","rgb(102,141,60)","rgb(0,151,172)","rgb(0,121,150)","rgb(195,183,172)","rgb(129,108,91)","rgb(177,221,161)","rgb(151,234,244)","rgb(6,194,244)"]

    #updated color scheme
    #colors = ['#494ca2','#8186d5','#c6cbef','#85cfcb','#219897','#ac3e31','#3282b8','#0f4c75','#bbe1fa','#b3c100','#000000']


    count = 0
    for c in top_ten_cy["City"].values:
        y = ["Pollution Index", "Safety Index","Cost of Living Index", "Health Care Index"]
        x = [top_ten_cy[top_ten_cy["City"] == c]["Pollution Index"].values[0],top_ten_cy[top_ten_cy["City"] == c]["Safety Index"].values[0], top_ten_cy[top_ten_cy["City"] == c]["Cost of Living Index"].values[0],top_ten_cy[top_ten_cy["City"] == c]["Health Care Index"].values[0] ]
        trace = go.Scatter(y=y,x=x, mode="markers", text=c, name=c,marker_color=colors[count%len(colors)], marker=dict(size=15), hovertext=c )
        count += 1
        data.append(trace)



    layout=go.Layout( title="Indicators of Top 10 Cities", plot_bgcolor="white", margin=dict(t=50,b=5,r=5,l=5), legend_orientation = 'h',
            xaxis=dict(range=[min_ind - 3, 101], zeroline=False, showgrid=False),
            yaxis=dict(zeroline=False, showgrid=True, gridwidth=1, gridcolor="lightgray"))
           
    fig_dot = go.Figure(data, layout)

    return fig_dot

################# -- box city callback -- #############################################
@app.callback(
    Output('box-city', 'children'),
    [Input("df-storage", "children")])
def update_box_city(top_ten):
    top_ten = pd.read_json(top_ten)

    top_one_city = top_ten.sort_values("final_score", ascending=False).head(n=1)["City"]
    top_one = top_ten[top_ten["City"] == top_one_city.values[0]]

    city = np.unique(top_one["City"].values)[0]

    return city

################# -- box temp callback -- #############################################
@app.callback(
    Output('box-temp', 'children'),
    [Input("df-storage", "children")])
def update_box_temp(top_ten):
    top_ten = pd.read_json(top_ten)

    top_one_city = top_ten.sort_values("final_score", ascending=False).head(n=1)["City"]
    top_one = top_ten[top_ten["City"] == top_one_city.values[0]]

    city = np.unique(top_one["City"].values)[0]

    df_tempe = pd.read_csv("data/temperature.csv")
    top_temp = df_tempe.loc[df_tempe["real_city"] == city]
    mean_temp = top_temp.iloc[:,1:].mean(axis=1).values[0]
    return str(round(mean_temp,2)) + "°C"

################# -- box rain callback -- #############################################
@app.callback(
    Output('box-rain', 'children'),
    [Input("df-storage", "children")])
def update_box_rain(top_ten):
    top_ten = pd.read_json(top_ten)

    top_one_city = top_ten.sort_values("final_score", ascending=False).head(n=1)["City"]
    top_one = top_ten[top_ten["City"] == top_one_city.values[0]]

    city = np.unique(top_one["City"].values)[0]

    df_rain = pd.read_csv("data/rain.csv")
    top_rain = df_rain.loc[df_rain["real_city"] == city]
    sum_rain = top_rain.iloc[:,1:].sum(axis=1).values[0]
    return str(int(sum_rain))

################# -- box sun callback -- #############################################
@app.callback(
    Output('box-sun', 'children'),
    [Input("df-storage", "children")])
def update_box_sun(top_ten):
    top_ten = pd.read_json(top_ten)

    top_one_city = top_ten.sort_values("final_score", ascending=False).head(n=1)["City"]
    top_one = top_ten[top_ten["City"] == top_one_city.values[0]]

    city = np.unique(top_one["City"].values)[0]

    df_sun = pd.read_csv("data/sun.csv")
    top_sun = df_sun.loc[df_sun["real_city"] == city]
    mean_sun = top_sun.iloc[:,1:].mean(axis=1).values[0]
    hours = int(mean_sun)
    minutes = int(60 * (mean_sun - hours))
    return str(hours) + "h " + str(minutes) + "min"


if __name__ == '__main__':
    app.run_server(debug = True)
