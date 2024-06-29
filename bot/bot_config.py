import discord
from discord.ext import commands

discordIntents = discord.Intents.default()

#PERMISSIONS
discordIntents.members = True
discordIntents.message_content = True

dndBot = commands.Bot(command_prefix="!", intents = discordIntents)