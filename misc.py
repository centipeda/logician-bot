# coding: utf-8
"""Random other commands."""

import random

from sopel.module import commands,require_admin
from sopel.module import rule
from sopel.config.types import StaticSection,ValidatedAttribute

class MiscConfig(StaticSection):
    ballansw = ["Yes.",
                "Not in any conceivable scenario.",
                "Undoubtedly.",
                "I doubt it, for some reason.",
                "Time will tell.",
                "Why do you need to know?",
                "No.",
                "Why?",
                "Perhaps.",
                "Ask another time.",
                "That seems plausible.",
                "That would be... unlikely.",
                "But... why?",
                "Nope.",
                "Maybe!",
                "Sorry, what was that?"]
    answers = ValidatedAttribute("answers",list,default=ballansw)
    quipfile = ValidatedAttribute("quipfile",str,default="/home/crit/.sopel/modules/1liners.cap")
    quiplist = ValidatedAttribute("quiplist",list,default=[])

def setup(bot):
    bot.config.define_section('misc',MiscConfig)
    quipfile = open(bot.config.misc.quipfile,"r")
    for line in quipfile.readlines():
        if line != "     \r\n":
            bot.config.misc.quiplist.append(line[5:-2])

@commands("8ball","8b","eightball")
def eightball(bot,trigger):
    """Consult the magic 8-ball for answers."""
    if trigger.group(2)[-1] != "?":
        bot.reply("Please ask a yes or no question.")
    else:
        # bot.reply(random.choice(bot.config.miscellaneous.answers))
        total = 0
        for char in trigger.group(2)[::-1]:
            total += ord(char)
        bot.reply(bot.config.misc.answers[total % len(bot.config.misc.answers)])
        
@commands("quip")
def quip(bot,trigger):
    """Has Logician say something from his quiplist."""
    bot.say(random.choice(bot.config.misc.quiplist))

@commands("douse","mindbleach","bleach")
def douse(bot,trigger):
    """Usage: $douse user"""
    bot.action("douses " + trigger.group(2) + " with mind bleach")

@commands("slap")
def slap(bot,trigger):
    """Usage: $slap user"""
    bot.say("I'd rather not.")

@commands("fliptable")
def fliptable(bot,trigger):
    """Usage: $fliptable"""
    bot.say("(╯°□°)╯︵ ┻━┻")

@commands("unflip")
def unfliptable(bot,trigger):
    """Usage: $unfliptable"""
    bot.say("┬─┬﻿ ノ( ゜-゜ノ)")

@commands("lenny")
def lenny(bot,trigger):
    """Usage: $lenny"""
    lennyface(bot,trigger)

@rule("[Yy]ou like that, Logic(ian)?")
def lennyface(bot,trigger):
    bot.say("( ͡° ͜ʖ ͡°)")
