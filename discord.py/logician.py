# Let's do this shit.
import random
import discord
from discord.ext import commands

ownerIds = [
    185877810760515585
]
db_name = "logic.db"
botToken = "MjIwNTA5MTUyNjA1MjQxMzQ1.CqhU8Q.cKKwIuQggYUQdAJOauFouAddNww"
description = """Testing version for Logician."""
startupExtensions = ["azgame","ttt"]

bot = commands.Bot(command_prefix="*",description=description)

@bot.event
async def on_ready():
    print("Current login: ")
    print(bot.user.name)
    print(bot.user.id)

    for extension in startupExtensions:
        try:
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
    bot.load_extension(extension_name)
    await bot.say("Reloaded extension `{}`.".format(extension_name))

@bot.command(pass_context = True)
async def doyouloveme(cxt, phrase : str):
    """Asks if you are loved."""
    # if phrase == "Do you love me?" or phrase == "Do you love me":
    #    if cxt

@bot.command()
async def echo(msg : str):
    """Echoes the given string."""
    print("Command received: echo {}".format(msg))
    await bot.say(msg)

@bot.command()
async def logic(msg : str):
    if str == "Who's the best?!" or str == "Who's the best!?":
        await bot.say("***LOOOOGICIAN!***")
    else:
        await bot.say("No.")

bot.run(botToken)
