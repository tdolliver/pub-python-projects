# pub-python-projects
Some example programs made in python

amazon-price-tracker:
This is a simple Amazon web scraper that will visit a specificed URL, and send a text when the price is below a specified target price. 
SMS sent using Twilio API

flight-deals:
This program will pull information from an existing google sheet using sheetyand check current flight prices compared to threshold set in the google sheet 
it will send an SMS with Twilio if current prices are lower then threshold

spotify-top100:
This program will ask a user for a date (YYYY-MM-DD)It will then scrape billboard.com's hot-100 chart for the specific date.
Finally it will use the Spotify API and create a private playlist of the hot-100 list.

stock-news-alert:
This program will query a stock market data API (alphavantage.co) for a specific (hardcoded) stock.
If the stock has had a price fluctuation over a specified (hardcoded) threshold in the last day
it will use the twilio API to send a text message to a specified phone number with the stock change
as well as the top three news stories related to the company (newsapi.org)
