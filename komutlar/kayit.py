from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

class Kayit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kayit')
    async def kayit(self, ctx, ip: str):
        raw_url = 'https://rentry.co/katroxipler/raw'
        edit_url = 'https://rentry.co/katroxipler/edit'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        edit_code = os.getenv('RENRY_EDIT_CODE')  # .env dosyasından edit kodunu al

        async with aiohttp.ClientSession() as session:
            # Önce mevcut içeriği al
            async with session.get(raw_url) as response:
                if response.status == 200:
                    content = await response.text()
                else:
                    await ctx.send('Mevcut içeriği alırken bir hata oluştu.')
                    return

            # IP zaten var mı kontrol et
            if ip in content:
                await ctx.send(f'IP adresi zaten mevcut: {ip}')
                return

            # Yeni IP'yi ekle
            new_content = content + '\n' + ip

            # Edit sayfasını al
            async with session.get(edit_url) as response:
                if response.status == 200:
                    text = await response.text()
                    soup = BeautifulSoup(text, 'html.parser')
                    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
                else:
                    await ctx.send('Edit sayfasını alırken bir hata oluştu.')
                    return

            # Yeni içeriği güncelle
            payload = {
                'csrfmiddlewaretoken': csrf_token,
                'text': new_content,
                'edit_code': edit_code,
                'new_edit_code': '',
                'new_url': '',
                'new_modify_code': ''
            }

            async with session.post(edit_url, headers=headers, data=payload) as response:
                if response.status == 200:
                    await ctx.send(f'IP adresi başarıyla eklendi: {ip}')
                else:
                    await ctx.send(f'IP adresi eklenirken bir hata oluştu: {response.status}')

def setup(bot):
    bot.add_cog(Kayit(bot))