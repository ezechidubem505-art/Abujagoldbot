print("Abuja Gold Bot is running")

import requests

price = requests.get("https://data-asg.goldprice.org/dbXRates/USD").json()
gold = price['items'][0]['curr'] + " " + str(price['items'][0]['xauPrice'])
print("Gold price now: " + gold)
