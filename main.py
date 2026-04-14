import telebot
from flask import Flask
from threading import Thread

# --- שרת למניעת קריסה ב-Render ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive and Running"

def run(): app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- הגדרות הבוט עם הטוקן החדש ---
API_TOKEN = '8788411826:AAEQdmRx5OVFB91zjRJrEaMJFghDp8Tayg0' 
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = telebot.types.KeyboardButton("📍 שלח מיקום למציאת חנויות", request_location=True)
    markup.add(button)
    bot.reply_to(message, "אהלן! שלח מיקום ואשלח לך קישורים ישירים לקסטרו, פוט לוקר ועוד - ללא שגיאות אימות.", reply_markup=markup)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    lat = message.location.latitude
    lon = message.location.longitude
    
    # קישורים חכמים שעוקפים את הצורך ב-API Key של גוגל
    search_msg = (
        f"✅ המיקום התקבל! הנה מה שקרוב אליך:\n\n"
        f"👟 *פוט לוקר:* [לחץ כאן לחיפוש וניווט](https://www.google.com/maps/search/Foot+Locker/@{lat},{lon},15z)\n\n"
        f"👕 *קסטרו:* [לחץ כאן לחיפוש וניווט](https://www.google.com/maps/search/Castro/@{lat},{lon},15z)\n\n"
        f"👖 *פוקס:* [לחץ כאן לחיפוש וניווט](https://www.google.com/maps/search/FOX/@{lat},{lon},15z)\n\n"
        f"🍔 *מקדונלדס:* [לחץ כאן לחיפוש וניווט](https://www.google.com/maps/search/McDonalds/@{lat},{lon},15z)"
    )
    
    bot.reply_to(message, search_msg, parse_mode="Markdown")

if __name__ == "__main__":
    keep_alive() # מפעיל את השרת ששומר על הבוט בחיים
    print("--- הבוט מוכן ומחובר! ---")
    bot.infinity_polling()
