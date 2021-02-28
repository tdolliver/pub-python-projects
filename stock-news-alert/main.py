# This program will query a stock market data API (alphavantage.co) for a specific (hardcoded) stock
# If the stock has had a price fluctuation over a specified (hardcoded) threshold in the last day
# it will use the twilio API to send a text message to a specified phone number with the stock change
# as well as the top three news stories related to the company (newsapi.org)


import requests
from datetime import datetime, timedelta
from twilio.rest import Client
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_ENDPOINT = "https://www.alphavantage.co/query"
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
STOCK_NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_NEWS_API_KEY = os.getenv("STOCK_NEWS_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_API_KEY = os.getenv("TWILIO_API_KEY")
RECIPIENT_PHONE_NUMBER = "+18888888888"
PERCENT = .05

alpha_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": ALPHA_VANTAGE_API_KEY
}

## Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

alpha_response = requests.get(url=ALPHA_ENDPOINT, params=alpha_params).json()

yesterday_date = (datetime.today() - timedelta(1)).strftime('%Y-%m-%d')
day_b4_yesterday_date = (datetime.today() - timedelta(2)).strftime('%Y-%m-%d')

yesterday_data = float(alpha_response["Time Series (Daily)"][yesterday_date]["4. close"])
day_b4_yesterday_data = float(alpha_response["Time Series (Daily)"][day_b4_yesterday_date]["4. close"])
difference = yesterday_data - day_b4_yesterday_data
diff_percent = round((difference / day_b4_yesterday_data) * 100)

if difference > 0:
    is_up = "🔺"
else:
    is_up = "🔻"
print(difference)
print(day_b4_yesterday_data)
print(diff_percent)

if abs(diff_percent) > PERCENT:
    print("Get News")

    ## Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

    news_params = {
        "sortBy": "publishedAt",
        "qInTitle": COMPANY_NAME,
        "language": "en",
        "apiKey": STOCK_NEWS_API_KEY
    }

    news_response = requests.get(url=STOCK_NEWS_ENDPOINT, params=news_params).json()
    top_3_stories = news_response["articles"][:3]
    print(top_3_stories)

    ## Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_API_KEY)

    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in top_3_stories]

    initial_message = client.messages.create(
        body=f"{STOCK}: {is_up}{diff_percent}%",
        from_='+13122489697',
        to=RECIPIENT_PHONE_NUMBER
    )

    for article in formatted_articles:
        article_message = client.messages.create(
        body=article,
        from_='+13122489697',
        to=RECIPIENT_PHONE_NUMBER
    )


