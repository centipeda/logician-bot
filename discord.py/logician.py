#!/usr/bin/env python3.5
# Serenity/Logician
import json
import sqlite3
import random
import os
import os.path
import traceback
import discord
from discord.ext import commands
import maintenance

config = "logic.cfg"
prefix = "$"
with open(config,'r') as cfg:
    configData = json.loads(cfg.read())

bot = commands.Bot(self_bot=False,command_prefix=prefix)
bot.shutting_down = False

@bot.event
async def on_ready():
    print("Current login: ")
    print(bot.user.name)
    print(bot.user.id)
    print("Prefix: " + configData["prefix"])
    print("Owners: " + str(configData["owner_ids"]))
    bot.owners = configData["owner_ids"]
    bot.owner = configData["owner_ids"][0]
    bot.token = configData["token"]

    bot.dbName = configData["database"]
    print("Connecting to database...")
    bot.db = sqlite3.connect(bot.dbName)
    print("Connected!")

    loaded = []
    for extension in configData["startup_extensions"]:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print("extension {} not loaded: ".format(extension))
            print("{}: {}".format(type(e).__name__,traceback.print_tb(e.__traceback__)))
        else:
            loaded.append(extension)
    print("Loaded extensions: " + ", ".join(loaded))

    print("Beginning maintenance...")
    maintenance.update(bot)
    print("Maintenance finished!")

    print("Ready to begin!")

@bot.command()
async def echo(msg : str):
    """Echoes the given string."""
    print("Command received: echo {}".format(msg))
    await bot.say(msg)

@bot.command(pass_context = True)
async def uid(ctx, user : discord.User=None):
    if user is not None:
        await bot.say(str(user.id))
    else:
        await bot.say(str(ctx.message.author.id))

while True and not bot.shutting_down:
    bot.run(configData["token"])
