from dash.dependencies import Input, Output
from dash import dcc, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from data import df, top_cities 
from plots import create_map, create_radar_chart,create_treemap, create_top5_cities_bar, create_top5_people_bar, create_age_distribution, create_gender_pie, create_wealth_source_pie
def register_callbacks(app):
    @app.callback(
        Output('tabs-content', 'children'),
        Input('tabs', 'value')
    )
    def render_content(tab):
        """ 监听 Tabs 变化，动态更新内容 """
        if tab == 'tab1':
            return dbc.Container([  
                html.H3("Global Billionaire Distribution", 
                        style={'textAlign': 'center', 'fontWeight': 'bold'}),

                # ✅ 模式切换按钮
                dcc.RadioItems(
                    id='map-mode',
                    options=[
                        {'label': 'Billionaire Count', 'value': 'count'},
                        {'label': 'Total Wealth', 'value': 'wealth'},
                        {'label': 'Billionaires per Capita', 'value': 'density'}
                    ],
                    value='count',
                    labelStyle={'display': 'block'}
                ),
                dbc.Row([
                    dbc.Col(dcc.Graph(id="world-map"), width=8),  # 🌍 左侧地图
                    dbc.Col(html.Div(id="country-details"), width=4)  # 📊 右侧雷达图
                ])
            ])
        
        elif tab == 'tab2':
            return dbc.Container([
                html.H3("Wealth Distribution by Industry2", 
                        style={'textAlign': 'center', 'fontWeight': 'bold'}),

                # 📌 Ensuring Treemap and Right Content align properly
                dbc.Row([
                    # 📌 Treemap (Left Column) - Takes 8/12 width
                    dbc.Col([
                        dcc.Graph(id="industry-treemap", figure=create_treemap(),
                                style={'height': '400px', 'width': '100%', 'minHeight': '500px'})
                    ], width=8, style={'display': 'flex', 'alignItems': 'stretch'}),

                    # 📌 Right-Side Content - Takes 4/12 width
                    dbc.Col([
                        # 💰 Total Wealth Box
                        dbc.Card(
                            dbc.CardBody([
                                html.H4("Total Wealth", className="card-title", 
                                        style={'textAlign': 'center', 'fontWeight': 'bold'}),
                                html.P(id="industry-wealth-box",
                                    className="card-text",
                                    style={'fontSize': '22px', 'textAlign': 'center', 'color': '#2C3E50'})
                            ]),
                            className="border-primary shadow-lg",
                            style={'backgroundColor': '#f8f9fa', 'marginBottom': '10px'}
                        ),

                        # 📊 Top 5 Cities & Billionaires (Equal Height)
                        dbc.Row([
                            dbc.Col(dcc.Graph(id="top5-cities-bar", 
                                            style={'height': '280px', 'width': '100%'}), width=12),
                            dbc.Col(dcc.Graph(id="top5-people-bar", 
                                            style={'height': '280px', 'width': '100%'}), width=12)
                        ], style={'display': 'flex', 'flexDirection': 'column'})
                    ], width=4, 
                    style={'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'flex-start'})
                ], style={'height': '600px'})  # ✅ Makes sure both sides are balanced
            ], fluid=True)

        
        elif tab == 'tab3':
            return dbc.Container([
                html.H3("Billionaire Insights", style={'textAlign': 'center', 'fontWeight': 'bold'}),
                
                # 📌 Dropdown 让用户选择问题
                dcc.Dropdown(
                    id='question-selector',
                    options=[
                        {'label': 'Age Distribution', 'value': 'age'},
                        {'label': 'Gender Ratio', 'value': 'gender'},
                        {'label': 'Wealth Source (Self-made vs Inherited)', 'value': 'source'},
                    ],
                    value='age',  # 默认选择年龄分布
                    clearable=False
                ),

                # 📊 这里放动态生成的图表
                dcc.Graph(id="question-graph"),
                
                # 📄 文字解释
                html.Div(id="question-text", style={'marginTop': '20px', 'fontSize': '16px'})
            ])
        
        
        return html.Div("Select a tab to view content")

    # ✅ 修正 update_world_map，监听 map-mode 的变化
    @app.callback(
        Output('world-map', 'figure'),
        Input('map-mode', 'value'),
        Input('world-map', 'clickData')
    )
    def update_world_map(mode, clickData=None):
        selected_country = None
        if clickData and 'points' in clickData:
            selected_country = clickData['points'][0]['location']
        
        if selected_country not in df['country'].unique():
            selected_country = None

        return create_map(mode, selected_country)

    # ✅ 监听 world-map 的点击，显示 GDP、人口、教育、税收
    @app.callback(
        Output('country-details', 'children'),
        Input('world-map', 'clickData')
    )
    def update_country_details(clickData):
        """ 点击国家后，显示 GDP、人口、教育水平、税收 """
        country = "China" 
        if clickData:
            country = clickData['points'][0]['location']

        country_data = df[df['country'] == country]

        if country_data.empty:
            return html.Div(f"No data available for {country}")

        country_data = country_data.iloc[0]
        # ✅ 格式化数值
        gdp_trillion = country_data['gdp_country'] / 1e12  # 转换为万亿美元
        population_billion = country_data['population_country'] / 1e9  # 转换为十亿

        # ✅ 教育指数 & 税率增加描述
        edu_index = country_data['gross_tertiary_education_enrollment']
        tax_rate = country_data['total_tax_rate_country']

        if edu_index > 70:
            edu_desc = " (High)"
        elif edu_index > 40:
            edu_desc = " (Medium)"
        else:
            edu_desc = " (Low)"

        if tax_rate > 35:
            tax_desc = " (High)"
        elif tax_rate > 20:
            tax_desc = " (Medium)"
        else:
            tax_desc = " (Low)"
        radar_fig = create_radar_chart(country)

        return dbc.Container([
            html.H3(f"{country} Overview"),
            html.P(f"GDP: ${gdp_trillion:.2f} Trillion"),
            html.P(f"Population: {population_billion:.2f} Billion"),
            html.P(f"Education Index: {edu_index:.2f}{edu_desc}"),
            html.P(f"Tax Rate: {tax_rate:.2f}%{tax_desc}"),

            dcc.Graph(figure=radar_fig)
        ])
    @app.callback(
    [Output("industry-wealth-box", "children"),  # 右上角 Wealth 框
         Output("top5-cities-bar", "figure"),  # 中部 Top 5 城市
         Output("top5-people-bar", "figure")],  # 底部 Top 5 富豪
        Input("industry-treemap", "clickData")
    )
    def update_industry_info(clickData):
        """ 点击 Treemap 时，更新财富总量 + Top5 城市 & 富豪 """
        
        if not clickData:
            selected_industry = "Technology"
        else:
            selected_industry = clickData["points"][0]["label"]
        # 🏦 计算该行业总财富
        industry_total_wealth = df[df['industries'] == selected_industry]["finalWorth"].sum()

        # 🏙️ 生成 Top 5 城市柱状图 & 👤 生成 Top 5 富豪柱状图
        top_cities_fig = create_top5_cities_bar(selected_industry)
        top_people_fig = create_top5_people_bar(selected_industry)

        # 📌 更新 右上角 Wealth 统计框
        industry_wealth_text = f"Total Wealth: ${industry_total_wealth:,.2f} Billion"

        # 📌 更新 详情框
        industry_details_div = html.Div([
            html.H4(f"{selected_industry} Overview", style={'fontWeight': 'bold'}),
            html.P(f"Total Wealth: ${industry_total_wealth:,.2f} Billion", style={'fontSize': '18px'}),
        ])

        return industry_wealth_text, top_cities_fig, top_people_fig
    
    
    @app.callback(
        [Output("question-graph", "figure"),
        Output("question-text", "children")],
        Input("question-selector", "value")
    )
    def update_question_chart(selected_question):
        """ 根据用户选择的问题，返回相应的图表和解释 """

        if selected_question == "age":
            fig = create_age_distribution()
            text = html.Div([
                html.P("Key Insights from Age Distribution:", style={"font-weight": "bold"}),
                html.Ul([
                    html.Li("Most billionaires are between 50 and 70 years old, with the highest concentration around 60."),
                    html.Li("There are fewer billionaires under 40, indicating that accumulating great wealth at a young age is rare."),
                    html.Li("Billionaires over 70 still make up a significant portion, but their numbers gradually decline."),
                ])
            ])
        
        elif selected_question == "gender":
            fig = create_gender_pie()
            text = html.Div([
                html.P("Key Insights from Gender Ratio:", style={"font-weight": "bold"}),
                html.Ul([
                    html.Li([
                        html.Span("Male Dominance", style={"font-weight": "bold"}),
                        html.Br(),
                        "• 87.2% of billionaires are male, shown in blue.",
                        html.Br(),
                        "• This indicates that the vast majority of global billionaires are men."
                    ]),

                    html.Li([
                        html.Span("Female Billionaires are a Minority", style={"font-weight": "bold"}),
                        html.Br(),
                        "• Only 12.8% of billionaires are female, represented in pink.",
                        html.Br(),
                        "• This suggests a significant gender disparity in extreme wealth accumulation."
                    ])
                ])
            ])
        
	

        elif selected_question == "source":
            fig = create_wealth_source_pie()
            text = html.Div([
                html.P("Key Insights from Wealth Source:", style={"font-weight": "bold"}),

                html.Ul([
                    html.Li([
                        html.Span("Self-Made Billionaires Dominate", style={"font-weight": "bold"}),
                        html.Br(),
                        "• 68.6% of billionaires built their own wealth, shown in green.",
                        html.Br(),
                        "• This suggests that the majority of billionaires achieved their status through entrepreneurship, investments, or business ventures."
                    ]),

                    html.Li([
                        html.Span("Inherited Billionaires Are a Minority", style={"font-weight": "bold"}),
                        html.Br(),
                        "• 31.4% of billionaires inherited their wealth, represented in orange.",
                        html.Br(),
                        "• While still a significant portion, this indicates that most billionaires are not born into wealth but create it themselves."
                    ])
                ])
            ])

        else:
            fig = {px.scatter()}
            text = "Select an option to display data."

        return fig, text