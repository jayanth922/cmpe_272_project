from dash import Dash
from layout import app_layout
from callbacks import register_callbacks

# Initialize Dash app
app = Dash(__name__)
app.layout = app_layout

# Register callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
