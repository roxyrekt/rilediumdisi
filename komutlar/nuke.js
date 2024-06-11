import discord
from discord.ext import commands

class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='nuke')
    async def nuke(self, ctx):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("You do not have permission to use this command.")
            return

        channel = ctx.channel
        category = channel.category
        position = channel.position
        overwrites = channel.overwrites
        name = channel.name

        await channel.delete()

        new_channel = await category.create_text_channel(name, position=position, overwrites=overwrites)
        await ctx.send(f"Channel '{name}' has been nuked!")

def setup(bot):
    bot.add_cog(Nuke(bot))
