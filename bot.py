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
bot.load_extension("commands.steamid")

keep_alive()

# Botu çalıştırma
bot.run(discord_token)
