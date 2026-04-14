import telebot
from flask import Flask
from threading import Thread

# --- שרת למניעת קריסה ב-Render ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive"

def run(): app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- הגדרת הבוט ---
API_TOKEN = '7611598236:AAFl9uS5i69F6Y5-W4e63eW4e63eW4e63e' # הטוקן שלך
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = telebot.types.KeyboardButton("📍 שלח מיקום כדי למצוא חנויות", request_location=True)
    markup.add(button)
    bot.reply_to(message, "שלום! שלח מיקום בלחיצה על הכפתור, ואשלח לך קישורים ישירים לחנויות לידך ללא צורך באימות.", reply_markup=markup)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    lat = message.location.latitude
    lon = message.location.longitude
    
    # שימוש בקישורי חיפוש ישירים (Deep Links) - עוקף את בעיית ה-API Key
    search_msg = (
        f"✅ המיקום נקלט! הנה החנויות הקרובות אליך:\n\n"
        f"👟 *פוט לוקר:* [לחץ כאן לניווט](https://www.google.com/maps/search/Foot+Locker/@{lat},{lon},15z)\n\n"
        f"👕 *קסטרו:* [לחץ כאן לניווט](https://www.google.com/maps/search/Castro/@{lat},{lon},15z)\n\n"
        f"👖 *פוקס:* [לחץ כאן לניווט](https://www.google.com/maps/search/Fox/@{lat},{lon},15z)\n\n"
        f"🍔 *מקדונלדס:* [לחץ כאן לניווט](https://www.google.com/maps/search/McDonalds/@{lat},{lon},15z)"
    )
    
    bot.reply_to(message, search_msg, parse_mode="Markdown")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
