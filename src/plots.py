import altair as alt
import plotly.express as px
from data import df, top_countries, top_cities
import plotly.graph_objects as go
from data import df
import seaborn as sns
import numpy as np
import pandas as pd

def create_map(mode="count", selected_country=None):
    """ Generate the map, click on the country after Zoom In """
    if mode == 'count':
        color_col, title, colorbar_title, color_scale = 'billionaire_count', 'Billionaire Count by Country', "Billionaire Count", "Blues"
    elif mode == 'wealth':
        color_col, title, colorbar_title, color_scale = 'total_wealth', 'Total Billionaire Wealth by Country', "Total Wealth (Billion $)", "Viridis"
    else:
        color_col, title, colorbar_title, color_scale = 'billionaire_density', 'Billionaires per Capita', "Billionaire Density", "Plasma"

    df_grouped = df.groupby('country', as_index=False).agg(value=(color_col, 'sum'))

    color_min = df_grouped["value"].quantile(0.05) 
    color_max = df_grouped["value"].quantile(0.95)

    fig = px.choropleth(
        df_grouped,
        locations="country",
        locationmode="country names",
        color="value",
        hover_name="country",
        color_continuous_scale=color_scale,
        color_continuous_midpoint=df_grouped["value"].median(),
        range_color=[color_min, color_max]
    )

    fig.update_geos(
        showcoastlines=True,
        showland=True,
        landcolor="white",
        projection_type="natural earth"
     )

    # Legend position adjusts to the left
    fig.update_layout(
        height=700,
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(
            title="",
            ticks="outside",
            x=-0.15  
        )
    )

    # click on the country after Zoom In
    if selected_country:
        country_data = df[df['country'] == selected_country]
        if not country_data.empty:
            lat, lon = country_data["latitude_country"].values[0], country_data["longitude_country"].values[0]
            fig.update_layout(geo=dict(center=dict(lat=lat, lon=lon), projection_scale=4))  # ✅ Zoom In

    return fig


def create_radar_chart(country):
    """ radar chart """
    country_data = df[df['country'] == country].iloc[0]

    categories = ["Population (100M)", "Education Enrollment", "Tax Rate", "GDP (Trillion USD)"]
    values = [
        country_data['population_country'] / 1e8,  
        country_data['gross_tertiary_education_enrollment'],  
        country_data['total_tax_rate_country'],  
        country_data['gdp_country'] / 1e12  
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        marker=dict(color='blue'),  
        line=dict(color='blue')
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False,
        title=dict(text=f"{country} Economic Overview", font=dict(size=16, color="blue")) 
    )

    return fig

def create_ranking_bar_chart():
    """
    Create a ranking bar chart that showcases the top 10 cities with the most billionaires
    """
    top_cities = df.groupby('city')['billionaire_count'].count().reset_index()
    top_cities = top_cities.sort_values('billionaire_count', ascending=False).head(10)

    fig = px.bar(
        top_cities,
        x="billionaire_count",
        y="city",
        orientation='h',
        text="billionaire_count",
        title="Top 10 Cities with Most Billionaires",
        labels={"billionaire_count": "Number of Billionaires", "city": "City"},
        color="billionaire_count",
        color_continuous_scale="blues"
    )

    fig.update_traces(
        texttemplate='%{text}',
        textposition='inside'
    )
    fig.update_layout(
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending"),
        showlegend=False,
        margin=dict(t=50, l=0, r=15, b=25)
    )

    return fig


def create_treemap():
    """
    Create a Treemap to show the percentage of wealth in different industries
    """
    industry_group = df.groupby('industries', as_index=False)['finalWorth'].sum()
    
    fig = px.treemap(df, path=['industries'], values='finalWorth',
                  title='Wealth Distribution by Industry',
                  color_discrete_sequence=px.colors.qualitative.Set1,
                   branchvalues="total" )
    fig.update_traces(textinfo="label+percent entry")
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Wealth: $%{value:,.2f} Billion",
        textfont=dict(size=20)
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25),height=850,width=900,)
    
    return fig


def create_top5_cities_bar(selected_industry):
    """
    生成 Top 5 城市（按该行业财富排序）的柱状图
    """
    industry_df = df[df['industries'] == selected_industry]

    top_cities = (
        industry_df.groupby("city")["finalWorth"].sum()
        .reset_index()
        .sort_values("finalWorth", ascending=False)
        .head(5)
    )

    fig = px.bar(
        top_cities,
        x="finalWorth",
        y="city",
        orientation='h',
        text="finalWorth",
        title=f"Top 5 Cities in {selected_industry}",
        labels={"finalWorth": "Total Wealth (Billion)", "city": "City"},
        color_discrete_sequence=["#FFD700"]
    )

    fig.update_traces(texttemplate='%{text:.2s}B', textposition='inside')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)" )

    return fig


def create_top5_people_bar(selected_industry):
    """
    Generate a bar chart of the top 5 cities, sorted by wealth in that sector
    """
    industry_df = df[df['industries'] == selected_industry]

    top_people = (
        industry_df[["personName", "finalWorth"]]
        .sort_values("finalWorth", ascending=False)
        .head(5)
    )

    fig = px.bar(
        top_people,
        x="finalWorth",
        y="personName",
        orientation='h',
        text="finalWorth",
        title=f"Top 5 Billionaires in {selected_industry}",
        labels={"finalWorth": "Total Wealth (Billion)", "personName": "Billionaire","country":"Country"},
        color_discrete_sequence=["#FFD700"]
    )

    fig.update_traces(texttemplate='%{text:.2s}B', textposition='inside')
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending', 'tickmode': 'array', 'tickvals': top_people["personName"]},
        xaxis_title="Total Wealth (Billion)"
    )
    fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)" )

    return fig


def create_age_distribution():

    age_data = df["age"].dropna()
    age_data = age_data[(age_data > 10) & (age_data < 100)]
    fig = px.histogram(age_data, 
                       x="age", 
                       nbins=20, 
                       title="Billionaire Age Distribution",
                       labels={"age": "Age", "count": "Number of Billionaires"},
                       color_discrete_sequence=["#3498db"],  
                       opacity=0.8,  
                       text_auto=False  
                      )

   
    fig.update_traces(marker_line_color='black',  
                      marker_line_width=1,  
                      hoverinfo="x+y", 
                      textfont_size=12)  

    fig.update_layout(
        plot_bgcolor="white",  
        bargap=0.1, 
        title=dict(text="Billionaire Age Distribution", font=dict(size=20, family="Arial", color="black"), x=0.5),
        xaxis=dict(title="Age", tickangle=0, gridcolor="lightgrey"),
        yaxis=dict(title="Number of Billionaires", gridcolor="lightgrey"),
    )

    return fig

def create_gender_pie():
    """
    Generate a pie chart of the gender ratio of billionaires
    """
    # calculate gender ratio
    gender_counts = df['gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']

    color_map = {"M": "#1f77b4", "F": "#e377c2"}  # male-blue，female-pink

    # create pie chart
    fig = px.pie(gender_counts, 
                 names="Gender", 
                 values="Count",
                 title="Gender Distribution of Billionaires",
                 color="Gender",
                 color_discrete_map=color_map,
                 hole=0.4)  

    fig.update_traces(
        textinfo="percent+label",
        hoverinfo="label+value+percent",
        marker=dict(line=dict(color='white', width=2))
    )


    # adjust layout
    fig.update_layout(
        annotations=[
            dict(text="<b>Gender</b>", x=0.5, y=0.5, showarrow=False, font=dict(size=18))
        ]
    )

    return fig

def create_wealth_source_pie():
    """
    Generate a pie chart of sources of wealth (entrepreneurship/inheritance).
    """
    source_counts = df["selfMade"].value_counts().reset_index()
    source_counts.columns = ["Wealth Source", "Count"]
    source_counts["Wealth Source"] = source_counts["Wealth Source"].replace({True: "Self-made", False: "Inherited"})

    fig = px.pie(source_counts, values="Count", names="Wealth Source",
                 title="Self-made vs Inherited Billionaires",
                 color_discrete_sequence=["green", "orange"],
                  hole=0.4)
    fig.update_layout(
        annotations=[
            dict(text="<b>source</b>", x=0.5, y=0.5, showarrow=False, font=dict(size=18))
        ] 
    )
    return fig

