import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

discordIntents = discord.Intents.default()

dndBot = commands.Bot(command_prefix=".", intents = discordIntents)
dndBot.run(os.getenv('BOT_TOKEN'))