import requests
import time
import telebot
from datetime import datetime

BOT_TOKEN = '8346409592:AAGQl6IYfEdoGU1w5oWKzDGpn4JaDwBGaB8'
bot = telebot.TeleBot(BOT_TOKEN)

# Binance symbol and settings
PAIR = "BTCUSDT"
INTERVAL = "1h"
LIMIT = 100

def get_klines():
    url = f"https://api.binance.com/api/v3/klines?symbol={PAIR}&interval={INTERVAL}&limit={LIMIT}"
    data = requests.get(url).json()
    closes = [float(candle[4]) for candle in data]
    return closes

def calculate_rsi(data, period=14):
    gains, losses = [], []
    for i in range(1, len(data)):
        diff = data[i] - data[i-1]
        gains.append(max(0, diff))
        losses.append(abs(min(0, diff)))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    rs = avg_gain / (avg_loss + 1e-6)
    return 100 - (100 / (1 + rs))

def send_alert(message):
    bot.send_message(chat_id="@mytradeai1_bot", text=message)

def check_rsi():
    closes = get_klines()
    rsi = calculate_rsi(closes)
    if rsi < 30:
        send_alert(f"[RSI] BUY Signal: RSI = {rsi:.2f}")
    elif rsi > 70:
        send_alert(f"[RSI] SELL Signal: RSI = {rsi:.2f}")

def main():
    while True:
        try:
            check_rsi()
            time.sleep(3600)  # 1 hour
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()