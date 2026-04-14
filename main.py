import telebot
from flask import Flask
from threading import Thread

# --- שרת למניעת קריסה ב-Render (Free Tier) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive"

def run(): app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- הגדרות הבוט (כאן התיקון) ---
# חשוב: תוודא שאתה מעתיק את הטוקן בדיוק כפי שקיבלת מה-BotFather
API_TOKEN = '7611598236:AAFl9uS5i69F6Y5-W4e63eW4e63eW4e63e' 
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = telebot.types.KeyboardButton("📍 שלח מיקום למציאת חנויות", request_location=True)
    markup.add(button)
    bot.reply_to(message, "אהלן! שלח מיקום ואשלח לך קישורים ישירים לפוט לוקר, קסטרו ועוד - ללא צורך באימות נוסף.", reply_markup=markup)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    lat = message.location.latitude
    lon = message.location.longitude
    
    # שימוש בקישורים שעוקפים את ה-API Key (חוסך אימות מול גוגל)
    search_msg = (
        f"✅ המיקום התקבל! הנה מה שקרוב אליך:\n\n"
        f"👟 *פוט לוקר:* [לחץ כאן לחיפוש וניווט](https://www.google.com/maps/search/Foot+Locker/@{lat},{lon},15z)\n\n"
        f"👕 *קסטרו:* [לחץ כאן לחיפוש וניווט](https://www.google.com/maps/search/Castro/@{lat},{lon},15z)\n\n"
        f"👖 *פוקס:* [לחץ כאן לחיפוש וניווט](https://www.google.com/maps/search/FOX/@{lat},{lon},15z)\n\n"
        f"🍔 *מקדונלדס:* [לחץ כאן לחיפוש וניווט](https://www.google.com/maps/search/McDonalds/@{lat},{lon},15z)"
    )
    
    bot.reply_to(message, search_msg, parse_mode="Markdown")

if __name__ == "__main__":
    keep_alive() # מפעיל את השרת שמונע מהבוט ליפול ב-Render
    print("Bot is ready!")
    bot.infinity_polling()
