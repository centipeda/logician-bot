from sopel.module import commands,rule,require_privmsg

def setup(bot):
    bot.memory["doAuto"] = True

@commands('test')
def test(bot,trigger):
    bot.write(("version",),"centipeda")

@commands('togglefeedback','tfb')
def togglefd(bot,trigger):
    bot.memory["doAuto"] = not bot.memory["doAuto"]
    bot.say("Feedback set to " + str(bot.memory["doAuto"]))
    

@rule('.*')
def auto(bot,trigger):
    if bot.memory["doAuto"]:
        line = trigger.sender + ": " + trigger.nick + ": " + trigger.group(0)
        bot.say(line,"#criticalstrike")

