from dash import Output, Input, State
from data_fetcher import (
    fetch_historical_data,
    forecast_prices_linear_regression,
    fetch_news_sentiment,
    generate_recommendation,
)
from plotly.graph_objs import Figure, Scatter


def register_callbacks(app):
    # Callback for updating the stock price trend plot
    @app.callback(
        Output("price-trend", "figure"),
        Input("search-bar", "value"),
    )
    def update_price_trend(symbol):
        if not symbol:
            return Figure()

        try:
            # Fetch historical data
            historical_data = fetch_historical_data(symbol)

            # Validate the historical data
            if historical_data.empty:
                raise ValueError("No historical data found for the given stock symbol.")

            # Forecast prices
            forecast_data = forecast_prices_linear_regression(historical_data)

            # Create the plot
            figure = Figure()

            # Add historical prices to the plot
            figure.add_trace(
                Scatter(
                    x=historical_data.index,
                    y=historical_data["Close"],
                    mode="lines+markers",
                    name="Historical Prices",
                    line=dict(color="blue"),
                )
            )

            # Add forecasted prices to the plot
            figure.add_trace(
                Scatter(
                    x=forecast_data.index,
                    y=forecast_data["Forecast"],
                    mode="lines",
                    name="Forecasted Prices",
                    line=dict(color="orange", dash="dash"),
                )
            )

            # Update layout
            figure.update_layout(
                title=f"{symbol.upper()} Price Trends with Forecast",
                xaxis_title="Date",
                yaxis_title="Price",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                ),
            )

            return figure

        except ValueError as e:
            return Figure(layout=dict(title=str(e)))
        except Exception as e:
            return Figure(layout=dict(title=f"Unexpected error occurred: {e}"))

    # Callback for the chatbot
    @app.callback(
        Output("chatbot-output", "children"),
        Input("send-button", "n_clicks"),
        State("chatbot-input", "value"),
        State("search-bar", "value"),
    )
    def update_chatbot(n_clicks, user_message, stock_symbol):
        print(f"Chatbot callback triggered. Button clicks: {n_clicks}, Query: {user_message}, Stock Symbol: {stock_symbol}")

        if not user_message:
            return "Type your query and click 'Send'."

        try:
            if stock_symbol:
                # Check for keywords in the query
                user_query = user_message.lower()

                if "price" in user_query or "forecast" in user_query:
                    # Handle price forecast
                    historical_data = fetch_historical_data(stock_symbol)
                    forecast_data = forecast_prices_linear_regression(historical_data)
                    predicted_price = forecast_data["Forecast"].iloc[-1]
                    return f"The forecasted price for {stock_symbol.upper()} in the next period is ${predicted_price:.2f}."

                elif "recommendation" in user_query:
                    # Handle recommendation generation
                    historical_data = fetch_historical_data(stock_symbol)
                    forecast_data = forecast_prices_linear_regression(historical_data)
                    predicted_price = forecast_data["Forecast"].iloc[-1]
                    news_feed = fetch_news_sentiment(stock_symbol)
                    news_titles = [article["title"] for article in news_feed]
                    news_sentiment = " ".join(news_titles)
                    recommendation = generate_recommendation(
                        stock_symbol, predicted_price, news_sentiment
                    )
                    return recommendation

                elif "news" in user_query:
                    # Handle news query
                    news_feed = fetch_news_sentiment(stock_symbol)
                    news_titles = [article["title"] for article in news_feed]
                    return "Recent news headlines:\n" + "\n".join(news_titles)

            # General fallback response
            return (
                f"I'm here to assist you with stock-related questions for "
                f"{stock_symbol.upper() if stock_symbol else 'any stock'}."
            )

        except Exception as e:
            print(f"Chatbot error: {e}")  # Log the error for debugging
            return f"An error occurred: {e}"
