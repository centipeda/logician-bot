"""An a-z word game."""

import random

from sopel import module
from sopel.config.types import StaticSection,ValidatedAttribute
from sopel.config import Config
from sopel.db import SopelDB

import sqlite3

class AZConfig(StaticSection):
    gamechan = ValidatedAttribute("gamechan",str,default="#LogicianGames")

def setup(bot):
    bot.config.define_section('azgame',AZConfig)
    bot.db.connect()
    bot.config.azgame.gaming = None

"""
@module.commands("azgame")
def aboutaz(bot,trigger):
    pass
"""
    
@module.require_chanmsg("Not in a channel.")
@module.commands("startaz","azgame","azstart")
def startaz(bot,trigger):
    """Starts a game of az.
    Usage: $startaz"""
    if bot.config.azgame.gaming:
        bot.reply("End the current game with $endaz first.")
    elif trigger.sender != bot.config.azgame.gamechan:
        bot.reply("Games can currently only be played in {}.".format(bot.config.azgame.gamechan))
    else:
        bot.say("Warming up...")
        bot.config.azgame.baselist = [word[0].encode('ascii') for word in bot.db.execute("SELECT word from wordlist;")]
        blist = bot.config.azgame.baselist
        bot.config.azgame.wordlist = blist[::]
        bot.config.azgame.answer = random.choice(blist)
        bot.say("Range is {} -- {}".format(blist[0],blist[-1]))
        bot.config.azgame.gaming = True

@module.commands("endaz","azquit","azend","quitaz")
def end_az(bot,trigger):
    """Ends a game of az.
    Usage: $endaz"""
    if bot.config.azgame.gaming and trigger.sender == bot.config.azgame.gamechan:
        bot.config.azgame.gaming = False    
        bot.say("Game ended, the winning word was {}. Blame {}!".format(bot.config.azgame.answer,trigger.nick))
    else:
        bot.reply("Start a game using $startaz first.")

@module.commands("az")
def attempt_az(bot,trigger,word=None):
    """Tries to redefine the word range by seeing if a given word is in the range.
    If the solution is given, the winner is recognized and the game ends.
    Usage: $az word"""
    if not bot.config.azgame.gaming:
        bot.reply("Start a game using $startaz first.")
    elif trigger.group(2) is None:
        pass
    elif trigger.sender != bot.config.azgame.gamechan:
        bot.reply("You can play in {}.".format(bot.config.azgame.gamechan))
    else:
        solution = bot.config.azgame.answer
        wlist = bot.config.azgame.wordlist[::]
        if word is not None:
            attempt = word
        else:
            attempt = str(trigger.group(2).split()[0])
        if attempt == bot.config.azgame.answer:
            az_win(bot,trigger)
        elif attempt in wlist:
            if wlist.index(attempt) < wlist.index(solution):
                wlist = wlist[wlist.index(attempt)::]
                bot.say("Close, but no cigar. Range is {} -- {}".format(attempt,wlist[-1]))
            elif wlist.index(attempt) > wlist.index(solution):
                wlist = wlist[:(wlist.index(attempt) + 1):]
                bot.say("Close, but no cigar. Range is {} -- {}".format(wlist[0],attempt))
            bot.config.azgame.wordlist = wlist[::]

def az_win(bot,trigger):
    """Called when a game of az is won."""
    bot.say("Congratulations to {}! The winning word was {}.".format(trigger.nick,solution))
    bot.config.azgame.gaming = False
    if bot.config.azgame.cheated or bot.config.azgame.altered:
        bot.say("Something seemed a little off about that game to me, though.")
    """
    winner = trigger.nick
    # Increment won counter.
    wins = sqlite3.fetchone(bot.db.execute("SELECT totalwon FROM azstats;"))
    wins += 1
    bot.db.execute("UPDATE azstats SET wontimes = ?;",(wins,))
    # Add to user's wins, if they're in the database. Otherwise, adds them.
    user = sqlite3.fetchone(bot.db.execute("SELECT userswon FROM azstats WHERE value = ?;",(trigger.nick,)))
    if user is None:
        bot.db.execute("INSERT INTO azstats (?,?) VALUES (userswon,wontimes);",(trigger.nick,1))
    else:
        pastwinner = bot.db.execute("SELECT * FROM azstats WHERE userswon = ?;",(trigger.nick,))
    """

@module.rule("(.)*")
def freeattempt(bot,trigger):
    """Makes it so $az isn't needed to play."""
    if bot.config.azgame.gaming and not True: # Disabled
        if len(trigger.group(1).split()) == 1:
            attempt_az(bot,trigger,word=trigger.group(1).split()[0])
        

@module.commands("azrange","rangeaz")
def azrange(bot,trigger):
    """Outputs the current range of a game of az.
    Usage: $azrange"""
    if bot.config.azgame.gaming and trigger.sender == bot.config.azgame.gamechan:
        bot.say("Range is {} -- {}".format(bot.config.azgame.wordlist[0],
                                           bot.config.azgame.wordlist[-1]))
    else:
        bot.reply("Start a game with $startaz first.")
        
@module.commands("azchan")
def azchan(bot,trigger):
    """Outputs the channel the current game of az was started in."""
    if bot.config.azgame.gaming and bot.config.azgame.startchan is not None and not True: # Disabled
        bot.say("Current game started in " + bot.config.azgame.startchan)
    else:
        bot.reply("Start a game with $startaz first.")

@module.require_admin(message="You're not one of my admins!")
@module.commands("azanswer","azsolution")
def azanswer(bot,trigger):
    """Outputs the answer of the current game of az. Admin-only command.
    Usage: $azanswer"""
    if bot.config.azgame.gaming and not True: # Disabled
        bot.say("The answer is " + bot.config.azgame.answer + ".")
        bot.say("...Cheater.")
        bot.config.azgame.cheated = True

@module.require_admin(message="You're not one of my admins!")
@module.commands("setaz","azset")
def azset(bot,trigger):
    """Changes the answer to a game of az.
    Be careful that the new answer is within the current range, or weird stuff happens.
    Usage: $azset newanswer"""
    if bot.config.azgame.gaming and not True: # Disabled
        bot.config.azgame.answer = trigger.group(2)
        bot.say("Answer set to " + bot.config.azgame.answer,trigger.sender)
        bot.config.azgame.altered = True
