# Let's do this shit.
import random
import sqlite3
import discord
from discord.ext import commands

ownerIds = [
    185877810760515585
]
db_name = "logic.db"
botToken = "MjE1MjIzNTQxNjMxNjgwNTEy.CpUaEQ.K3QAh9jeFwPFYoUfHBmq4RMhiMU"
description = """A first attempt at using discord.py to create a bot."""

bot = commands.Bot(command_prefix="$",description=description)

@bot.event
async def on_ready():
    print("Current login: ")
    print(bot.user.name)
    print(bot.user.id)
    print("Connecting to database...")
    bot.db = sqlite3.connect(db_name)
    print("Connected to {}!".format(db_name))
    bot.memory = {} # dict for maintaining information per-instance
    bot.memory["playing"] = False
    print("Ready to begin!")

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

@bot.command(pass_context=True)
async def az(ctx, option: str):
    """Controls the AZ game."""
    if option == "start":
        print("Starting game of AZ.")
        if not bot.memory["playing"]:
            await bot.say("Warming up...")
            await begin_az()
            await bot.say("Current range: {} --{}".format(
                                  bot.memory["wordlist"][0],
                                  bot.memory["wordlist"][-1]))
        else:
            await bot.say("A game of AZ has already been started!")
    else:
        print("Applying attempt {}.".format(option))
        status = await play_az(option)
        if status: # if the game is won
            await end_az(ctx.message.author,bot.memory["solution"])


async def begin_az():
    """Loads the word database into memory."""
    c = bot.db.cursor()
    print("Loading words from database...")
    c.execute("SELECT word FROM wordlist;")
    bot.memory["wordlist"] = []
    print("Loading words into memory...")
    for row in c.fetchall():
          bot.memory["wordlist"].append(row[0])
    print("Loaded.")
    bot.memory["solution"] = random.choice(bot.memory["wordlist"])
    print("Solution word is {}.".format(bot.memory["solution"]))
    bot.memory["playing"] = True

async def play_az(word):
    """Tries to redefine the current word range by seeing if a given word is in the range.
    If the solution is given, the winner is recognized and the game ends.
    Usage: $az word"""
    wlist = bot.memory["wordlist"][::]
    solution = bot.memory["solution"]
    if word == solution:
        return True
    elif word in wlist:
        if wlist.index(word) < wlist.index(solution):
            wlist = wlist[wlist.index(word)::]
            await bot.say("Close, but no cigar. Range is {} -- {}".format(word,wlist[-1]))
        elif wlist.index(word) > wlist.index(solution):
            wlist = wlist[:(wlist.index(word) + 1):]
            await bot.say("Close, but no cigar. Range is {} -- {}".format(
                                                            wlist[0],
                                                            word))
        bot.memory["wordlist"] = wlist[::]

async def end_az(winner,solution):
    """Ends a game of AZ."""
    await bot.say("Congratulations! {} won with {}!".format(winner,solution))
    bot.memory["playing"] = False
    print("Removing necessary game data...")
    del bot.memory["wordlist"]
    del bot.memory["solution"]




bot.run(botToken)
