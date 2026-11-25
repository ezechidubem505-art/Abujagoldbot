import time, requests, yfinance as yf
import os
from flask import Flask
import threading

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

@app.route('/test')
def test():
    send("✅ TEST - Bot dey work! If you see this, Telegram dey connect.")
    return "Test sent!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
        print(f"Telegram sent: {r.status_code} - {msg[:50]}")
    except Exception as e:
        print(f"Send fail: {e}")

send("✅ Abujagoldbot don start! Watching GOLD. Drop $2 = BUY")

last_high = None
in_trade = False
buy_price = 0

while True:
    try:
        ticker = yf.Ticker("GC=F")
        data = ticker.history(period="1d", interval="1m")
        if data.empty:
            print("No data from Yahoo")
            time.sleep(60)
            continue
        price = float(data['Close'].iloc[-1])
        print(f"Price check: ${price:.2f} | High: {last_high}")

        if last_high is None:
            last_high = price
        if price > last_high:
            last_high = price

        # CHANGE AM TO $2 SO E GO FAST
        if not in_trade and price <= last_high - 2:
            send(f"🟢 ABUJAGOLDBOT: BUY NOW\nGold don drop!\nPrice: ${price:.2f}\nGo MT5 -> XAUUSD -> BUY 0.01 lot\nTake Profit: ${price+8:.2f} | Stop Loss: ${price-20:.2f}")
            in_trade = True
            buy_price = price

        if in_trade and price >= buy_price + 8:
            send(f"🔴 ABUJAGOLDBOT: SELL NOW\nTake Profit!\nPrice: ${price:.2f}\nYou buy for: ${buy_price:.2f}\nGo MT5 -> Close your BUY")
            in_trade = False
            last_high = price

        if in_trade and price <= buy_price - 20:
            send(f"⚠️ ABUJAGOLDBOT: CLOSE NOW - STOP LOSS\nPrice: ${price:.2f}\nTo protect your $3000 demo")
            in_trade = False
            last_high = price

        time.sleep(60)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)
