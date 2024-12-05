from dash import html, dcc

app_layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "padding": "20px"},
    children=[
        # Input for stock symbol
        dcc.Input(
            id="search-bar",
            type="text",
            placeholder="Search for stocks (e.g., AAPL)...",
            style={
                "width": "100%",
                "padding": "10px",
                "marginBottom": "20px",
                "borderRadius": "5px",
                "border": "1px solid #ccc",
            },
        ),
        # Price trend plot
        html.Div(
            id="price-trend-container",
            style={
                "backgroundColor": "#fff",
                "borderRadius": "10px",
                "padding": "20px",
                "marginBottom": "20px",
                "boxShadow": "0 2px 5px rgba(0,0,0,0.1)",
            },
            children=[
                html.H4("📈 Price Trends", style={"marginBottom": "15px"}),
                dcc.Graph(id="price-trend"),
            ],
        ),
        # Chatbot UI
        html.Div(
            style={
                "backgroundColor": "#fff",
                "borderRadius": "10px",
                "padding": "20px",
                "boxShadow": "0 2px 5px rgba(0,0,0,0.1)",
            },
            children=[
                html.H4("💬 AI Chatbot", style={"marginBottom": "10px"}),
                dcc.Textarea(
                    id="chatbot-input",
                    placeholder="Ask a question about the stock...",
                    style={
                        "width": "100%",
                        "height": "80px",
                        "marginBottom": "10px",
                        "borderRadius": "5px",
                        "border": "1px solid #ccc",
                        "padding": "10px",
                    },
                ),
                html.Button("Send", id="send-button", n_clicks=0),
                html.Div(
                    id="chatbot-output",
                    style={
                        "marginTop": "20px",
                        "padding": "10px",
                        "backgroundColor": "#f9f9f9",
                        "borderRadius": "5px",
                        "boxShadow": "0 2px 5px rgba(0,0,0,0.1)",
                    },
                ),
            ],
        ),
    ],
)
