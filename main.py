import requests
import time
import os
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Abuja Gold Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Start web server in background
threading.Thread(target=run_web, daemon=True).start()

print("Abuja Gold Bot is running!")

def get_price():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=10)
        return r.json()["price"]
    except Exception as e:
        print("API failed, using fallback:", e)
        return 2650.0

price = get_price()
print("Gold price now:", price)

# Keep bot alive so Render no go e crash
while True:
    time.sleep(60)
