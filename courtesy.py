"""Simple greetings and courteous responses."""

import sopel.module
from sopel.tools import events
from sopel.config.types import StaticSection,ValidatedAttribute
import random


class CourtesyConfig(StaticSection):
    greets = ["Hi there, ","Hey, ","Yo, ","Greetings, ","Hello, "]
    again = None
    greetings = ValidatedAttribute("greetings",list,default=greets)

def setup(bot):
    bot.config.define_section("courtesy",CourtesyConfig)

"""@sopel.module.event(None)
@sopel.module.rule(".*")
def greet_newuser(bot,trigger):
    pass # Too spammy, maybe
    if trigger.sender != bot.nick:
        greet = random.choice(greetings)+trigger.nick+". Welcome to #reddit-intp, I'm Logician. Type $help for more on what I can do."
        bot.say(greet)"""

@commands('about','aboutme')
def about(bot,trigger):
    """Basic information about Logician."""
    bot.say("I\'m a bot originally created by centipeda for #reddit-intp. I run using Sopel. Type $help for a full list of what I can do.")

@sopel.module.commands('greet')
def greet(bot,trigger):
    """Greets another user."""
    if trigger.group(2) == bot.config.core.owner:
        bot.say("No need, I already know him.")
    elif trigger.group(2) == bot.nick or trigger.group(2) == "Logic":
        if bot.config.courtesy.again:
            bot.say("Fine. " + random.choice(bot.config.courtesy.greetings) + trigger.group(2) + "!")
            bot.config.courtesy.again = False
        else:
            bot.say("Why would I do that?")
            bot.config.courtesy.again = True
    else:
        bot.say(random.choice(bot.config.courtesy.greetings) + trigger.group(2) + "!")

@sopel.module.commands('fight')
def nofight(bot,trigger):
    """Logician's a pacifist."""
    bot.say("No!")

@sopel.module.rule("[Tt]hanks, Logic(ian)?([!.])?")
def thank(bot,trigger):
    """Says 'You're welcome'."""
    bot.say("No problem!")

@sopel.module.rule("ty logic")
def thank_short(bot,trigger):
    """Same as thank()."""
    bot.say("np")

@sopel.module.rule("[Ww]hy, Logic(ian)?\?")
def retort(bot,trigger):
    """Defends Logician's position."""
    bot.say("Well, why not?")

@sopel.module.rule("(R|r)ight, Logic(ian)?")
def unsure(bot,trigger):
    """What happens when you don't pay attention."""
    bot.say("Umm...")
    bot.say("Yes!")

@sopel.module.rule("I (hate|dislike|don't want) (this bot|Logic(ian)?)*")
def sad(bot,tprigger):
    """Not upset, just saddened."""
    bot.say(":(")
                   
@sopel.module.rule("[Ww]hat do you think, Logic(ian)?\?")
def opinion(bot,trigger):
    """Gives Logic's opinion on things."""
    bot.say("I don't generally have an opinion on things.")

@sopel.module.rule("(what's up|sup|wassup), Logic(ian)?\?")
def wassup(bot,trigger):
    """Says what is up."""
    bot.say("Quarks.")
