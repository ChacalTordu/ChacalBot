import os
import discord
from discord.ext import commands
import json
import asyncio

# Lire les configurations à partir du fichier config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Créer une instance de la classe Intents avec les intents nécessaires
intents = discord.Intents.all()

# Initialiser le bot avec les configurations lues
bot = commands.Bot(command_prefix=config['command_prefix'], intents=intents)

# Événement de connexion du bot Discord
@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name} ({bot.user.id})')

async def load_cogs():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')
            print(f'Loaded cog: {file[:-3]}')

loop = asyncio.get_event_loop()
loop.run_until_complete(load_cogs())

# Lancer le bot Discord avec le token d'identification
bot.run(config['bot_token'])