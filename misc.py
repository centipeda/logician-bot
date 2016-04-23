# coding: utf-8
"""Random other commands."""

import random

from sopel.module import commands as command
from sopel.module import rule
from sopel.config.types import StaticSection,ValidatedAttribute

class MiscConfig(StaticSection):
    ballansw = ["Yes.",
                "Not in any conceivable scenario.",
                "Undoubtably.",
                "I doubt it, for some reason.",
                "Time will tell.",
                "Why do you need to know?",
                "No.",
                "Why?",
                "Perhaps.",
                "Ask another time.",
                "That seems plausible.",
                "That would be... unlikely.",
                "Sorry, what was that?"]
    answers = ValidatedAttribute("answers",list,default=ballansw)

def setup(bot):
    bot.config.define_section('miscellaneous',MiscConfig)

@command("8ball","8b","eightball")
def eightball(bot,trigger):
    if trigger.group(2)[-1] != "?":
        bot.reply("Please ask a yes or no question.")
    else:
        bot.reply(random.choice(bot.config.miscellaneous.answers))

@command("fliptable")
def fliptable(bot,trigger):
    bot.say("(╯°□°)╯︵ ┻━┻")

@command("unflip")
def unfliptable(bot,trigger):
    bot.say("┬─┬﻿ ノ( ゜-゜ノ)")

@rule("[Yy]ou like that, Logic(ian)?")
def lennyface(bot,trigger):
    bot.say("( ͡° ͜ʖ ͡°)")
