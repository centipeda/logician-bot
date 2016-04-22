"""Random other commands."""

import random

from sopel.module import commands as command
from sopel.config.types import StaticSection,ValidatedAttribute

class MiscConfig(StaticSection):
    ballansw = ["Yes.",
                "No.",
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
