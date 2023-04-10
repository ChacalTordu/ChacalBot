import discord
from discord.ext import commands
import json
import asyncio 
import __future__
import interactions

# Lire les configurations à partir du fichier config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Créer une instance de la classe Intents avec les intents nécessaires
intents = discord.Intents.all()

# Initialiser le bot avec les configurations lues
bot = commands.Bot(command_prefix=config['command_prefix'], intents=intents)

# Configuration du bot
PREFIX = "!"
TOURNOI_ROLE = "💵CHACAL VIP💵" # Nom du rôle qui peut créer un tournoi
TOURNOIS = [] # Liste des tournois en cours

class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command()
    async def test(self, ctx: interactions.CommandContext, text: str):
        await ctx.send(f"Vous avez ecrit : {text}")

    # Commande pour créer un tournoi
    @commands.command(description = "Creer un tournoi")
    @commands.has_role(TOURNOI_ROLE)
    async def creer_tournoi(self, ctx):
        # Proposition de choix pour l'utilisateur
        choix = ["choix 1", "choix 2", "choix 3"]
        proposition = "\n".join([f"{i+1}. {choix[i]}" for i in range(len(choix))])
        await ctx.send(f"Veuillez choisir une option pour le tournoi en tapant le numéro correspondant :\n{proposition}")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        # Attente de la réponse de l'utilisateur
        try:
            reponse = await self.bot.wait_for('message', check=check, timeout=60.0)
            choix_utilisateur = int(reponse.content) - 1
            tournoi = {"organisateur": ctx.author, "option": choix[choix_utilisateur], "participants": []}
            TOURNOIS.append(tournoi)
            # Embed message résumant le tournoi
            embed = discord.Embed(title=f"Tournoi créé par {ctx.author.name}", description=f"Option choisie : {choix[choix_utilisateur]}", color=0xFADE13)
            embed.add_field(name="Participants", value="Aucun participant pour le moment")
            await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            await ctx.send("Temps écoulé, veuillez réessayer.")

async def setup(bot):
    await bot.add_cog(Tournament(bot))
    print('Cogs tournament setup')
    



