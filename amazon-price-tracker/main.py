# This program will scrape a specific Amazon.com URL and compare the current displayed price
# with a hardcoded target price. It will then send an email if the current price is below the threshold.

from bs4 import BeautifulSoup
import requests
import smtplib

# Amazon requires a valid User-Agent otherwise it will be blocked
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}
my_email = "{EMAIL}"
password = "{PASSWORD}"
product_link = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"
target_price = 200.00

response = requests.get(url=product_link, headers=HEADERS)

# Use BeautifulSoup to parse the html and pull the product title and price
soup = BeautifulSoup(response.text, "html.parser")
current_price = float(soup.find(id='priceblock_ourprice').getText().split("$")[1])
product_title = soup.find(id="productTitle").getText().split('\n')
for i in product_title:
    if i != '':
        formatted_product_title = i
print(current_price)
print(formatted_product_title)

# send an email if current price is below target price
if current_price < target_price:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email,
                            msg=f"Subject:Amazon Price Alert!\n\n {formatted_product_title} is now ${current_price}\n {product_link}".encode('utf-8'))