import dash_bootstrap_components as dbc
from dash import dcc, html

layout = dbc.Container([
    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='Where the Billionaires Are', value='tab1'),
        dcc.Tab(label='The Business of Billionaires', value='tab2'),
        dcc.Tab(label='Meet the Billionaires', value='tab3'),
    ]),

    html.Div(id='tabs-content'),  
])

