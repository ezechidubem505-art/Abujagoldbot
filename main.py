import requests
import time

print("Abuja Gold Bot is running")

def get_price():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=10)
        return r.json()["price"]
    except Exception as e:
        print("Price API failed, using fallback:", e)
        return 2650.0

price = get_price()
print("Gold price now:", price)

# Keep bot alive so Render no go say e crash
while True:
    time.sleep(60)
