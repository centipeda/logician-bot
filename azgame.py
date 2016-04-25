"""An a-z word game."""

import random

from sopel import module
from sopel.config.types import StaticSection,ValidatedAttribute
from sopel.config import Config
from sopel.db import SopelDB
    
def setup(bot):
    bot.config.define_section('azgame',StaticSection)
    bot.db.connect()
    bot.config.azgame.gaming = None
    bot.config.azgame.cheated = False
    
@module.commands("startaz","azgame","azstart")
def startaz(bot,trigger):
    """Starts a game of az.
    Usage: $startaz"""
    if bot.config.azgame.gaming:
        bot.reply("End the current game with $endaz first.")
    else:
        bot.say("Warming up...")
        bot.config.azgame.baselist = [word[0].encode('ascii') for word in bot.db.execute("SELECT word from wordlist;")]
        blist = bot.config.azgame.baselist
        bot.config.azgame.wordlist = blist[::]
        bot.config.azgame.answer = random.choice(blist)
        bot.say("Range is {} -- {}".format(blist[0],blist[-1]))
        bot.config.azgame.gaming = True
        bot.db.close()

@module.commands("endaz","azquit","azend","quitaz")
def end_az(bot,trigger):
    """Ends a game of az.
    Usage: $endaz"""
    if bot.config.azgame.gaming:
        bot.config.azgame.gaming = False
        bot.say("Game ended, the winning word was {}. Blame {}!".format(bot.config.azgame.answer,
                                                                    trigger.nick))

@module.commands("az")
def attempt_az(bot,trigger):
    """Tries to redefine the word range by seeing if a given word is in the range.
    If the solution is given, the winner is recognized and the game ends.
    Usage: $az word"""
    if not bot.config.azgame.gaming:
        bot.reply("Start a game using $startaz first.")
    elif trigger.group(2) is None or len(trigger.group(2).split()) > 1:
        pass
    else:
        solution = bot.config.azgame.answer
        wlist = bot.config.azgame.wordlist[::]
        attempt = str(trigger.group(2))
        if attempt == bot.config.azgame.answer:
            bot.say("Congratulations to {}! The winning word was {}.".format(trigger.nick,solution))
            bot.config.azgame.gaming = False
            if bot.config.azgame.cheated or bot.config.azgame.altered:
                bot.say("Something seemed a little off about that game to me, though.")
        elif attempt in wlist:
            if wlist.index(attempt) < wlist.index(solution):
                wlist = wlist[wlist.index(attempt)::]
                bot.say("Close, but no cigar. Range is {} -- {}".format(attempt,wlist[-1]))
            elif wlist.index(attempt) > wlist.index(solution):
                wlist = wlist[:(wlist.index(attempt) + 1):]
                bot.say("Close, but no cigar. Range is {} -- {}".format(wlist[0],attempt))
            bot.config.azgame.wordlist = wlist[::]

@module.rule("(.)*")
def freeattempt(bot,trigger):
    """Makes it so $az isn't needed to play."""
    if bot.config.azgame.gaming and not True: # Disabled for now.
        if len(trigger.group(1).split()) == 1:
            attempt_az(bot,trigger.group(1))
        

@module.commands("azrange","rangeaz")
def azrange(bot,trigger):
    """Outputs the current range of a game of az.
    Usage: $azrange"""
    if bot.config.azgame.gaming:
        bot.say("Range is {} -- {}".format(bot.config.azgame.wordlist[0],
                                           bot.config.azgame.wordlist[-1]))
    else:
        bot.reply("Start a game with $startaz first.")

@module.require_admin(message="You're not one of my admins!")
@module.commands("azanswer","azsolution")
def azanswer(bot,trigger):
    """Outputs the answer of the current game of az. Admin-only command.
    Usage: $azanswer"""
    if bot.config.azgame.gaming:
        bot.say("The answer is " + bot.config.azgame.answer + ".")
        bot.say("...Cheater.")
        bot.config.azgame.cheated = True

@module.require_admin(message="You're not one of my admins!")
@module.commands("setaz","azset")
def azset(bot,trigger):
    """Changes the answer to a game of az.
    Be careful that the new answer is within the current range, or weird stuff happens.
    Usage: $azset newanswer"""
    if bot.config.azgame.gaming:
        bot.config.azgame.answer = trigger.group(2)
        bot.say("Answer set to " + bot.config.azgame.answer,trigger.sender)
        bot.config.azgame.altered = True
