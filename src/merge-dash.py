import pandas as pd
import altair as alt
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
df = pd.read_csv('Billionaires Statistics Dataset.csv', encoding="ISO-8859-1")
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)
df.head()
df_cleaned = df[['age', 'finalWorth']].dropna()
'''
chart = alt.Chart(df_cleaned).mark_circle(opacity=0.5).encode(
    x=alt.X('age:Q', title='Age'),
    y=alt.Y('finalWorth:Q', title='Wealth (Final Worth)'),
    tooltip=['age', 'finalWorth']
).properties(
    title='Age vs. Wealth'
)
chart
'''
df_cleaned = df[df['finalWorth'] < 20000]
'''chart = alt.Chart(df_cleaned).mark_circle(opacity=0.5).encode(
    x=alt.X('age:Q', title='Age'),
    y=alt.Y('finalWorth:Q', title='Wealth (Final Worth)'),
    tooltip=['age', 'finalWorth']
).properties(
    title='Age vs. Wealth'
)
chart'''
df_cleaned = df[['country', 'city', 'finalWorth']].dropna()


top_countries = df_cleaned.groupby('country').size().reset_index(name='count')
top_countries = top_countries.nlargest(10, 'count')


top_cities = df_cleaned.groupby('city').size().reset_index(name='count')
top_cities = top_cities.nlargest(10, 'count')
'''
chart_countries = alt.Chart(top_countries).mark_bar().encode(
    y=alt.Y('country:N', title='Country', sort='x'),
    x=alt.X('count:Q', title='Number of Billionaires'),
    tooltip=['country', 'count']
).properties(
    title='Top 10 Countries with the Most Billionaires'
)

chart_cities = alt.Chart(top_cities).mark_bar().encode(
    y=alt.Y('city:N', title='City', sort='x'),
    x=alt.X('count:Q', title='Number of Billionaires'),
    tooltip=['city', 'count']
).properties(
    title='Top 10 Cities with the Most Billionaires'
)
chart_countries'''
'''chart_cities'''
import altair as alt
import pandas as pd

# top 3 source
df_grouped = df.groupby('category', as_index=False)['finalWorth'].sum()
df_top_sources = df.groupby(['category', 'source'])['finalWorth'].sum().reset_index()
df_top_sources = df_top_sources.sort_values(['category', 'finalWorth'], ascending=[True, False]) 
df_top_sources = df_top_sources.groupby('category').head(3)

# tooltip
df_top_sources = df_top_sources.groupby('category')['source'].apply(lambda x: ', '.join(x)).reset_index()
df_grouped = df_grouped.merge(df_top_sources, on='category', how='left')
'''
# Altair
chart = alt.Chart(df_grouped).mark_bar().encode(
    x='finalWorth:Q',
    y=alt.Y('category:N', sort='-x'),
    tooltip=['category', 'finalWorth', 'source']
).properties(
    title="Total Final Worth by Category",
    width=600,
    height=400
)

chart'''

# top_countries
top_countries = df.groupby('country').size().reset_index(name='count')
top_countries = top_countries.nlargest(10, 'count')  # 选出前 10 个国家
top_countries['count'] = top_countries['count'].astype(int)  # 确保 `count` 是整数

# top_cities
top_cities = df.groupby('city').size().reset_index(name='count')
top_cities = top_cities.nlargest(10, 'count')  # 选出前 10 个城市
top_cities['count'] = top_cities['count'].astype(int)  # 确保 `count` 是整数

# define city
city_coordinates = {
    "New York": (40.7128, -74.0060),
    "Beijing": (39.9042, 116.4074),
    "Hong Kong": (22.3193, 114.1694),
    "Shanghai": (31.2304, 121.4737),
    "London": (51.5074, -0.1278),
    "Moscow": (55.7558, 37.6173),
    "Mumbai": (19.0760, 72.8777),
    "Shenzhen": (22.5431, 114.0579),
    "Singapore": (1.3521, 103.8198),
    "Delhi": (28.7041, 77.1025)
}

# add `top_cities`
top_cities["latitude_country"] = top_cities["city"].map(lambda x: city_coordinates[x][0])
top_cities["longitude_country"] = top_cities["city"].map(lambda x: city_coordinates[x][1])

# Importing
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

# ========== Dash App ==========
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = dbc.Container([
    html.H1("Data Visualization Dashboard", style={'textAlign': 'center'}),

    # Tabs
    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='Tab 1: World Map', value='tab1'),
        dcc.Tab(label='Tab 2: Wealth Analysis', value='tab2'),
        dcc.Tab(label='Tab 3: Top 10 Cities', value='tab3'),
        dcc.Tab(label='Tab 4: Wealth Distribution by Industry', value='tab4')

    ]),

    html.Div(id='tabs-content')
])

# ========== Tab ==========
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'tab1':
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id='xcol-widget',
                        value='age',
                        options=[{'label': col, 'value': col} for col in df.columns],
                        placeholder="Select X-axis"
                    ),
                    dcc.Dropdown(
                        id='ycol-widget',
                        value='finalWorth',
                        options=[{'label': col, 'value': col} for col in df.columns],
                        placeholder="Select Y-axis"
                    )],
                    md=4
                ),

                dbc.Col([
                    dcc.Graph(id='world-map')
                ], md=8)
            ]),

            dbc.Row([
                html.Iframe(
                    id='scatter',
                    style={'border-width': '0', 'width': '100%', 'height': '400px'}
                )
            ])
        ])

    elif tab == 'tab2':
        # ========== Wealth Factor ==========
        df["gdp_country"] = df["gdp_country"].replace(r"[\$,]", '', regex=True).astype(float)
        df["population_country"] = df["population_country"].astype(float)

        df["gdp_per_capita"] = df["gdp_country"] / df["population_country"]
        df["wealth_factor"] = (df["finalWorth"] * 1e6) / df["gdp_per_capita"]

        fig_hist = px.histogram(
            df, x="wealth_factor", nbins=50, log_y=True, title="Wealth Factor Distribution"
        )

        # ========== Billionaire Count (Log Scale) vs. Tertiary Education Enrollment Rate ==========
        edu_columns = ["country", "gross_tertiary_education_enrollment", "gross_primary_education_enrollment_country"]
        df_edu = df[edu_columns].dropna()

        billionaire_count_by_country = df.groupby("country").size()
        df_edu = df_edu.drop_duplicates(subset=["country"]).set_index("country")
        df_edu["billionaire_count"] = billionaire_count_by_country
        df_edu = df_edu.dropna()
        df_edu["billionaire_count_log"] = np.log1p(df_edu["billionaire_count"])

        fig1 = px.scatter(df_edu, 
                        x="gross_tertiary_education_enrollment", 
                        y="billionaire_count_log", 
                        hover_name=df_edu.index,  
                        hover_data={"billionaire_count": True},  
                        title="Billionaire Count (Log Scale) vs. Tertiary Education Enrollment Rate",
                        labels={"gross_tertiary_education_enrollment": "Gross Tertiary Education Enrollment (%)",
                                "billionaire_count_log": "Log(Number of Billionaires)",
                                "billionaire_count": "Real Number of Billionaires"})

        fig2 = px.scatter(df_edu, 
                        x="gross_primary_education_enrollment_country", 
                        y="billionaire_count_log", 
                        hover_name=df_edu.index,  
                        hover_data={"billionaire_count": True},  
                        title="Billionaire Count (Log Scale) vs. Primary Education Enrollment Rate",
                        labels={"gross_primary_education_enrollment_country": "Gross Primary Education Enrollment (%)",
                                "billionaire_count_log": "Log(Number of Billionaires)",
                                "billionaire_count": "Real Number of Billionaires"})

        # ========== Top 10 Countries: Billionaire Wealth as % of GDP ==========
        billionaire_wealth_by_country = df.groupby("country")["finalWorth"].sum() * 1000
        billionaire_gdp_ratio = (billionaire_wealth_by_country / df.groupby("country")["gdp_country"].first()) * 100
        per_capita_gdp = df.groupby("country")["gdp_country"].first() / df.groupby("country")["population_country"].first()
        billionaire_per_capita_gdp_ratio = billionaire_wealth_by_country / per_capita_gdp
        billionaire_density = (billionaire_count_by_country / df.groupby("country")["population_country"].first()) * 1_000_000

        wealth_inequality_metrics = pd.DataFrame({
            "Total Billionaire Wealth (Million $)": billionaire_wealth_by_country,
            "Billionaire Wealth / GDP (%)": billionaire_gdp_ratio,
            "Billionaire Wealth / Per Capita GDP (Years)": billionaire_per_capita_gdp_ratio,
            "Billionaires per Million People": billionaire_density
        }).dropna().sort_values("Billionaire Wealth / GDP (%)", ascending=False)

        # fig
        fig3 = px.bar(
            wealth_inequality_metrics.head(10), 
            x=wealth_inequality_metrics.head(10).index, 
            y="Billionaire Wealth / GDP (%)",
            title="Top 10 Countries: Billionaire Wealth as % of GDP",
            labels={"x": "Country", "y": "Billionaire Wealth as % of GDP"},
            color="Billionaire Wealth / GDP (%)",
            color_continuous_scale="blues"
        )

        return dbc.Container([
            html.H3("Wealth, Education & GDP Analysis"),

            dcc.Graph(figure=fig1),

            html.Hr(),
            dcc.Graph(figure=fig2),

            html.Hr(),
            dcc.Graph(figure=fig3)
        ])


    elif tab == 'tab3':
        fig_map = px.scatter_mapbox(
            top_cities, 
            lat="latitude_country", lon="longitude_country",
            text="city", size="count",
            color="count",
            hover_name="city",
            zoom=1, center={"lat": 30, "lon": 10},
            title="Top 10 Cities with the Most Billionaires",
            mapbox_style="open-street-map"
        )
    
        return dbc.Container([
            html.H3("Top 10 Cities with the Most Billionaires"),
            
            # map
            dcc.Graph(id="city-map", figure=fig_map)
        ])
    
    elif tab == 'tab4':
        fig7 = px.treemap(df, path=['industries'], values='finalWorth',
                          color_discrete_sequence=px.colors.qualitative.Set1)
        fig7.update_traces(textinfo="label+percent entry")
        fig7.update_layout(margin=dict(t=50, l=0, r=0, b=0))
        
        return dbc.Container([
            html.H3("Wealth Distribution by Industry"),
            dcc.Graph(figure=fig7)
        ])



# ========== World map（Tab 1）==========
@app.callback(
    Output('world-map', 'figure'),
    Input('xcol-widget', 'value'),
    Input('ycol-widget', 'value')
)
def update_world_map(xcol, ycol):
    df_grouped = df.groupby('country', as_index=False).agg(
        x_value=(xcol, 'sum'),
        y_value=(ycol, 'sum')
    )

    fig_map = px.choropleth(
        df_grouped,
        locations="country",
        locationmode="country names",
        color="y_value",
        hover_name="country",
        hover_data=["x_value", "y_value"],
        color_continuous_scale="Viridis",
        title=f"{ycol} Distribution"
    ).update_layout(height=500)

    return fig_map


# ========== altar Age vs Wealth（Tab 1）==========
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('world-map', 'clickData'),
    Input('xcol-widget', 'value'),
    Input('ycol-widget', 'value')
)
def update_scatter(clickData, xcol, ycol):
    if clickData:
        selected_country = clickData['points'][0]['location']
        filtered_df = df[df['country'] == selected_country]
    else:
        filtered_df = df  

    chart = alt.Chart(filtered_df).mark_circle(opacity=0.5).encode(
        x=alt.X(xcol, title=xcol),
        y=alt.Y(ycol, title=ycol),
        tooltip=['city', 'country']
    ).interactive()

    return chart.to_html()


# ========== city map (Tab 3）==========
@app.callback(
    Output('city-map', 'figure'),
    Input('city-map', 'clickData')
)
def update_city_map(clickData):
    if clickData:
        selected_city = clickData['points'][0]['hovertext']
        city_data = top_cities[top_cities['city'] == selected_city]

        fig_map = px.scatter_mapbox(
            top_cities, 
            lat="latitude_country", 
            lon="longitude_country",
            text="city", 
            size="count",
            color="count",
            hover_name="city",
            zoom=7,  
            center={
                "lat": city_data["latitude_country"].values[0], 
                "lon": city_data["longitude_country"].values[0]
            },
            title=f"Zoomed in: {selected_city}",
            mapbox_style="open-street-map"
        )
    else:
        # default top10 cities
        fig_map = px.scatter_mapbox(
            top_cities, 
            lat="latitude_country", 
            lon="longitude_country",
            text="city", 
            size="count",
            color="count",
            hover_name="city",
            zoom=1, 
            center={"lat": 30, "lon": 10},
            title="Top 10 Cities with the Most Billionaires",
            mapbox_style="open-street-map"
        )
    fig_map.update_layout(
        width=1200, 
        height=650,  
        margin=dict(l=10, r=10, t=50, b=10)  
    )
        
    return fig_map


# ========== Run ==========
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)