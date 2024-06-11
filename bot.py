import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

# .env dosyasını yükle
load_dotenv()

# Discord tokenini al
discord_token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Komutları yükle
async def load_extensions():
    await bot.load_extension("commands.steamid")

@bot.event
async def on_ready():
    await load_extensions()
    await bot.tree.sync()  # Slash komutlarını senkronize et
    print(f"Logged in as {bot.user}")

keep_alive()

# Botu çalıştırma
bot.run(discord_token)
