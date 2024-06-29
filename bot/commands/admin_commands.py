import os
from dotenv import load_dotenv
from discord.ext import commands
from bot.bot_config import dndBot

load_dotenv()

@dndBot.command()
async def synchCommands(context: commands.Context):
    if context.author.id == int(os.getenv('ADMIN_ID')):
        synchronise = await dndBot.tree.sync()
        await context.reply(f"{len(synchronise)} synchronised commands")
    else:
        await context.reply("You don't have permission to use this command")