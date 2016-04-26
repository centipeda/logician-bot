"""Simple greetings and courteous responses."""

import sopel.module
from sopel.tools import events
from sopel.config.types import StaticSection,ValidatedAttribute
import random


class CourtesyConfig(StaticSection):
    greets = ["Hi there, ","Hey, ","Yo, ","Greetings, ","Hello, "]
    dogreet = False
    again = None
    greetings = ValidatedAttribute("greetings",list,default=greets)
    greet = ValidatedAttribute("do_greet",bool,default=dogreet)
    

def setup(bot):
    bot.config.define_section("courtesy",CourtesyConfig)

@sopel.module.event("JOIN")
@sopel.module.rule("(.)*")
def greetjoin(bot,trigger):
    """Greets users on entering."""
    if bot.config.courtesy.greet and trigger.sender == "#reddit-intp" and trigger.group(1) != bot.nick and not True: # Disabled.
        bot.say("Welcome to {}! Type $help to find out more about what I can do. I'm normally pretty quiet in chat, but if you say the right things I might just respond.".format(trigger.sender))

@sopel.module.require_admin("Not an admin.")
@sopel.module.commands("togglegreet")
def togglegreet(bot,trigger):
    """Changes whether Logician greets users upon entering."""
    bot.config.courtesy.greet = not bot.config.courtesy.greet
    bot.say("Greet setting toggled.")

@sopel.module.commands('about','aboutme')
def about(bot,trigger):
    """Displays basic information about Logician.
    Usage: $about"""
    bot.say("I\'m a bot originally created by centipeda for #reddit-intp. I run using Sopel (https://sopel.chat). Type $help for a full list of what I can do.")

@sopel.module.commands('greet')
def greet(bot,trigger):
    """Greets another user.
    Usage: $greet username"""
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
    """Logician's a pacifist.
    Usage: $fight"""
    bot.say("No!")

@sopel.module.rate(300)
@sopel.module.rule("(Nice|Good|Hard)( game | az | answer | one )?(,)? Logic(ian)?(.)?")
def thanks(bot,trigger):
    """Logician appreciates being complimented."""
    bot.say("Thank you.")

@sopel.module.rate(300)
@sopel.module.rule("(I|We) (like|love|appreciate|am interested in| are interested in) Logic(ian)?(.)?")
def wink(bot,trigger):
    """Of course, Logician also appreciates affection."""
    bot.say(";)")

@sopel.module.rate(300)
@sopel.module.rule("Give( us)? (an easier|an easy) (word|answer|az| game)(,)? Logic(ian)?(.)?")
def no(bot,trigger):
    """Logician doesn't let up."""
    bot.say("No.")

@sopel.module.rate(300)
@sopel.module.rule("(Logic(ian)? is (the best|the superior bot|boss|the best bot))|(INTP(s)? are the best( type)?(.)?)")
def best(bot,trigger):
    """Logician is the best."""
    bot.say("Damn straight.")

@sopel.module.rate(300)
@sopel.module.rule("[Tt]hanks, Logic(ian)?([!.])?")
def thank(bot,trigger):
    """Says 'You're welcome'."""
    bot.say("No problem!")

@sopel.module.rate(300)
@sopel.module.rule("ty logic")
def thank_short(bot,trigger):
    """Same as thank()."""
    bot.say("np")

@sopel.module.rate(300)
@sopel.module.rule("[Ww]hy, Logic(ian)?\?")
def retort(bot,trigger):
    """Defends Logician's position."""
    bot.say("Well, why not?")

@sopel.module.rate(300)
@sopel.module.rule("(R|r)ight, Logic(ian)?")
def unsure(bot,trigger):
    """What happens when you don't pay attention."""
    bot.say("Umm...")
    bot.say("Yes!")

@sopel.module.rate(300)
@sopel.module.rule("((I |We |They |You )?(hate|hates|dislike|dislikes|doesn't want|don't want) (this bot|Logic(ian)?(.)?))|((god)?dammit Logic(ian)?(.)?)")
def sad(bot,trigger):
    """Not upset, just saddened."""
    bot.say(":(")

@sopel.module.rate(300)
@sopel.module.rule("[Ww]hat do you think, Logic(ian)?\?")
def opinion(bot,trigger):
    """Gives Logic's opinion on things."""
    bot.say("I don't generally have an opinion on things.")

@sopel.module.rate(300)
@sopel.module.rule("(what's up|sup|wassup), Logic(ian)?\?")
def wassup(bot,trigger):
    """Says what is up."""
    bot.say("Quarks.")
