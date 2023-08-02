import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla_Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "EBUQ7CLD41V4DE1U"
NEWS_API_KEY = "aef9c20205be4523baa364dbc74451ac"

TWILIO_SID = "AC46b1cc16aa75745f685e3a15c8af662e"
TWILIO_AUTH_TOKEN = "6d50d9f24909054264b16cc810a98d06"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = stock_response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = abs(float(yesterday_closing_price)-float(day_before_yesterday_closing_price))
print(difference)
diff_percent = (difference/float(yesterday_closing_price))*100
print(diff_percent)

if diff_percent > 1:

 news_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME
 }

news_response = requests.get(NEWS_ENDPOINT, params=news_params)
articles = news_response.json()["articles"]
three_articles = articles[:3] # Using slice operator to get first 3 artciles only (0->2)
print(three_articles)

formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

client = Client(TWILIO_SID,TWILIO_AUTH_TOKEN)

for article in formatted_articles:
 message = client.messages.create(
                     body=article,
                     from_='+12295973671',
                     to='+916204717753'
                 )
