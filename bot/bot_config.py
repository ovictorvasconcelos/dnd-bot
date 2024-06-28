import discord
from discord.ext import commands

discordIntents = discord.Intents.default()

dndBot = commands.Bot(command_prefix="!", intents = discordIntents)