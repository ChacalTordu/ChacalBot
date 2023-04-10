import discord
from discord.ext import commands
import json

# Lire les configurations à partir du fichier config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Créer une instance de la classe Intents avec les intents nécessaires
intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True
intents.message_content = True #v2

# Initialiser le bot avec les configurations lues
bot = commands.Bot(command_prefix=config['command_prefix'], intents=intents)

# Événement de connexion du bot Discord
@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name} ({bot.user.id})')

# Commande personnalisée "chacal"
@bot.command()
async def chacal(ctx):
    await ctx.send("Chacal présent")

@bot.command()
async def creetorunoi(ctx):
    await ctx.send("Veuillez entrer le nom du tournoi : ")
    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    tournoi_nom = response.content

    await ctx.send("Veuillez entrer la date et l'heure du tournoi (format : dd/mm/yyyy hh:mm) : ")
    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    tournoi_date = response.content

    await ctx.send("Veuillez entrer le nombre maximum de participants : ")
    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    tournoi_max_participants = int(response.content)

    await ctx.send("Tournoi créé : " + tournoi_nom + " le " + tournoi_date + " avec un maximum de " + str(tournoi_max_participants) + " participants.")
    
    # Créez un message récapitulatif des informations entrées par l'utilisateur
    message_recap = f"Tournoi créé : {tournoi_nom} le {tournoi_date} avec un maximum de {tournoi_max_participants} participants."

    await ctx.send(message_recap)

# Définit une commande d'aide pour le bot
@bot.command()
async def help(ctx):
    commands_list = []
    for command in bot.commands:
        commands_list.append(f"{command.name} - {command.help}")
    help_message = "Voici les commandes disponibles :\n" + "\n".join(commands_list)
    await ctx.send(help_message)
    
# Lancer le bot Discord avec le token d'identification
bot.run(config['bot_token'])