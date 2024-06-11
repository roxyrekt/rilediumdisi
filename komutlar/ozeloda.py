import discord
from discord.ext import commands

class OzelOda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel and after.channel.id == YOUR_PRIVATE_CHANNEL_ID:
            guild = member.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=False),
                member: discord.PermissionOverwrite(connect=True, manage_channels=True),
            }
            channel = await guild.create_voice_channel(f'Özel Oda - {member.display_name}', overwrites=overwrites)
            await member.send(f"{channel.name} adında özel bir oda oluşturuldu. Diğer kullanıcıları davet edebilirsiniz.")

def setup(bot):
    bot.add_cog(OzelOda(bot))
