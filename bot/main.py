import os
from dotenv import load_dotenv
from bot.bot_config import dndBot

load_dotenv()

def loadBotEvents():
    import bot.events.on_ready

loadBotEvents()

dndBot.run(os.getenv('BOT_TOKEN'))