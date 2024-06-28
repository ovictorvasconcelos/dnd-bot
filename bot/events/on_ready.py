from bot.bot_config import dndBot

@dndBot.event
async def on_ready():
    print('BOT successfully initialised! Ready to use...')