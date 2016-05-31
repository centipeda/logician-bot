"""Manages Logic's quote database."""

from sopel import module
import random

def setup(bot):
    # Add things as they come to mind.
    pass

@module.commands("quote","q")
def quote(bot,trigger):
    """Pulls the quote with the number specified, or a random one otherwise."""
    quotes = bot.db.execute("SELECT quote, creator, channel FROM quotes;").fetchall()
    if trigger.group(2) is not None and type(eval(trigger.group(2))) is int and eval(trigger.group(2)) in range(1,len(quotes) + 1):
        quote = quotes[eval(trigger.group(2)) - 1]
    else:
        quote = random.choice(quotes) 
        # bot.say("Yeah, I'm just spitting out random stuff.")
    if quote[2][0] != "#":
        bot.say("{} -- added by {}".format(quote[0],quote[1]))
    else:
        bot.say("{} -- added by {} in {}".format(quote[0],quote[1],quote[2]))

@module.commands("quoteadd","addquote","qadd")
def addquote(bot,trigger):
    """Adds a quote to Logic's database."""
    adder = trigger.nick
    quote = trigger.group(2)
    if trigger.sender[0] != "#":
        chan = "none"
    else:
        chan = trigger.sender
    bot.db.execute("INSERT INTO quotes (creator,channel,quote) VALUES (?,?,?)",(adder,chan,quote))
    bot.say("Quote added!") 
