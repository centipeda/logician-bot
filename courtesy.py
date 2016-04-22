"""Simple greetings and courteous responses."""

import sopel.module

@sopel.module.commands('greet')
def greet(bot,trigger):
    """Greets another user."""
    bot.say("Greetings, " + trigger.group(2) + "!")

@sopel.module.nickname_commands("Thanks(\!|\.)?")
def thank(bot,trigger):
    """Says 'You're welcome'."""
    bot.reply("No problem!")

@sopel.module.nickname_commands("(W|w)hy?")
def retort(bot,trigger):
    """Defends Logician's position."""
    bot.reply("Well, why not?")

@sopel.module.rule("(R|r)ight, Logic(ian)?")
def unsure(bot,trigger):
    """What happens when you don't pay attention."""
    bot.say("Umm...")
    bot.say("Yes!")

@sopel.module.rule("*.(hate|dislike|don't want)*.(this bot|Logic|Logician)*.")
def sad(bot,trigger):
    """Not upset, just saddened."""
    bot.say(":(")
                   
