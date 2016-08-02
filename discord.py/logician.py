# Serenity/Logician

import sqlite3
import random
import os
import os.path
import discord
from discord.ext import commands

ownerIds = [
    185877810760515585
]
dbName = "logic.db"
botToken = "MjE1MjIzNTQxNjMxNjgwNTEy.Cqwnrg.70AtEEUSDdLIJPSbiBMyu3-jgUQ"
subToken = "MjIwNTA5MTUyNjA1MjQxMzQ1.CqzjCg.8nbVlfQxTxcQhhFBG0hGZGbBqZ4"
startupExtensions = ["azgame","ttt","response","status","admin"]

token = botToken
if token == botToken:
    description = """A simple bot for Discord."""
    prefix = "$"
else:
    description = """Testing version for Logician."""
    prefix = "*"

bot = commands.Bot(command_prefix=prefix,description=description)

@bot.event
async def on_ready():
    print("Current login: ")
    print(bot.user.name)
    print(bot.user.id)
    print("Prefix: " + prefix)
    print("Owners: " + str(ownerIds))
    bot.owners = ownerIds

    bot.dbName = dbName
    print("Connecting to database...")
    bot.db = sqlite3.connect(bot.dbName)
    print("Connected!")

    for extension in startupExtensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print("extension {} not loaded: ".format(extension))
            print("{}: {}".format(type(e).__name__,e))

    print("Ready to begin!")

@bot.command()
async def echo(msg : str):
    """Echoes the given string."""
    print("Command received: echo {}".format(msg))
    await bot.say(msg)


bot.run(token)
