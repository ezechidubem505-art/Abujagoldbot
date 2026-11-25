import os
import time
import threading
import requests
from flask import Flask
import telebot

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Abuja Gold Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

print("Abuja Gold Bot is running!")

def get_gold_price():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=10)
        return r.json()["price"]
    except Exception as e:
        print("API failed, using fallback:", e)
        return 2650.0

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome to Abuja Gold Bot! 🥇\nSend /price to see Gold price now.")

@bot.message_handler(commands=['price'])
def price(message):
    price = get_gold_price()
    bot.reply_to(message, f"Gold price now: ${price:,.2f} / oz")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, "Send /price to see Gold price. Send /start to start.")

print("Starting bot polling...")
bot.infinity_polling()
