# Serenity

import sqlite3
import random
import os
import os.path
import discord
from discord.ext import commands

ownerIds = [
    185877810760515585
]
moduleDir = "modules"
dbName = "logic.db"
botToken = "MjIwNTA5MTUyNjA1MjQxMzQ1.CqhU8Q.cKKwIuQggYUQdAJOauFouAddNww"
description = """Testing version for Logician."""
startupExtensions = ["azgame","ttt","response"]

bot = commands.Bot(command_prefix="*",description=description)

@bot.event
async def on_ready():
    print("Current login: ")
    print(bot.user.name)
    print(bot.user.id)

    bot.dbName = dbName
    print("Connecting to database...")
    bot.db = sqlite3.connect(bot.dbName)
    print("Connected!")

    for extension in startupExtensions:
        try:
            # modpath = os.path.join(os.getcwd(), moduleDir, extension + ".py")
            # print(modpath)
            bot.load_extension(extension)
        except Exception as e:
            print("extension {} not loaded: ".format(extension))
            print(e)

    print("Ready to begin!")

@bot.command()
async def loadext(extension_name: str):
    try:
        bot.load_extension(extension_name)
    except Exception as e:
        print(e)
        await bot.say("Failed to load extension `{}`.".format(extension_name))
        return
    print("Successfully loaded extension {}.".format(extension_name))
    await bot.say("Loaded extension `{}`.".format(extension_name))

@bot.command()
async def unloadext(extension_name: str):
    bot.unload_extension(extension_name)
    print("Unloaded " + extension_name)
    await bot.say("Unloaded extension `{}`.".format(extension_name))

@bot.command()
async def reloadext(extension_name: str):
    bot.unload_extension(extension_name)
    try:
        bot.load_extension(extension_name)
    except Exception as e:
        print(e)
        await bot.say("Failed to load extension `{}`.".format(extension_name))
        return
    await bot.say("Reloaded extension `{}`.".format(extension_name))

@bot.command()
async def echo(msg : str):
    """Echoes the given string."""
    print("Command received: echo {}".format(msg))
    await bot.say(msg)


bot.run(botToken)
