import discord
from discord.ext import commands
from discord.ext.tasks import loop
import datetime
import os
import asyncio
import json
from dotenv import load_dotenv
import re
from cogs.GeneralFunctions.string_formatters import title_format


client = commands.Bot(command_prefix=YOUR PREFIX HERE)
client.remove_command('help')
cwd = os.getcwd()
global bot_name


def load_cogs(load_type):
    try:
        load_cog_title = title_format(f"{bot_name}: {load_type} Load")
    except:
        load_cog_title = title_format(f"Bot: {load_type} Load")
    print(load_cog_title[0])
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")
            print(f"{datetime.datetime.now()}   ||   {filename[:-3]} Loaded")
    print(load_cog_title[1])


def unload_cogs(load_type):
    try:
        unload_cog_title = title_format(f"{bot_name}: {load_type} Unload")
    except:
        unload_cog_title = title_format(f"Bot: {load_type} Unload")
    print(unload_cog_title[0])
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.unload_extension(f"cogs.{filename[:-3]}")
            print(f"{datetime.datetime.now()}   ||   {filename[:-3]} Unloaded")
    print(unload_cog_title[1])


def reload_cogs(load_type):
    try:
        reload_cog_title = title_format(f"{bot_name}: {load_type} Reload")
    except:
        reload_cog_title = title_format(f"Bot: {load_type} Reload")
    print(reload_cog_title[0])
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.unload_extension(f"cogs.{filename[:-3]}")
            print(f"{datetime.datetime.now()}   ||   {filename[:-3]} Unloaded")
            client.load_extension(f"cogs.{filename[:-3]}")
            print(f"{datetime.datetime.now()}   ||   {filename[:-3]} loaded")
    print(reload_cog_title[1])



@client.event
async def on_ready():
    global bot_name
    bot_name = re.search('^[^#]*', str(client.user)).group(0)
    debug_title_ready = title_format(f"{bot_name}: Main")
    print(debug_title_ready[0])
    print(f"{datetime.datetime.now()}   ||   {client.user} is ready!")
    print(debug_title_ready[1])


load_cogs("Initial")


@client.event
async def on_disconnect():
    debug_title_disconnect = title_format(f"{bot_name}: Disconnected")
    print(debug_title_disconnect[0])
    print(f"{datetime.datetime.now()}   ||   {client.user} disconnected from Discord")
    print(debug_title_disconnect[1])


@client.event
async def on_connect():
    await asyncio.sleep(5)
    debug_title_connect = title_format(f"{bot_name}: Connected")
    print(debug_title_connect[0])
    print(f"{datetime.datetime.now()}   ||   {client.user} connected to Discord")
    print(debug_title_connect[1])


@client.event
async def on_guild_join(guild):
    debug_title_join = title_format(f"{bot_name}: Added to Guild")
    print(debug_title_join[0])
    with open(f"{cwd}\\cogs\\ServerProperties\\ServerSettings.json", "r") as settingsJson:
        settings = json.load(settingsJson)

    with open(f"{cwd}\\cogs\\ServerProperties\\properties.json", "r") as propertiesJson:
        properties = json.load(propertiesJson)

    # --- Server settings here

    # ------------------------

    # --- Server properties here

    # --------------------------

    # --- setting variables to insert the settings and properties
    settings[str(guild.id)] = {}
    properties[str(guild.id)] = {}
    # -----------------------------------------------------------

    with open(f"{cwd}\\cogs\\ServerProperties\\ServerSettings.json", "w") as settingsJson:
        json.dump(settings, settingsJson, indent=4)

    with open(f"{cwd}\\cogs\\ServerProperties\\properties.json", "w") as propertiesJson:
        json.dump(properties, propertiesJson, indent=4)

    print(f"{datetime.datetime.now()}   ||   {client.user} added to guild: {guild.id}")
    print(debug_title_join[1])


@client.event
async def on_guild_remove(guild):
    debug_title_remove = title_format(f"{bot_name}: Removed from Guild")
    print(debug_title_remove[0])
    with open(f"{cwd}\\cogs\\ServerProperties\\ServerSettings.json", "r") as settingsJson:
        settings = json.load(settingsJson)

    with open(f"{cwd}\\cogs\\ServerProperties\\properties.json", "r") as propertiesJson:
        properties = json.load(propertiesJson)

    # --- deletes the guild from the json
    settings.pop(str(guild.id))
    properties.pop(str(guild.id))
    # -----------------------------------

    with open(f"{cwd}\\cogs\\ServerProperties\\ServerSettings.json", "w") as settingsJson:
        json.dump(settings, settingsJson, indent=4)

    with open(f"{cwd}\\cogs\\ServerProperties\\properties.json", "w") as propertiesJson:
        json.dump(properties, propertiesJson, indent=4)

    print(f"{datetime.datetime.now()}   ||   {client.user} removed from guild: {guild.id}")
    print(debug_title_remove[1])


# --- As it says auto reloads the cogs
@loop(hours=5)
async def auto_reload():
    reload_cogs("Auto")
# ------------------------------------


@client.command(aliases=["invite", "Invite"])
async def create_invite(ctx):
    debug_title_invite = title_format(f"{bot_name}: Invite Link")
    print(debug_title_invite[0])
    data = await client.application_info()
    link = discord.utils.oauth_url(client_id=data.id, permissions=discord.Permissions(8)) # --- Permissions are what your bot needs to function properly

    invite_embed = discord.Embed(title=f"{bot_name} Invite", color=discord.Color.from_rgb(247, 55, 24))
    invite_embed.add_field(name="Link", value=link).add_field(name="Permissions", value="- Administrator") # This is here to tell the user what the bot needs and give them the link
    await ctx.send(embed=invite_embed)

    print(f"{datetime.datetime.now()}   ||   Invite link created in {ctx.guild.id}")
    print(debug_title_invite[1])


# --- Replaces normal help command, can use short to access the users perms and give them a perm specific help message
@client.command(aliases=["help", "Help", "HELP"])
async def discord_help(ctx):
    short = ctx.author.guild_permissions

    help_embed = discord.Embed(title=f"{bot_name} help",
                               description=f"Just some info on how to use {bot_name}",
                               colour=discord.Colour.from_rgb(26, 255, 0)
                               )

    await ctx.author.send(embed=help_embed)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

auto_reload.start()
client.run(TOKEN)