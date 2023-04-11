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
PREFIX = config['command_prefix']
TOURNOI_ROLE = "💵CHACAL VIP💵" # Nom du rôle qui peut créer un tournoi
TOURNOIS = [] # Liste des tournois en cours

class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.choix = ['jeu_de_puceau','suce_mon_chibre','TFT']
    
    @commands.command(description="Ajouter un choix de jeu pour le tournoi")
    @commands.has_role(TOURNOI_ROLE)
    async def ajouter_jeu(self, ctx, jeu: str):
        self.choix.append(jeu)
        await ctx.send(f"Le jeu {jeu} a été ajouté à la liste des choix.")

    @commands.command(description = "Supprimer un choix de jeu")
    @commands.has_role(TOURNOI_ROLE)
    async def supprimer_jeu(self, ctx, index: int):
        if index >= 0 and index < len(self.choix):
            del self.choix[index]
            await ctx.send("Le choix de jeu a été supprimé avec succès.")
        else:
            await ctx.send("L'indice fourni est invalide.")

    @commands.command(description = "Creer un tournoi")
    @commands.has_role(TOURNOI_ROLE)
    async def creer_tournoi(self, ctx):
        if any(tournoi["organisateur"] == ctx.author for tournoi in TOURNOIS):
            await ctx.send("Vous avez déjà créé un tournoi.")
            return

        # Proposition de choix pour l'utilisateur
        proposition = "\n".join([f"{i+1}. {self.choix[i]}" for i in range(len(self.choix))]) # Modification : utiliser la liste des choix de jeu
        await ctx.send(f"Veuillez choisir une option pour le tournoi en tapant le numéro correspondant :\n{proposition}")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        # Attente de la réponse de l'utilisateur
        try:
            reponse = await self.bot.wait_for('message', check=check, timeout=60.0)
            choix_utilisateur = int(reponse.content) - 1
            tournoi = {"organisateur": ctx.author, "option": self.choix[choix_utilisateur], "participants": []}
            TOURNOIS.append(tournoi)
            # Embed message résumant le tournoi
            embed = discord.Embed(title=f"Tournoi créé par {ctx.author.name}", description=f"Option choisie : {self.choix[choix_utilisateur]}", color=0xFADE13)
            embed.add_field(name="Participants", value="Aucun participant pour le moment")
            await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            await ctx.send("Temps écoulé, veuillez réessayer.")

    @commands.command(description = "Rejoindre un tournoi")
    async def rejoindre_tournoi(self, ctx, index: int):
        if index >= 0 and index < len(TOURNOIS):
            TOURNOIS[index]["participants"].append(ctx.author)
            participants = ", ".join([participant.name for participant in TOURNOIS[index]["participants"]])
            # Embed message résumant le tournoi
            embed = discord.Embed(title=f"{ctx.author.name} a rejoint le tournoi {TOURNOIS[index]['option']}", description=f"Participants ({len(TOURNOIS[index]['participants'])})", color=0xFADE13)
            embed.add_field(name="Liste des participants", value=participants if participants else "Aucun participant pour le moment")
            await ctx.send(embed=embed)
        else:
            await ctx.send("L'indice fourni est invalide.")


    @commands.command(description = "Quitter un tournoi")
    async def quitter_tournoi(self, ctx, index: int):
        if index >= 0 and index < len(TOURNOIS):
            participants = TOURNOIS[index]["participants"]
            if ctx.author in participants:
                participants.remove(ctx.author)
                # Embed message résumant le tournoi
                embed = discord.Embed(title=f"{ctx.author.name} a quitté le tournoi {TOURNOIS[index]['option']}", description=f"Participants ({len(TOURNOIS[index]['participants'])})", color=0xFADE13)
                embed.add_field(name="Liste des participants", value=", ".join([participant.name for participant in participants]) if participants else "Aucun participant pour le moment")
                await ctx.send(embed=embed)
            else:
                await ctx.send("Vous ne participez pas à ce tournoi.")
        else:
            await ctx.send("L'indice fourni est invalide.")

async def setup(bot):
    await bot.add_cog(Tournament(bot))
    print('Cogs tournament setup')
    


