import os
import json
import random
import discord
import requests
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from bot.bot_config import dndBot

load_dotenv()

character_sheets = {}

def roll_4d6():
    rolls = [random.randint(1, 6) for _ in range(4)]
    rolls.remove(min(rolls))

    return sum(rolls)

#BOT COMMANDS
@dndBot.tree.command(description="List all the races available in D&D 5e")
async def show_races(interact: discord.Interaction):
    raceUrl = f"{os.getenv('API_URL')}"

    allRaces = []

    response = requests.get(f"{raceUrl}/races")

    if response.status_code == 200:
        raceData = json.loads(response.content)

        for race in range(len(raceData['results'])):
            allRaces.append(raceData['results'][race]['name'])
        
        raceString = '\n'.join(allRaces)

        embedConfig = discord.Embed(color=1, title='D&D 5e - All Races', description=f"{raceString}")
        embedConfig.set_thumbnail(url="https://th.bing.com/th/id/OIG3.V8mtCM5vXGahqc_9NnnH?w=270&h=270&c=6&r=0&o=5&dpr=1.3&pid=ImgGn")

        await interact.response.send_message(embed=embedConfig)

@dndBot.tree.command(description="List all the classes availabe available in D&D 5e")
async def show_classes(interact: discord.Interaction):
    classUrl = f"{os.getenv('API_URL')}"

    allClasses = []

    response = requests.get(f"{classUrl}/classes")

    if response.status_code == 200:
        classData = json.loads(response.content)

        for dnd_class in range(len(classData['results'])):
            allClasses.append(classData['results'][dnd_class]['name'])
            
        classString = '\n'.join(allClasses)

        embedConfig = discord.Embed(color=1, title='D&D 5e - All Classes', description=f"{classString}")
        embedConfig.set_thumbnail(url="https://th.bing.com/th/id/OIG3.V8mtCM5vXGahqc_9NnnH?w=270&h=270&c=6&r=0&o=5&dpr=1.3&pid=ImgGn")

        await interact.response.send_message(embed=embedConfig)

@dndBot.tree.command(description="List the information for a specific class")
@app_commands.describe(class_name="The name of the chosen class")
async def dnd_class(interact: discord.Interaction, class_name: str):
    classUrl = f"{os.getenv('API_URL')}/classes/{class_name.lower()}"
    responseClass = requests.get(classUrl)

    if responseClass.status_code == 200:
        classData = json.loads(responseClass.content)

        classSubclasses = []
        classSavingThrows = []
        classProficiencies = []
        classStartEquipament = []
        classSavingThrowsName = []

        className = classData['name']
        classHitDie = classData['hit_die']
        classProficiencyChoices = classData['proficiency_choices'][0]['desc']

        for item in range(len(classData['saving_throws'])):
            classSavingThrows.append(classData['saving_throws'][item]['name'])

        for item in range(len(classData['starting_equipment'])):
            classStartEquipament.append(classData['starting_equipment'][item]['equipment']['name'])

        for item in range(len(classData['subclasses'])):
            classSubclasses.append(classData['subclasses'][item]['name'])

        for item in range(len(classSavingThrows)):
            abilityScoresUrl = f"{os.getenv('API_URL')}/ability-scores/{classSavingThrows[item].lower()}"
            responseabilityScoresUrl = requests.get(abilityScoresUrl)

            abilityScoresData = json.loads(responseabilityScoresUrl.content)
            classSavingThrowsName.append(abilityScoresData['full_name'])

        for item in range(len(classData['proficiencies'])):
            classProficiencies.append(classData['proficiencies'][item]['name'])

        embedConfig = discord.Embed(color=1, title=f'Class - **{className}**', description=f"")
        embedConfig.set_thumbnail(url="https://th.bing.com/th/id/OIG3.V8mtCM5vXGahqc_9NnnH?w=270&h=270&c=6&r=0&o=5&dpr=1.3&pid=ImgGn")

        embedConfig.add_field(name="Hit Die", value=classHitDie, inline=False)
        embedConfig.add_field(name="Saving Throws", value=classSavingThrowsName, inline=False)
        embedConfig.add_field(name="Proficiencies", value=classProficiencies, inline=False)
        embedConfig.add_field(name="Starting Equipment", value=classStartEquipament, inline=False)
        embedConfig.add_field(name="Proficiency Choices", value=classProficiencyChoices, inline=False)
        embedConfig.add_field(name="Subclasses", value=classSubclasses, inline=False)

        await interact.response.send_message(embed=embedConfig)
        
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