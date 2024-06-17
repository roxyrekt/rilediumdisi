from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import re

# .env dosyasını yükle
load_dotenv()

class KayitSil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_valid_ip(self, ip: str) -> bool:
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if pattern.match(ip):
            return all(0 <= int(num) < 256 for num in ip.split('.'))
        return False

    @commands.command(name='kayitsil')
    @commands.has_permissions(manage_messages=True)
    async def kayitsil(self, ctx, ip: str):
        if not self.is_valid_ip(ip):
            await ctx.send(f'Geçersiz IP adresi formatı: {ip}')
            return

        raw_url = 'https://rentry.co/katroxipler/raw'
        edit_url = 'https://rentry.co/katroxipler/edit'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://rentry.co/katroxipler/edit',
        }
        edit_code = os.getenv('RENRY_EDIT_CODE')  # .env dosyasından edit kodunu al

        if not edit_code:
            await ctx.send('Edit kodu bulunamadı. Lütfen .env dosyasını kontrol edin.')
            return

        async with aiohttp.ClientSession() as session:
            # Önce mevcut içeriği al
            try:
                async with session.get(raw_url) as response:
                    if response.status == 200:
                        content = await response.text()
                    else:
                        await ctx.send('Mevcut içeriği alırken bir hata oluştu.')
                        return
            except Exception as e:
                await ctx.send(f'Mevcut içeriği alırken bir hata oluştu: {e}')
                return

            # IP var mı kontrol et
            if ip not in content:
                await ctx.send(f'IP adresi mevcut değil: {ip}')
                return

            # IP'yi içerikten sil
            new_content = '\n'.join([line for line in content.splitlines() if line.strip() != ip.strip()])

            # Edit sayfasını al
            try:
                async with session.get(edit_url) as response:
                    if response.status == 200:
                        text = await response.text()
                        soup = BeautifulSoup(text, 'html.parser')
                        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
                        if not csrf_token:
                            await ctx.send('CSRF token alınamadı. Edit sayfasını kontrol edin.')
                            return
                    else:
                        await ctx.send('Edit sayfasını alırken bir hata oluştu.')
                        return
            except Exception as e:
                await ctx.send(f'Edit sayfasını alırken bir hata oluştu: {e}')
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

            try:
                async with session.post(edit_url, headers=headers, data=payload) as response:
                    if response.status == 200:
                        await ctx.send(f'IP adresi başarıyla silindi: {ip}')
                    else:
                        await ctx.send(f'IP adresi silinirken bir hata oluştu: {response.status}')
            except Exception as e:
                await ctx.send(f'IP adresi silinirken bir hata oluştu: {e}')

async def setup(bot):
    await bot.add_cog(KayitSil(bot))
