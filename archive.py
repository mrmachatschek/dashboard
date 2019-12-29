################# -- lines callback -- #############################################
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
    fig_lines = make_subplots(rows=1, cols=4,subplot_titles=('Clean Air', 'Cheap Living','Health', 'Safety'))
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
            row=1, col=4
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
            row=1, col=3
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

