from sopel.module import commands

@commands('test')
def test(bot,trigger):
    bot.say(trigger.group(2))
