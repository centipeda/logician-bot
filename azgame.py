"""An a-z word game."""

import random

from sopel import module
from sopel.config.types import StaticSection,ValidatedAttribute
from sopel.config import Config
from sopel.db import SopelDB
    
def setup(bot):
    bot.config.define_section('azgame',StaticSection)
    bot.config.azgame.database = SopelDB(Config('../default.cfg'))
    bot.config.azgame.database.connect()
    bot.config.azgame.gaming = None
    
@module.commands("startaz","azgame","azstart")
def startaz(bot,trigger):
    if bot.config.azgame.gaming:
        bot.reply("End the current game with $endaz first.")
    else:
        bot.say("Warming up...")
        bot.config.azgame.baselist = [word[0].encode('ascii') for word in bot.config.azgame.database.execute("SELECT word from wordlist;")]
        blist = bot.config.azgame.baselist
        bot.config.azgame.wordlist = blist[::]
        bot.config.azgame.answer = random.choice(blist)
        bot.say("Range is {} -- {}".format(blist[0],blist[-1]))
        bot.config.azgame.gaming = True

@module.commands("endaz","azquit","azend","quitaz")
def end_az(bot,trigger):
    if bot.config.azgame.gaming:
        bot.config.azgame.gaming = False
        bot.say("Game ended, the winning word was {}. Blame {}!".format(bot.config.azgame.answer,
                                                                    trigger.nick))

@module.commands("az")
def attempt_az(bot,trigger):
    if not bot.config.azgame.gaming:
        bot.reply("Start a game using $startaz first.")
    elif len(trigger.group(2).split()) > 1:
        pass
    else:
        solution = bot.config.azgame.answer
        wlist = bot.config.azgame.wordlist[::]
        attempt = str(trigger.group(2))
        if attempt == bot.config.azgame.answer:
            bot.say("Congratulations to {}! The winning word was {}.".format(trigger.nick,solution))
            bot.config.gaming = False
        elif attempt in wlist:
            if wlist.index(attempt) < wlist.index(solution):
                wlist = wlist[wlist.index(attempt)::]
                bot.say("Close, but no cigar. Range is {} -- {}".format(attempt,wlist[-1]))
            elif wlist.index(attempt) > wlist.index(solution):
                wlist = wlist[:(wlist.index(attempt) + 1):]
                bot.say("Close, but no cigar. Range is {} -- {}".format(wlist[0],attempt))

            bot.config.azgame.wordlist = wlist[::]

@module.require_admin(message="Not an admin!")
@module.commands("azanswer","azsolution")
def azanswer(bot,trigger):
    """Cheater!"""
    bot.say("The answer is " + bot.config.azgame.answer,trigger.sender)
    bot.say("...Cheater.",trigger.sender)

@module.require_admin(message="Not an admin!")
@module.commands("setaz","azset")
def azset(bot,trigger):
    """For administration purposes."""
    bot.config.azgame.answer = trigger.group(2)
    bot.say("Answer set to " + bot.config.azgame.answer,trigger.sender)
