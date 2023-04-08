import discord
from discord.ext import commands

class MyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rejoindre(self, ctx):
        await ctx.author.send("Vous avez rejoint le tournoi")

def setup(bot):
    bot.add_cog(MyCommands(bot))
