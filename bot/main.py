import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

dndBot = commands.Bot(command_prefix=".")
dndBot.run(os.getenv('BOT_TOKEN'))