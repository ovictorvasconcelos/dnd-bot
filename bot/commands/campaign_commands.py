import discord
from discord.ext import commands
from bot.bot_config import dndBot
from bot.commands.dnd_commands import create_embed
from bot.commands.dnd_commands import character_sheets

@dndBot.tree.command(description="Start a simple adventure")
async def start_adventure(interact: discord.Interaction):
    user_id = interact.user.id

    if user_id in character_sheets:
        character_profile = character_sheets[user_id]
        embed = create_embed(f'Adventure D&D 5e - **{character_profile["name"]}**', "", interact.user.avatar.url)
        embed.add_field(name="Introduction", value="You enter a dark dungeon. What you want to do?", inline=False)