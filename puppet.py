"""Contains (mostly admin-only) commands for remotely operating on Logician."""

from sopel.module import commands,require_admin,require_owner,require_privmsg,rule
from sopel.config.types import StaticSection,ValidatedAttribute

class PuppetConfig(StaticSection):
    pass

def setup(bot):
    bot.config.define_section("puppet",PuppetConfig)
    bot.config.puppet.saychan = None
    bot.config.puppet.echo = False

@require_admin()
@commands("do")
def do(bot,trigger):
    bot.write(trigger.group(2).split())

@require_admin()
@commands("setchannel","setchan","setpa")
def setchannel(bot,trigger):
    bot.config.puppet.saychan = trigger.group(2)
    bot.say("Set PA channel to " + trigger.group(2))

@require_admin()
@require_privmsg()
@commands("pa")
def pa(bot,trigger):
    bot.say(trigger.group(2),bot.config.puppet.saychan)

@require_admin()
@commands("toggleecho","echotoggle")
def toggleecho(bot,trigger):
    bot.config.puppet.echo = not bot.config.puppet.echo
    bot.say("Echo set to " + str(bot.config.puppet.echo))

@require_admin()
@rule("(.)*")
def echo(bot,trigger):
    if bot.config.puppet.echo and (trigger.match.string != "toggleecho"):
        bot.say(trigger.match.string,bot.config.puppet.saychan)
