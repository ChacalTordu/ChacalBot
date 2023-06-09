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
        self.choix = ['Rocket League','League Of Legend','TFT', 'Valorant']
        self.format_tournoi = ['SoloGaming' , 'MultiGaming']
        
# -------------------------------------------------------------------------------------------------
#   AJOUTER JEU
# -------------------------------------------------------------------------------------------------    
    @commands.command(description="Ajouter un choix de jeu pour le tournoi")
    @commands.has_role(TOURNOI_ROLE)
    async def ajouter_jeu(self, ctx, jeu: str):
        self.choix.append(jeu)
        await ctx.send(f"Le jeu {jeu} a été ajouté à la liste des choix.")
# -------------------------------------------------------------------------------------------------
#   SUPPRIMER JEU
# ------------------------------------------------------------------------------------------------- 
    @commands.command(description = "Supprimer un choix de jeu")
    @commands.has_role(TOURNOI_ROLE)
    async def supprimer_jeu(self, ctx, index: int):
        if index >= 0 and index < len(self.choix):
            del self.choix[index]
            await ctx.send("Le choix de jeu a été supprimé avec succès.")
        else:
            await ctx.send("L'indice fourni est invalide.")
# -------------------------------------------------------------------------------------------------
#   REJOINDRE TOURNOI
# ------------------------------------------------------------------------------------------------- 
    @commands.command(description="Rejoindre un tournoi")
    async def rejoindre_tournoi(self, ctx, index: int):
        if index >= 0 and index < len(TOURNOIS):
            tournoi = TOURNOIS[index]
            if ctx.author in tournoi["participants"]:
                await ctx.send("Vous participez déjà à ce tournoi.")
                return
            if tournoi.get('etat') == 'En cours':
                await ctx.send("Vous ne pouvez pas rejoindre un tournoi en cours.")
                return
            tournoi["participants"].append(ctx.author)
            participants = ", ".join([participant.name for participant in tournoi["participants"]])
            # Embed message résumant le tournoi
            embed = discord.Embed(title=f"{ctx.author.name} a rejoint le tournoi {tournoi['option']}", description=f"Participants ({len(tournoi['participants'])})", color=0xFADE13)
            embed.add_field(name="Liste des participants", value=participants if participants else "Aucun participant pour le moment")
            await ctx.send(embed=embed)
        else:
            await ctx.send("L'indice fourni est invalide.")
# -------------------------------------------------------------------------------------------------
#   CREER TOURNOI
# ------------------------------------------------------------------------------------------------- 
    @commands.command(description = "Creer un tournoi")
    @commands.has_role(TOURNOI_ROLE)
    async def creer_tournoi(self, ctx):
        channel = discord.utils.get(ctx.guild.channels, name='tournois') # Les recaps sont envoyés sur un autre channel

        if any(tournoi["organisateur"] == ctx.author for tournoi in TOURNOIS):
            await ctx.send("Vous avez déjà créé un tournoi.")
            return
        if self.choix == 0 :
            await ctx.send("Veuillez rentrer au minimum un jeu dans la liste de choix de jeu grâce à la commande 'ajouter_jeu'")
        else :
            # Proposition de choix pour l'utilisateur
            format_tournoi = "\n".join([f"{i+1}. {self.format_tournoi[i]}" for i in range(len(self.format_tournoi))])
            await ctx.send(f"Veuillez choisir un format pour le tournoi en tapant le numéro correspondant :\n{format_tournoi}")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        # Attente de la réponse de l'utilisateur
        try:
            reponse = await self.bot.wait_for('message', check=check, timeout=120.0)
            choix_utilisateur = int(reponse.content) - 1
            #tournoi = {"organisateur": ctx.author, "option": self.choix[choix_utilisateur], "participants": [], "etat": "En construction"}
            tournoi = {"organisateur": ctx.author, "option": self.format_tournoi[choix_utilisateur], "participants": [], "etat": "En construction"}
            TOURNOIS.append(tournoi)

            #MONOGAMING
            if (self.format_tournoi[choix_utilisateur]==1):
                # Attente de la réponse de l'utilisateur pour définir la date et l'heure du tournoi
                proposition = "\n".join([f"{i+1}. {self.choix[i]}" for i in range(len(self.choix))]) 
                await ctx.send(f"Veuillez choisir le jeu pour le tournoi en tapant le numéro correspondant :\n{proposition}")
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                try:
                    reponse = await self.bot.wait_for('message', check=check, timeout=120.0)
                    jeu_tournoi = reponse.content
                except asyncio.TimeoutError:
                    await ctx.send("Temps écoulé, veuillez réessayer.")

            #MULTIGAMING
            else:
                # Afficher la liste des jeux et attendre la réaction de l'utilisateur
                proposition = "\n".join([f"{i+1}. {self.choix[i]}" for i in range(len(self.choix))])
                msg = await ctx.send(f"Veuillez ajouter les jeux pour le tournoi en réagissant avec les émojis correspondants :\n{proposition}")
                emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

                for i in range(len(self.choix)):
                    await msg.add_reaction(emojis[i])
                await msg.add_reaction("✅")

                def checkEmoji(reaction, user):
                    return ctx.author == user and str(reaction.emoji) in emojis + ["✅"] and msg.id == reaction.message.id

                # Attendre la réaction de l'utilisateur
                reaction, user = await self.bot.wait_for("reaction_add", check=checkEmoji)

                # Créer une liste pour stocker les indices des émojis sélectionnés
                jeux_selectionnes = []

                while str(reaction.emoji) != "✅":
                    # Ajouter l'indice de l'emoji sélectionné à la liste jeux_selectionnes
                    index = emojis.index(str(reaction.emoji))
                    jeux_selectionnes.append(self.choix[index])

                    # Attendre la prochaine réaction de l'utilisateur
                    reaction, user = await self.bot.wait_for("reaction_add", check=checkEmoji)

                # Afficher les indices des emojis sélectionnés
                await ctx.send(f"{ctx.author} a sélectionné les jeux suivants : {', '.join(map(str, jeux_selectionnes))}.")
                    
            # Attente de la réponse de l'utilisateur pour définir la date et l'heure du tournoi
            await ctx.send("Veuillez entrer la date et l'heure du tournoi au format jj/mm/aaaa hh:mm")
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                reponse = await self.bot.wait_for('message', check=check, timeout=120.0)
                date_et_heure = reponse.content
            except asyncio.TimeoutError:
                await ctx.send("Temps écoulé, veuillez réessayer.")

            # Embed message résumant le tournoi
            embed1 = discord.Embed(title=f"Tournoi créé par {ctx.author.name}", description=f"Format du tournoi : {self.format_tournoi[choix_utilisateur]}", color=0xFADE13)
            embed1.add_field(name="Participants", value="Aucun participant pour le moment")
            embed1.add_field(name="Indice du tournoi", value=str(len(TOURNOIS)-1))
            await channel.send(embed=embed1)

            # Embed message des informations du tournoi
            embed2 = discord.Embed(title=f"Informations du tournoi", color=0xFADE13)
            embed2.add_field(name="Date et heure", value=date_et_heure)
            embed2.add_field(name="Jeu choisi", value=f"{', '.join(jeux_selectionnes)}")
            embed2.set_footer(text="Récompense : Non défini pour le moment.")
            await channel.send(embed=embed2)

        except asyncio.TimeoutError:
            await ctx.send("Temps écoulé, veuillez réessayer.")

# -------------------------------------------------------------------------------------------------
#   QUITTER TOURNOI
# -------------------------------------------------------------------------------------------------
    @commands.command(description = "Quitter un tournoi")
    async def quitter_tournoi(self, ctx, index: int):
        if index >= 0 and index < len(TOURNOIS):
            participants = TOURNOIS[index]["participants"]
            if TOURNOIS[index]["etat"] == "En cours":
                await ctx.send("Vous ne pouvez pas quitter un tournoi en cours, vous pouvez seulement abandonner.")
                return
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
# -------------------------------------------------------------------------------------------------
#   ABANDON TOURNOI
# -------------------------------------------------------------------------------------------------
    @commands.command(description="Abandonner un tournoi")
    async def abandon_tournoi(self, ctx, index: int):
        # Vérifier si l'indice est valide
        if index < 0 or index >= len(TOURNOIS):
            await ctx.send("L'indice fourni est invalide.")
            return

        # Vérifier si l'utilisateur est bien inscrit dans le tournoi
        tournoi = TOURNOIS[index]
        if ctx.author not in tournoi["participants"]:
            await ctx.send("Vous n'êtes pas inscrit dans ce tournoi.")
            return

        # Demander une confirmation à l'utilisateur
        embed = discord.Embed(title=f"Abandonner le tournoi {tournoi['option']} ?", description="Réagissez avec ✅ pour confirmer, ou avec ❌ pour annuler.", color=0xFADE13)
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and reaction.message == message and str(reaction.emoji) in ["✅", "❌"]

        # Attendre la réaction de l'utilisateur
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == "✅":
                tournoi["participants"].remove(ctx.author)
                await ctx.send(f"Vous avez abandonné le tournoi {tournoi['option']}.")
            else:
                await ctx.send("Abandon annulé.")
        except asyncio.TimeoutError:
            await ctx.send("Temps écoulé, veuillez réessayer.")

        # Retirer les réactions du message pour empêcher d'autres utilisateurs de réagir
        await message.clear_reactions()
# -------------------------------------------------------------------------------------------------
#   DEMARRER TOURNOI
# -------------------------------------------------------------------------------------------------
    @commands.command(description="Démarrer un tournoi")
    async def demarrer_tournoi(self, ctx, index: int):
        if index >= 0 and index < len(TOURNOIS):
            tournoi = TOURNOIS[index]
            if ctx.author != tournoi["organisateur"]:
                await ctx.send("Vous n'êtes pas l'organisateur de ce tournoi.")
                return
            if len(tournoi["participants"]) < 2:
                await ctx.send("Le tournoi doit avoir au moins deux participants pour démarrer.")
                return
            tournoi["etat"] = "En cours"
            await ctx.send(f"Le tournoi {TOURNOIS[index]['option']} va commencer !")
        else:
            await ctx.send("L'indice fourni est invalide.")
# -------------------------------------------------------------------------------------------------
#   SUPPRIMER TOURNOI
# -------------------------------------------------------------------------------------------------
    @commands.command(description="Supprimer un tournoi")
    async def supprimer_tournoi(self, ctx, index: int):
        # Vérifier si l'indice est valide
        if index < 0 or index >= len(TOURNOIS):
            await ctx.send("L'indice fourni est invalide.")
            return
        
        # Vérifier si l'auteur du message est celui qui a créé le tournoi
        if ctx.author != TOURNOIS[index]["organisateur"]:
            await ctx.send(f"Seul {TOURNOIS[index]['organisateur'].mention} est autorisé à supprimer ce tournoi.")
            return
        
        # Supprimer le tournoi de la liste des tournois
        del TOURNOIS[index]
        await ctx.send(f"Le tournoi numéro {index} a été supprimé avec succès.")


async def setup(bot):
    await bot.add_cog(Tournament(bot))
    print('Cogs tournament setup')
    


