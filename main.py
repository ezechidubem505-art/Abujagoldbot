import time, requests, yfinance as yf
import osfrom flask import Flask
import threading

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

send("✅ Abujagoldbot don start! Watching GOLD for Buy Low Sell High. Demo $3000, Lot 0.01")

last_high = None
in_trade = False
buy_price = 0

while True:
    try:
        data = yf.download("GC=F", period="1d", interval="1m", progress=False)
        price = float(data['Close'].iloc[-1])

        if last_high is None:
            last_high = price
        if price > last_high:
            last_high = price

        if not in_trade and price <= last_high - 5:
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
        print(e)
        time.sleep(60)
