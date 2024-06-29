import os
import json
import random
import requests
from dotenv import load_dotenv
from discord.ext import commands
from bot.bot_config import dndBot

load_dotenv()

character_sheets = {}

def roll_4d6():
    rolls = [random.randint(1, 6) for _ in range(4)]
    rolls.remove(min(rolls))

    return sum(rolls)

#BOT COMMANDS
@dndBot.command(name='show_races', help='Show all races in D&D 5e')
async def show_races(context: commands.Context, *, race_name):
    raceUrl = f"{os.getenv('API_URL')}"

    allRaces = []

    response = requests.get(f"{raceUrl}/races")

    if response.status_code == 200:
        raceData = json.loads(response.content)

        for race in range(len(raceData['results'])):
            allRaces.append(raceData['results'][race]['name'])
            
        raceString = '\n'.join(allRaces)

        await context.reply(f'**D&D 5e - All Races**\n\n{raceString}')


@dndBot.command(name='class', aliases=['classe'], help='Show information about a class')
async def dnd_class(context: commands.Context, *, class_name):
    classUrl = f"{os.getenv('API_URL')}/classes/{class_name.lower()}"
    response = requests.get(classUrl)

    if response.status_code == 200:
        classData = json.loads(response.content)

        classStartEquipament = []
        classDescription = classData['proficiency_choices'][0]['desc']

        for item in range(len(classData['starting_equipment'])):
            classStartEquipament.append(classData['starting_equipment'][item]['equipment']['name'])

        await context.reply(f'Class - **{classData['name']}**\n\nStart Equipament: {classStartEquipament}')
    else:
        await context.send(f'Could not find information about the class "{class_name}".')
    


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