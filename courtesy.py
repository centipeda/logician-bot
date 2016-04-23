"""Simple greetings and courteous responses."""

import sopel.module
from sopel.tools import events
import random

greetings = ["Hi there, ","Hey, ","Yo, ","Greetings, ","Hello, "]

@sopel.module.event("JOIN")
@sopel.module.rule(".*")
def greet_newuser(bot,trigger):
    """Greets new users."""
    if trigger.sender != bot.nick:
        greet = random.choice(greetings)+trigger.nick+". Welcome to #reddit-intp, I'm Logician. Type $help for more on what I can do."
        bot.say(greet)

@sopel.module.commands('greet')
def greet(bot,trigger):
    """Greets another user."""
    bot.say(random.choice(greetings) + trigger.group(2) + "!")

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
