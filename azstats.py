"""Displays statistics for the azgame module."""

from sopel import module
from sopel.config.types import StaticSection,ValidatedAttribute

def setup(bot):
    bot.db.connect()

@module.commands("azstats","azstat")
def azstats(bot,trigger):
    args = trigger.group(2).split()
    if args[0] == "full":
        fullstats(bot)
    elif args[0] == "lastwinner":
        lastwinner(bot)
    elif args[0] == "lastwin":
        lastwintime(bot)
    elif args[0] == "userwins":
        userwins(bot)

def fullstats(bot):
    pass

def lastwinner(bot):
    pass

def lastwintime(bot):
    pass

def userwins(bot):
    pass
