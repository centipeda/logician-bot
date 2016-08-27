from sopel.module import commands,rule,require_privmsg,require_admin

def setup(bot):
    bot.memory["doAuto"] = True

@require_privmsg()
@require_admin()
@commands('togglefeedback','tfb')
def togglefd(bot,trigger):
    bot.memory["doAuto"] = not bot.memory["doAuto"]
    bot.say("Feedback set to " + str(bot.memory["doAuto"]))
    
@require_admin()
@rule('.*')
def auto(bot,trigger):
    if bot.memory["doAuto"]:
        line = trigger.sender + ": " + trigger.nick + ": " + trigger.group(0)
        bot.say(line,"#criticalstrike")

