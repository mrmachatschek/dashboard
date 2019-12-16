import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
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

df = pd.read_csv("data/qol_indices.csv", index_col=0)
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
                   

################# -- safety index line -- #############################################

df_plot = filtering(df, 'Abu Dhabi, United Arab Emirates')
df_plot = df_plot.sort_values("Year")

fig_safety = go.Figure(data=go.Scatter(x=df_plot["Year"],y=df_plot["Safety Index"]))

fig_safety.update_layout(title = 'Safety Index')


################# -- health care line -- #############################################

df_plot = filtering(df, 'Abu Dhabi, United Arab Emirates')
df_plot = df_plot.sort_values("Year")

fig_health = go.Figure(data=go.Scatter(x=df_plot["Year"],y=df_plot["Health Care Index"]))

fig_health.update_layout(title = 'Health Care Index')

################# -- cost of living index line -- #############################################

df_plot = filtering(df, 'Abu Dhabi, United Arab Emirates')
df_plot = df_plot.sort_values("Year")

fig_costs = go.Figure(data=go.Scatter(x=df_plot["Year"],y=df_plot["Cost of Living Index"]))

fig_costs.update_layout(title = 'Cost of Living Index')


################# -- pollution line -- #############################################

df_plot = filtering(df, 'Abu Dhabi, United Arab Emirates')
df_plot = df_plot.sort_values("Year")

fig_pollution = go.Figure(data=go.Scatter(x=df_plot["Year"],y=df_plot["Pollution Index"]))

fig_pollution.update_layout(title = 'Pollution Index')


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

app.layout = html.Div(
    # outer container
    html.Div([
        
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
                    max = 2, 
                    step = 0.5,
                    value = 1
                )
            ], id = 'first-preference', className = 'col'),
            
            html.Div([
                html.H6(children = 'Health Care')
            ], id = 'second-preference-title', className = 'col'),
            
            html.Div([
                dcc.Slider(
                    id='slider-health',
                    min = 0,
                    max = 2, 
                    step = 0.5,
                    value = 1
                )
            ], id = 'second-preference', className = 'col'),
            
            html.Div([
                html.H6(children = 'Cost of Living')
            ], id = 'third-preference-title', className = 'col'),
            
            html.Div([
                dcc.Slider(
                    id='slider-costs',
                    min = 0,
                    max = 2, 
                    step = 0.5,
                    value = 1
                )
            ], id = 'third-preference', className = 'col'),
            
            html.Div([
                html.H6(children = 'Pollution')
            ], id = 'fourth-preference-title', className = 'col'),
            
            html.Div([
                dcc.Slider(
                    id='slider-pollution',
                    min = 0,
                    max = 2, 
                    step = 0.5,
                    value = 1
                )
            ], id = 'fourth-preference', className = 'col'),
            
            # button div
            html.Div([
            html.Button(
                    id='submit-button',
                    children='Filter cities',
                    style={'fontSize':18}
                ) 
            ],className= "col justify-content-md-center" ),
             
        ], id = 'preferences-div', className = 'shadow p-3 mb-5 bg-white rounded', style = {'margin-right':20}),
           
        # map div 
        html.Div([
            
            dcc.Graph(id = 'fig-map',
                    figure = fig_map)
        ], id = 'map-div', className = 'col auto shadow p-9 mb-5 bg-white rounded'),
        

    ], id = 'first-container', className = 'row', style = {'margin-top':0}),
    
    html.Div([
        
        html.Div([
            dcc.Graph(id = 'fig-safety', 
                      figure = fig_safety)
            
        ], id = 'first-right-graph', className = 'six columns'),
        
        html.Div([
            dcc.Graph(id = 'fig-health',
                      figure = fig_health)
        ], id = 'first-left-graph', className = 'six columns')
        
    ], id = 'first-row', className = 'twelve columns'),
    
    html.Div([
        
        html.Div([
            dcc.Graph(id = 'fig-costs', 
                      figure = fig_costs)
            
        ], id = 'second-right-graph', className = 'six columns'),
        
        html.Div([
            dcc.Graph(id = 'fig-pollutions',
                      figure = fig_pollution)
        ], id = 'second-left-graph', className = 'six columns')
        
    ], id = 'second-row', className = 'twelve columns')

    ], id = 'outer-div', className = 'container')
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
    [Input("submit-button", "n_clicks")],
    [State('slider-safety', 'value'),
     State('slider-health', 'value'),
     State('slider-costs', 'value'),
     State('slider-pollution', 'value'),
     ])
def update_map(n,a,b,c,d):
    df["final_score"] = a * df["Safety Index"] + b * df["Health Care Index"] + c * df["Cost of Living Index"] + d * df["Pollution Index"]
    df_cy = df[df["Year"] == 2019]
    df_cy = df_cy.sort_values("final_score", ascending=False)
   
    top_five = df_cy.head(n=5)
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
    Output('fig-safety', 'figure'),
    [Input("submit-button", "n_clicks")],
    [State('slider-safety', 'value'),
     State('slider-health', 'value'),
     State('slider-costs', 'value'),
     State('slider-pollution', 'value'),
     ])
def update_safety(n,a,b,c,d):        
    df["final_score"] = a * df["Safety Index"] + b * df["Health Care Index"] + c * df["Cost of Living Index"] + d * df["Pollution Index"]
    df_temp = df.sort_values("final_score", ascending=False)
    top_five = df_temp[df_temp["Year"] == 2019].head(n=5)
    top_five = top_five.sort_values("final_score", ascending=False)
    top_five = df_temp[df_temp["City"].isin(top_five["City"].values)]

    top_five = top_five.sort_values("Year")
    cities = np.unique(top_five["City"].values)
    traces = []
    for city in cities:
        traces.append(go.Scatter(x=top_five[top_five["City"] == city]["Year"],y=top_five[top_five["City"] == city]["Safety Index"], name=city))
    fig_safety = go.Figure(data=traces)
    fig_safety.update_layout(title = 'Safety Index')
    
    return fig_safety

################# -- health callback -- #############################################
@app.callback(
    Output('fig-health', 'figure'),
    [Input("submit-button", "n_clicks")],
    [State('slider-safety', 'value'),
     State('slider-health', 'value'),
     State('slider-costs', 'value'),
     State('slider-pollution', 'value'),
     ])
def update_health(n,a,b,c,d):        
    df["final_score"] = a * df["Safety Index"] + b * df["Health Care Index"] + c * df["Cost of Living Index"] + d * df["Pollution Index"]
    df_health = df.sort_values("final_score", ascending=False)
    top_five = df_health[df_health["Year"] == 2019].head(n=5)
    top_five = top_five.sort_values("final_score", ascending=False)
    top_five = df_health[df_health["City"].isin(top_five["City"].values)]

    top_five = top_five.sort_values("Year")
    cities = np.unique(top_five["City"].values)
    traces = []
    for city in cities:
        traces.append(go.Scatter(x=top_five[top_five["City"] == city]["Year"],y=top_five[top_five["City"] == city]["Health Care Index"], name=city))
    fig_health = go.Figure(data=traces)
    fig_health.update_layout(title = 'Health Care Index')
    
    return fig_health

################# -- costs callback -- #############################################
@app.callback(
    Output('fig-costs', 'figure'),
    [Input("submit-button", "n_clicks")],
    [State('slider-safety', 'value'),
     State('slider-health', 'value'),
     State('slider-costs', 'value'),
     State('slider-pollution', 'value'),
     ])
def update_costs(n,a,b,c,d):        
    df["final_score"] = a * df["Safety Index"] + b * df["Health Care Index"] + c * df["Cost of Living Index"] + d * df["Pollution Index"]
    df_costs = df.sort_values("final_score", ascending=False)
    top_five = df_costs[df_costs["Year"] == 2019].head(n=5)
    top_five = top_five.sort_values("final_score", ascending=False)
    top_five = df_costs[df_costs["City"].isin(top_five["City"].values)]

    top_five = top_five.sort_values("Year")
    cities = np.unique(top_five["City"].values)
    traces = []
    for city in cities:
        traces.append(go.Scatter(x=top_five[top_five["City"] == city]["Year"],y=top_five[top_five["City"] == city]["Cost of Living Index"], name=city))
    fig_costs = go.Figure(data=traces)
    fig_costs.update_layout(title = 'Cost of Living Index')
    
    return fig_costs

################# -- pollution callback -- #############################################
@app.callback(
    Output('fig-pollutions', 'figure'),
    [Input("submit-button", "n_clicks")],
    [State('slider-safety', 'value'),
     State('slider-health', 'value'),
     State('slider-costs', 'value'),
     State('slider-pollution', 'value')])
def update_pollutions(n,a,b,c,d):        
    df["final_score"] = a * df["Safety Index"] + b * df["Health Care Index"] + c * df["Cost of Living Index"] + d * df["Pollution Index"]
    df_pollutions = df.sort_values("final_score", ascending=False)
    top_five = df_pollutions[df_pollutions["Year"] == 2019].head(n=5)
    top_five = top_five.sort_values("final_score", ascending=False)
    top_five = df_pollutions[df_pollutions["City"].isin(top_five["City"].values)]

    top_five = top_five.sort_values("Year")
    cities = np.unique(top_five["City"].values)
    traces = []
    for city in cities:
        traces.append(go.Scatter(x=top_five[top_five["City"] == city]["Year"],y=top_five[top_five["City"] == city]["Pollution Index"], name=city))
    fig_pollution = go.Figure(data=traces)
    fig_pollution.update_layout(title = 'Pollution Index')
    
    return fig_pollution



if __name__ == '__main__':
    app.run_server(debug = True)
    
    
 