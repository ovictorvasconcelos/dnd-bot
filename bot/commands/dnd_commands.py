import random
from discord.ext import commands
from bot.bot_config import dndBot

character_sheets = {}

def roll_4d6():
    rolls = [random.randint(1, 6) for _ in range(4)]
    rolls.remove(min(rolls))

    return sum(rolls)

@dndBot.command(name="create_character", help="Creates a sheet for a character")
async def create_character(context: commands.Context, name: str, dnd_class: str, race: str):
    userId = context.author.id

    userAttributes = {
        'Strengh': roll_4d6(),
        'Dexterity': roll_4d6(),
        'Constitution': roll_4d6(),
        'Intelligence': roll_4d6(),
        'Wisdom': roll_4d6(),
        'Charisma': roll_4d6
    }

    create_character[userId] = {
        'name': name,
        'class': dnd_class,
        'level': 1,
        'attributes': userAttributes
    }

    await context.reply(f"Character {name} the {race} {dnd_class} created successfully with attributes: {userAttributes}")

@dndBot.command(name='class', aliases=['classe'], help='Show information about a class')
async def dnd_class(context: commands.Context):
    await context.reply('Oi')
    
