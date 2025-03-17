import dash
import dash_bootstrap_components as dbc
from dash import html
from styles import layout
from callback import register_callbacks


# create Dash app
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                suppress_callback_exceptions=True)
app.title = "Billionaire Insights Dashboard"

# set layout
app.layout = layout

# register callback app
register_callbacks(app)

# run dash_app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)