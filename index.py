import discord
from discord.ext import commands
import re
import requests
import os
from dotenv import load_dotenv

from keep_alive import keep_alive
keep_alive()

# .env dosyasını yükle
load_dotenv()

# Discord tokenini al
discord_token = os.getenv("DISCORD_TOKEN")

# Steam API anahtarını al
steam_api_key = os.getenv("STEAM_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Steam Web API anahtarı
api_key = steam_api_key

# steamid komutu
@bot.command(name='steamid')
async def steamid(ctx, steam_identifier: str):
    # Sadece belirli bir kanalda çalışsın
    if ctx.channel.id != 1239701061179150346:
        await ctx.send("Sadece VEGAS reisin ayarladığı kanallarda çalışır.")
        return
    
    try:
        if steam_identifier.isdigit() and len(steam_identifier) == 17:
            # SteamID64 işle
            steam_id64 = steam_identifier
            steam_id3 = str(int(steam_id64) - 76561197960265728)
            steam_id31 = f"[U:1:{steam_id3}]"
        elif steam_identifier.startswith("[U:1:") and steam_identifier.endswith("]"):
            # SteamID3 işle
            steam_id3 = steam_identifier[5:-1]
            steam_id64 = str(int(steam_id3) + 76561197960265728)
            steam_id31 = steam_identifier
        else:
            # Steam profil URL'si işle
            match = re.search(r'(?:id|profiles)\/(?P<id>\d+)', steam_identifier)
            if match:
                steam_id64 = match.group('id')
            else:
                match = re.search(r'(?:id|profiles)\/(?P<id>\w+)', steam_identifier)
                if match:
                    steam_id = match.group('id')
                    response = requests.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={api_key}&vanityurl={steam_id}")
                    data = response.json()
                    if data.get("response", {}).get("success", 0) == 1:
                        steam_id64 = data["response"]["steamid"]
                    else:
                        await ctx.send("Geçersiz Steam linki.")
                        return

            steam_id3 = str(int(steam_id64) - 76561197960265728)
            steam_id31 = f"[U:1:{steam_id3}]"
        
        steam_profile_url = f"https://steamcommunity.com/profiles/{steam_id64}"

        await ctx.send(f"Komutu kullanan: {ctx.author.mention}\n<a:ok23:1231431234907799682> **Steam Profili:** {steam_profile_url}\n<a:ok23:1231431234907799682> **SteamID3:** `{steam_id31}`\n<a:ok23:1231431234907799682> **SteamID64:** `{steam_id64}`")
    except ValueError:
        await ctx.send("Geçersiz SteamID.")

# Botu çalıştırma
bot.run(discord_token)
