from discord.ext import commands
from bot.bot_config import dndBot

@dndBot.command(name='class', aliases=['classe'], help='Show information about a class')
async def dnd_class(context: commands.Context):
    await context.reply('Oi')
    
