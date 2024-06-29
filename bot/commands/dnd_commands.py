import os
import json
import random
import discord
import requests
from dotenv import load_dotenv
from discord import app_commands
from bot.bot_config import dndBot

load_dotenv()

character_sheets = {}
API_URL = os.getenv('API_URL')

def roll_4d6():
    rolls = [random.randint(1, 6) for _ in range(4)]
    rolls.remove(min(rolls))

    return sum(rolls)

def get_api_data(endpoit):
    response = requests.get(f"{API_URL}/{endpoit}")

    if response.status_code == 200:
        return json.loads(response.content)
    return None

def create_embed(title, description="", thumbnail_url=None):
    embed = discord.Embed(color=discord.Color.blue(), title=title, description=description)

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)
    return embed

@dndBot.tree.command(description="List all the races available in D&D 5e")
async def show_races(interact: discord.Interaction):
    race_data = get_api_data('races')

    if race_data:
        race_names = [race["name"] for race in race_data['results']]
        race_string = '\n'.join(race_names)

        embed_config = create_embed('D&D 5e - All Races', race_string, "https://th.bing.com/th/id/OIG3.V8mtCM5vXGahqc_9NnnH?w=270&h=270&c=6&r=0&o=5&dpr=1.3&pid=ImgGn")
        await interact.response.send_message(embed=embed_config)     

@dndBot.tree.command(description="List all the classes availabe available in D&D 5e")
async def show_classes(interact: discord.Interaction):
    class_data = get_api_data('classes')

    if class_data:
        class_names = [dndClass['name'] for dndClass in class_data['results'] ]
        class_string = '\n'.join(class_names)

        embed_config = create_embed('D&D 5e - All Classes', class_string, "https://th.bing.com/th/id/OIG3.V8mtCM5vXGahqc_9NnnH?w=270&h=270&c=6&r=0&o=5&dpr=1.3&pid=ImgGn")
        await interact.response.send_message(embed=embed_config)

@dndBot.tree.command(description="List the information for a specific class")
@app_commands.describe(class_name="The name of the chosen class")
async def dnd_class(interact: discord.Interaction, class_name: str):
    class_data = get_api_data(f"classes/{class_name.lower()}")

    if class_data:
        name = class_data['name']
        hit_die = class_data['hit_die']
        proficiency_choices = class_data['proficiency_choices'][0]['desc']
        class_saving_throws = [saving_throws['name'] for saving_throws in class_data['saving_throws']]
        start_equipment = [equipment['equipment']['name'] for equipment in class_data['starting_equipment']]
        sub_classes = [sub_class['name'] for sub_class in class_data['subclasses']]
        proficiencies = [proeficiency['name'] for proeficiency in class_data['proficiencies']]
        saving_throws_full = [get_api_data(f"ability-scores/{saving_throws.lower()}")['full_name'] for saving_throws in class_saving_throws]

        embed = create_embed(f'Class - **{class_name}**', "", "https://th.bing.com/th/id/OIG3.V8mtCM5vXGahqc_9NnnH?w=270&h=270&c=6&r=0&o=5&dpr=1.3&pid=ImgGn")
        embed.add_field(name="Hit Die", value=hit_die, inline=False)
        embed.add_field(name="Saving Throws", value=', '.join(saving_throws_full), inline=False)
        embed.add_field(name="Proficiencies", value=', '.join(proficiencies), inline=False)
        embed.add_field(name="Starting Equipment", value=', '.join(start_equipment), inline=False)
        embed.add_field(name="Proficiency Choices", value=proficiency_choices, inline=False)
        embed.add_field(name="Subclasses", value=', '.join(sub_classes), inline=False)

        await interact.response.send_message(embed=embed)

@dndBot.tree.command(description="Create a character to start the game")
@app_commands.describe(name="Your name", class_name="Your classe", race="Your race")
async def create_character(interact: discord.Interaction, name: str, class_name: str, race: str):
    user_id = interact.user.id

    user_attributes = {
        'Strengh': roll_4d6(),
        'Dexterity': roll_4d6(),
        'Constitution': roll_4d6(),
        'Intelligence': roll_4d6(),
        'Wisdom': roll_4d6(),
        'Charisma': roll_4d6()
    }
    
    character_sheets[user_id] = {
        'name': name.capitalize(),
        'race': race.capitalize(),
        'class': class_name.capitalize(),
        'level': 1,
        'attributes': user_attributes
    }

    embed = create_embed(f'D&D 5e Character - **Successfully Created!**', "", interact.user.avatar.url)

    embed.add_field(name="Player name", value=name.capitalize(), inline=False)
    embed.add_field(name="Player level", value=character_sheets[user_id]['level'], inline=False)
    embed.add_field(name="Player Race", value=race.capitalize(), inline=False)
    embed.add_field(name="Player class", value=class_name.capitalize(), inline=False)

    for attribute, value in user_attributes.items():
        embed.add_field(name=attribute, value=value, inline=True)

    await interact.response.send_message(embed=embed)

@dndBot.tree.command(description="See your character sheet")
async def view_character(interact: discord.Interaction):
    user_id = interact.user.id

    if user_id in character_sheets:
        character_profile = character_sheets[user_id]
        user_attributes = character_profile['attributes']

        embed = create_embed(f'D&D 5e Character - **{character_profile["name"]}**', "", interact.user.avatar.url)

        embed.add_field(name="Player name", value=character_profile['name'], inline=False)
        embed.add_field(name="Player level", value=character_profile['level'], inline=False)
        embed.add_field(name="Player Race", value=character_profile['race'], inline=False)
        embed.add_field(name="Player class", value=character_profile['class'], inline=False)


        for attribute, value in user_attributes.items():
            embed.add_field(name=attribute, value=value, inline=True)

        await interact.response.send_message(embed=embed)
    else:
        await interact.response.send_message("You don't have a character sheet yet. Use `/create_character` to create one.")