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

df_original = pd.read_csv("data/indices_scaled_inversed.csv", index_col=0)
df=df_original.copy()
df_coord = pd.read_csv('data/coordinates.csv', index_col=0)

#### sun plot ####
df_sun = pd.read_csv("data/sun.csv")
df_sun_test = df_sun.iloc[0,:]
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
data = []
for i in range(1,len(months) + 1):
    x = [i for j in range(0, df_sun_test[months[i-1]])]
    y = [j + 0.5 + j*0.03 for j in range(0, df_sun_test[months[i-1]])]
    data.append(go.Scatter(x=x,y=y,mode="markers", marker=dict(symbol=18, color="yellow", size=11), hoverinfo="none"))
    data.append(go.Scatter(x=x,y=y,mode="markers", marker=dict(symbol="circle", color="yellow", size=10), hoverinfo="none"))

layout=go.Layout(showlegend=False, plot_bgcolor="white", margin=dict(t=50,b=5,r=5,l=5),
        xaxis=dict(showgrid=False, zeroline=False, ticktext=months, tickvals=[1,2,3,4,5,6,7,8,9,10,11,12]),title=dict(text="Sunny days in " + df_sun_test["real_city"]),
        yaxis=dict(showgrid=False, zeroline=False, range=[0,30]))

fig_sun = go.Figure(data, layout)

#### rain plot ####
df_rain = pd.read_csv("data/rain.csv")
df_rain_test = df_rain.iloc[0,:]
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
data = []
for i in range(1,len(months) + 1):
    x = [i for j in range(0, df_rain_test[months[i-1]])]
    y = [j + 0.5 + j*0.03 for j in range(0, df_rain_test[months[i-1]])]
    data.append(go.Scatter(x=x,y=y,mode="markers", marker=dict(symbol="circle", color="blue", size=11), hoverinfo="none"))

layout=go.Layout(showlegend=False, plot_bgcolor="white", margin=dict(t=50,b=5,r=5,l=5),
        xaxis=dict(showgrid=False, zeroline=False, ticktext=months, tickvals=[1,2,3,4,5,6,7,8,9,10,11,12]),title=dict(text="Rainy days in " + df_rain_test["real_city"]),
        yaxis=dict(showgrid=False, zeroline=False, range=[0,30]))

fig_rain = go.Figure(data, layout)

#### temp plot ####
df_temp = pd.read_csv("data/temperature.csv")
df_temp_test = df_temp.iloc[0,:]
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
data = []
x = [j for j in range(1, 13)]
y = df_temp_test[months].values
data.append(go.Scatter(x=x,y=y ,marker=dict(symbol="circle", color="gray", size=8)))

layout=go.Layout(showlegend=False, plot_bgcolor="white", margin=dict(t=50,b=5,r=5,l=5),
        xaxis=dict(showgrid=False, zeroline=False, ticktext=months, tickvals=[1,2,3,4,5,6,7,8,9,10,11,12]),title=dict(text="Average Temperature in " + df_temp_test["real_city"]),
        yaxis=dict(showgrid=False, zeroline=False))

fig_temp = go.Figure(data, layout)

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

fig_lines = make_subplots(rows=2, cols=2,subplot_titles=('Clean Air', 'Cheap Living','Health', 'Safety'))
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

            html.Div([
                html.H6(children = 'Safety')
            ], id = 'first-preference-title', className = 'col'),

            html.Div([
                dcc.Slider(
                    id='slider-safety',
                    min = 0,
                    max = 1,
                    step = 0.1,
                    value = .5
                )
            ], id = 'first-preference', className = 'col'),

            html.Div([
                html.H6(children = 'Health Care')
            ], id = 'second-preference-title', className = 'col'),

            html.Div([
                dcc.Slider(
                    id='slider-health',
                    min = 0,
                    max = 1,
                    step = 0.1,
                    value = .5
                )
            ], id = 'second-preference', className = 'col'),

            html.Div([
                html.H6(children = 'Cheap Living')
            ], id = 'third-preference-title', className = 'col'),

            html.Div([
                dcc.Slider(
                    id='slider-costs',
                    min = 0,
                    max = 1,
                    step = 0.1,
                    value = .5
                )
            ], id = 'third-preference', className = 'col'),

            html.Div([
                html.H6(children = 'Clean Air')
            ], id = 'fourth-preference-title', className = 'col'),

            html.Div([
                dcc.Slider(
                    id='slider-pollution',
                    min = 0,
                    max = 1,
                    step = 0.1,
                    value = .5
                )
            ], id = 'fourth-preference', className = 'col'),

        ], id = 'preferences-div', className = 'shadow p-4 mb-5 bg-white rounded', style = {'margin-right':20}),

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
                dcc.Graph(figure=fig_temp, config={'displayModeBar': False})
            ], className = 'col shadow p-4 mb-5 bg-white rounded', style = {'margin-right':20}),
            html.Div([
                dcc.Graph(figure=fig_sun, config={'displayModeBar': False})
            ], className = 'col shadow p-4 mb-5 bg-white rounded', style = {'margin-right':20}),
            html.Div([
                dcc.Graph(figure=fig_rain, config={'displayModeBar': False})
            ], className = 'col shadow p-4 mb-5 bg-white rounded')], className="row")

    ], id = 'outer-div', className = 'container')

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
    fig_lines = make_subplots(rows=2, cols=2,subplot_titles=('Clean Air', 'Cheap Living','Health', 'Safety'))
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
        fig_lines.update_layout(plot_bgcolor="#e5ecf6", margin=dict(t=110,b=15,r=15,l=15), title=dict(text="Comparison of Top Cities", y=0.98, x=0.5, xanchor="center", yanchor="top"), legend_orientation="h", legend=dict(x=0.1, y=1.2) )
    return fig_lines

if __name__ == '__main__':
    app.run_server(debug = True)
