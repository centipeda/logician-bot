"""Various MBTI (Myers-Briggs Type Indicator)-related channel commands."""

from sopel.module import commands
from sopel.config.types import StaticSection, ValidatedAttribute

class MbtiSection(StaticSection):
    descs = ['http://personalitycafe.com/intp-forum-thinkers/94751-intp-jungian-cognitive-function-analysis.htm',
                    'http://www.intp.org/intprofile.html',
                    'http://www.personalitydesk.com/intp',
                    'http://www.16personalities.com/intp-personality']
    subreddit = 'https://reddit.com/r/INTP'
    famous = 'http://www.celebritytypes.com/intp.php'
    descriptions = ValidatedAttribute('descriptions',list,default=descs)
    famous = ValidatedAttribute('famous',str,default=famous)
    subreddit = ValidatedAttribute('subreddit',str,default=subreddit)

def setup(bot):
    bot.config.define_section('mbti',MbtiSection)
    
@commands('intp')
def intp(bot,trigger):
    """Multiple INTP-related things.
    Try description, subreddit, or famous as arguments."""
    if trigger.group(2) == "description":
        list_descriptions(bot,trigger)
    elif trigger.group(2) == "subreddit":
        subreddit(bot,trigger)
    elif trigger.group(2) == "famous":
        famous(bot,trigger)

## Too lazy to retype this stuff. ##
def list_descriptions(bot,trigger):
    """Provides links to descriptions of the INTP type."""
    bot.say('Some INTP descriptions:')
    for link in bot.config.mbti.descriptions:
        bot.say(link)
    
def subreddit(bot,trigger):
    """Provides links to MBTI-related subreddits."""
    bot.reply(bot.config.mbti.subreddit)

def famous(bot,trigger):
    """Links to examples of famous INTPs."""
    bot.reply("Some famous INTPs: " + bot.config.mbti.famous)
