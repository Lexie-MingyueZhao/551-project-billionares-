import altair as alt
import plotly.express as px
from data import df, top_countries, top_cities
import plotly.graph_objects as go
from data import df
import seaborn as sns
import numpy as np
import pandas as pd

def create_map(mode="count", selected_country=None):
    """ ✅ 生成地图，点击国家后 Zoom In，Legend 位置调整到左侧 """
    if mode == 'count':
        color_col, title, colorbar_title, color_scale = 'billionaire_count', 'Billionaire Count by Country', "Billionaire Count", "Blues"
    elif mode == 'wealth':
        color_col, title, colorbar_title, color_scale = 'total_wealth', 'Total Billionaire Wealth by Country', "Total Wealth (Billion $)", "Viridis"
    else:
        color_col, title, colorbar_title, color_scale = 'billionaire_density', 'Billionaires per Capita', "Billionaire Density", "Plasma"

    df_grouped = df.groupby('country', as_index=False).agg(value=(color_col, 'sum'))

    fig = px.choropleth(
        df_grouped,
        locations="country",
        locationmode="country names",
        color="value",
        hover_name="country",
        color_continuous_scale=color_scale,
        title=title
    )

    # ✅ 调整 Legend 位置（放在左侧）
    fig.update_layout(
        height=700,
        geo=dict(showcoastlines=True, projection_type="natural earth"),
        coloraxis_colorbar=dict(
            title=colorbar_title,
            ticks="outside",
            x=-0.15  # ✅ 调整到左侧
        )
    )

    # ✅ 如果点击了国家，放大该地区
    if selected_country:
        country_data = df[df['country'] == selected_country]
        if not country_data.empty:
            lat, lon = country_data["latitude_country"].values[0], country_data["longitude_country"].values[0]
            fig.update_layout(geo=dict(center=dict(lat=lat, lon=lon), projection_scale=4))  # ✅ Zoom In

    return fig


def create_radar_chart(country):
    """ ✅ 蓝色主题雷达图 """
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


def create_treemap():
    """
    创建一个 Treemap 展示不同行业的财富占比
    """
    industry_group = df.groupby('industries', as_index=False)['finalWorth'].sum()
    
    fig = px.treemap(df, path=['industries'], values='finalWorth',
                  title='Wealth Distribution by Industry',
                  color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_traces(textinfo="label+percent entry")
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Wealth: $%{value:,.2f} Billion"
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
    )

    fig.update_traces(texttemplate='%{text:.2s}B', textposition='outside')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    fig.update_layout(showlegend=False)

    return fig


def create_top5_people_bar(selected_industry):
    """
    生成 Top 5 富豪（按该行业财富排序）的柱状图
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
    )

    fig.update_traces(texttemplate='%{text:.2s}B', textposition='outside')
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending', 'tickmode': 'array', 'tickvals': top_people["personName"]},
        xaxis_title="Total Wealth (Billion)"
    )

    return fig


def create_age_distribution():

    age_data = df["age"].dropna()
    age_data = age_data[(age_data > 10) & (age_data < 100)]
    fig = px.histogram(age_data, 
                       x="age", 
                       nbins=20, 
                       title="Billionaire Age Distribution",
                       labels={"age": "Age", "count": "Number of Billionaires"},
                       color_discrete_sequence=["#3498db"],  # 更柔和的蓝色
                       opacity=0.8,  # 透明度增强层次感
                       text_auto=False  # 直方图上显示具体数值
                      )

    # 添加优化细节
    fig.update_traces(marker_line_color='black',  # 给柱子加黑色边框，增强对比度
                      marker_line_width=1,  
                      hoverinfo="x+y",  # 鼠标悬停时显示 X 轴和 Y 轴数据
                      textfont_size=12)  

    # 图表美化
    fig.update_layout(
        plot_bgcolor="white",  # 设为白色背景
        bargap=0.1,  # 调整柱子间隔
        title=dict(text="Billionaire Age Distribution", font=dict(size=20, family="Arial", color="black"), x=0.5),
        xaxis=dict(title="Age", tickangle=0, gridcolor="lightgrey"),
        yaxis=dict(title="Number of Billionaires", gridcolor="lightgrey"),
    )

    return fig

def create_gender_pie():
    """
    生成亿万富翁的性别比例饼图
    """
    # 计算性别比例
    gender_counts = df['gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']

    # 颜色映射
    color_map = {"M": "#1f77b4", "F": "#e377c2"}  # 男性-蓝色，女性-粉色

    # 生成饼图
    fig = px.pie(gender_counts, 
                 names="Gender", 
                 values="Count",
                 title="Gender Distribution of Billionaires",
                 color="Gender",
                 color_discrete_map=color_map,
                 hole=0.4)  # 设定圆环

    # 增强 Tooltip（显示性别、人数、百分比）
    fig.update_traces(
        textinfo="percent+label",
        hoverinfo="label+value+percent",
        marker=dict(line=dict(color='white', width=2))
    )


    # 调整布局
    fig.update_layout(
        annotations=[
            dict(text="<b>Gender</b>", x=0.5, y=0.5, showarrow=False, font=dict(size=18))
        ]
    )

    return fig

def create_wealth_source_pie():
    """
    生成财富来源（创业/继承）饼图
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

