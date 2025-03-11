import dash
import dash_bootstrap_components as dbc
from dash import html
from styles import layout
from callback import register_callbacks


# 创建 Dash 应用
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                suppress_callback_exceptions=True)
app.title = "Billionaire Insights Dashboard"

# 设置布局
app.layout = layout

# 注册回调函数
register_callbacks(app)

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)