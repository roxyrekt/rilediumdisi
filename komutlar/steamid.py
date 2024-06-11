import re
import requests
from datetime import datetime, timezone, timedelta
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# Steam API anahtarını al
steam_api_key = os.getenv("STEAM_API_KEY")
api_key = steam_api_key

# İzin verilen kanal kimliklerini tanımlayın
allowed_channels = [1239701061179150346, 1232074719486808184]

def steam_id_to_steam_id64(steam_id):
    parts = steam_id.split(':')
    y = int(parts[1])
    z = int(parts[2])
    steam_id64 = 76561197960265728 + z * 2 + y
    return str(steam_id64)

class SteamID(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='steamid')
    async def steamid(self, ctx, steam_identifier: str):
        if ctx.channel.id not in allowed_channels:
            await ctx.send("Sadece VEGAS reisin ayarladığı kanallarda çalışır.")
            return
        
        try:
            steam_id64, steam_steamid, steam_id31 = self.process_steam_identifier(steam_identifier)
            steam_profile_url = f"https://steamcommunity.com/profiles/{steam_id64}"

            player_info = self.get_steam_profile(steam_id64)

            profile_created_unix = player_info.get('timecreated', 'Bilinmiyor')
            profile_created_human = self.convert_unix_to_turkey_time(profile_created_unix) if profile_created_unix != 'Bilinmiyor' else 'Bilinmiyor'
            profile_state = 'Açık' if player_info.get('communityvisibilitystate', 0) == 3 else 'Gizli'
            profile_name = player_info.get('personaname', 'Bilinmiyor')
            profile_location = player_info.get('loccountrycode', 'Bilinmiyor')
            profile_custom_url = player_info.get('profileurl', 'Ayarlanmamış')

            custom_url_username = self.extract_custom_url(profile_custom_url)

            message = (
                f"Komutu kullanan: {ctx.author.mention}\n"
                f"<a:ok23:1231431234907799682> **Steam Profili:** {steam_profile_url}\n"
                f"<a:ok23:1231431234907799682> **SteamID:** `{steam_steamid}`\n"
                f"<a:ok23:1231431234907799682> **SteamID3:** `{steam_id31}`\n"
                f"<a:ok23:1231431234907799682> **SteamID64:** `{steam_id64}`\n"
                f"<a:ok23:1231431234907799682> **Profil Durumu:** `{profile_state}`\n"
                f"<a:ok23:1231431234907799682> **Profil Oluşturulma Tarihi:** `{profile_created_human}`\n"
                f"<a:ok23:1231431234907799682> **Kullanıcı Adı:** `{profile_name}`\n"
                f"<a:ok23:1231431234907799682> **Konum:** `{profile_location}`\n"
                f"<a:ok23:1231431234907799682> **Özel URL:** `{custom_url_username}`"
            )

            await ctx.send(message)
        except ValueError:
            await ctx.send("Geçersiz SteamID.")
    
    def process_steam_identifier(self, steam_identifier):
        if steam_identifier.isdigit() and len(steam_identifier) == 17:
            steam_id64 = steam_identifier
            steam_id3 = str(int(steam_id64) - 76561197960265728)
            steam_id31 = f"[U:1:{steam_id3}]"
            steam_steamid = f"STEAM_0:{int(steam_id64) % 2}:{(int(steam_id64) - 76561197960265728) // 2}"
        elif steam_identifier.startswith("STEAM_"):
            steam_steamid = steam_identifier
            steam_id64 = steam_id_to_steam_id64(steam_steamid)
            steam_id3 = str(int(steam_id64) - 76561197960265728)
            steam_id31 = f"[U:1:{steam_id3}]"
        elif steam_identifier.startswith("[U:1:") and steam_identifier.endswith("]"):
            steam_id3 = steam_identifier[5:-1]
            steam_id64 = str(int(steam_id3) + 76561197960265728)
            steam_id31 = steam_identifier
            steam_steamid = f"STEAM_0:{int(steam_id64) % 2}:{(int(steam_id64) - 76561197960265728) // 2}"
        else:
            match = re.search(r'(?:id|profiles)\/(?P<id>[\w-]+)', steam_identifier)
            if match:
                identifier = match.group('id')
            else:
                identifier = steam_identifier

            if identifier.isdigit():
                steam_id64 = identifier
            else:
                response = requests.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={api_key}&vanityurl={identifier}")
                data = response.json()
                if data.get("response", {}).get("success", 0) == 1:
                    steam_id64 = data["response"]["steamid"]
                else:
                    raise ValueError("Geçersiz Steam linki veya özel URL.")

            steam_id3 = str(int(steam_id64) - 76561197960265728)
            steam_id31 = f"[U:1:{steam_id3}]"
            steam_steamid = f"STEAM_0:{int(steam_id64) % 2}:{(int(steam_id64) - 76561197960265728) // 2}"

        return steam_id64, steam_steamid, steam_id31

    def get_steam_profile(self, steam_id64):
        profile_response = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&steamids={steam_id64}")
        profile_data = profile_response.json()
        return profile_data['response']['players'][0]

    def convert_unix_to_turkey_time(self, unix_time):
        dt = datetime.utcfromtimestamp(unix_time)
        dt_turkey = dt.astimezone(timezone(timedelta(hours=3)))
        return dt_turkey.strftime('%d.%m.%Y %H:%M:%S')

    def extract_custom_url(self, profile_custom_url):
        custom_url_match = re.search(r'https?://steamcommunity\.com/id/(\w+)/', profile_custom_url)
        return custom_url_match.group(1) if custom_url_match else 'Ayarlanmamış'

async def setup(bot):
    await bot.add_cog(SteamID(bot))
