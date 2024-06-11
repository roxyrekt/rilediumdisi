import discord
from discord.ext import commands

class OdaAyar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='odaayarları')
    async def manage_channel_settings(self, ctx, setting: str, value: str):
        if ctx.channel.id != YOUR_MANAGEMENT_CHANNEL_ID:
            await ctx.send("Bu komut sadece yönetim kanalında kullanılabilir.")
            return

        author_id = ctx.author.id
        if author_id not in created_channels:
            await ctx.send("Önce bir özel oda oluşturmalısınız.")
            return

        channel_id = created_channels[author_id]
        channel = ctx.guild.get_channel(channel_id)
        if setting == 'isim':
            await channel.edit(name=value)
            await ctx.send(f"Oda adı başarıyla '{value}' olarak değiştirildi.")
        elif setting == 'kapalı':
            await channel.set_permissions(ctx.guild.default_role, connect=False)
            await ctx.send("Oda başarıyla kilitlendi.")
        elif setting == 'açık':
            await channel.set_permissions(ctx.guild.default_role, connect=True)
            await ctx.send("Oda başarıyla açıldı.")
        else:
            await ctx.send("Geçersiz ayar veya değer.")

def setup(bot):
    bot.add_cog(OdaAyar(bot))
