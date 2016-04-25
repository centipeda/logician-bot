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

def setup(bot):
    bot.config.define_section('misc',MiscConfig)

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
