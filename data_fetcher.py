import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def fetch_historical_data(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "Time Series (Daily)" in data:
        df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index", dtype=float)
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        }, inplace=True)
        return df
    elif "Error Message" in data:
        raise ValueError("Invalid stock symbol. Please check input.")
    elif "Note" in data:
        raise ValueError("API rate limit exceeded. Please wait and try again.")
    else:
        raise ValueError("Unexpected error occurred.")

def forecast_prices_linear_regression(historical_df, periods=90):
    try:
        # Ensure the data is sorted by date
        historical_df = historical_df.sort_index()

        # Prepare the data for regression
        dates = np.arange(len(historical_df)).reshape(-1, 1)  # Use sequential indices as X
        prices = historical_df["Close"].values  # Use closing prices as Y

        # Fit a linear regression model
        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("model", LinearRegression())
        ])
        pipeline.fit(dates, prices)

        # Generate future indices for forecasting
        future_dates = np.arange(len(historical_df), len(historical_df) + periods).reshape(-1, 1)

        # Predict future prices
        future_prices = pipeline.predict(future_dates)

        # Create a DataFrame for forecasted prices
        forecast_index = pd.date_range(start=historical_df.index[-1], periods=periods + 1, freq="D")[1:]
        forecast_df = pd.DataFrame({"Forecast": future_prices}, index=forecast_index)

        return forecast_df
    except Exception as e:
        raise ValueError(f"Forecasting failed: {e}")



def fetch_news_sentiment(symbol):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(url, params=params)
    news_data = response.json()
    if "feed" in news_data:
        return news_data["feed"]
    else:
        raise ValueError("No news sentiment data available.")


def generate_recommendation(symbol, forecasted_price, news_sentiment):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = (
        f"Given the forecasted stock price of {symbol} is ${forecasted_price:.2f} "
        f"and the recent news sentiment is: {news_sentiment}. "
        "What investment action would you recommend?"
    )
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content