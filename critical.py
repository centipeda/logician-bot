"""My hacked-in identification module."""

import sopel

class CriticalConfig(sopel.config.types.StaticSection):
    pswd = sopel.config.types.ValidatedAttribute("pswd",str,default="swordfish")
    idented = sopel.config.types.ValidatedAttribute("idented",bool,default=False)
    confowner = sopel.config.types.ValidatedAttribute("confowner",str)

def setup(bot):
    bot.config.define_section("critical",CriticalConfig)
    bot.config.critical.confowner = bot.config.core.owner[::]
    bot.config.core.owner = "NickServ"


@sopel.module.require_privmsg("That's not something to do in public.")
@sopel.module.commands("ident","identify")
def identify(bot,trigger):
    if trigger.group(2) == bot.config.critical.pswd and not bot.config.critical.idented:
        bot.config.core.owner = bot.config.critical.confowner
        bot.say("Welcome back!")
    elif bot.config.critical.idented:
        bot.say("Already identified.")
    else:
        bot.say("No!")
    
