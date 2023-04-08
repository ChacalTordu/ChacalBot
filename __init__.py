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

# Charger les commandes personnalisées
bot.load_extension('cog_listing')

# Événement de connexion du bot Discord
@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name} ({bot.user.id})')

# Commande personnalisée "chacal"
@bot.command()
async def chacal(ctx):
    await ctx.send("Chacal présent")

# Lancer le bot Discord avec le token d'identification
bot.run(config['bot_token'])
