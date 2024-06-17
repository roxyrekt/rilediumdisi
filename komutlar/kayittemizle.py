from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

class KayitTemizle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kayittemizle')
    @commands.has_permissions(administrator=True)
    async def kayittemizle(self, ctx):
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

            # İçeriği temizle
            payload = {
                'csrfmiddlewaretoken': csrf_token,
                'text': '',
                'edit_code': edit_code,
                'new_edit_code': '',
                'new_url': '',
                'new_modify_code': ''
            }

            try:
                async with session.post(edit_url, headers=headers, data=payload) as response:
                    if response.status == 200:
                        await ctx.send('Tüm IP adresleri başarıyla temizlendi.')
                    else:
                        await ctx.send(f'IP adresleri temizlenirken bir hata oluştu: {response.status}')
            except Exception as e:
                await ctx.send(f'IP adresleri temizlenirken bir hata oluştu: {e}')

async def setup(bot):
    await bot.add_cog(KayitTemizle(bot))
