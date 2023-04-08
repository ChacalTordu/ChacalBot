import discord
from discord.ext import commands

class participant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.participants = []

    @commands.command()
    async def rejoindre(self, ctx):
        """
        Commande pour inscrire un joueur à la liste des participants
        """
        self.participants.append(ctx.author.name)
        await ctx.author.send(f"Vous avez été inscrit au tournoi dans le ChacalDiscord. Participants actuels : {', '.join(self.participants)}")

    @commands.command()
    async def quitter(self, ctx):
        """
        Commande pour désinscrire un joueur de la liste des participants
        """
        try:
            self.participants.remove(ctx.author.name)
            await ctx.author.send("Vous avez été désinscrit du tournoi dans le ChacalDiscord.")
        except ValueError:
            await ctx.author.send("Vous n'êtes pas inscrit au tournoi dans le ChacalDiscord.")

    @commands.command()
    async def liste(self, ctx):
        """
        Commande pour afficher la liste des participants inscrits
        """
        await ctx.author.send(f"Participants inscrits : {', '.join(self.participants)}")