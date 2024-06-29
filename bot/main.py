import os
from dotenv import load_dotenv
from bot.bot_config import dndBot

load_dotenv()

def loadBotEvents():
    import bot.events.on_ready

def loadBotCommands():
    import bot.commands.dnd_commands
    import bot.commands.admin_commands

loadBotEvents()
loadBotCommands()

dndBot.run(os.getenv('BOT_TOKEN'))