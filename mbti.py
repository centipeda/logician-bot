"""Various MBTI (Myers-Briggs Type Indicator)-related channel commands."""

from sopel.module import commands
from sopel.config.types import StaticSection, ValidatedAttribute

# This feels really inefficient, but I don't have any better ideas.
types = ["intp","entp","intj","entj",
         "enfj","infj","infp","enfp",
         "estp","istp","esfp","isfp",
         "isfj","estj","istj","esfj"]

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

@commands('mbti')
def mbti(bot,trigger):
    if trigger.group(2) is None:
        bot.say("Try $mbti [type|test].")
    elif trigger.group(2).lower() in types:
        bot.say("https://www.16personalities.com/{}-personality".format(trigger.group(2).lower()))
        bot.say("http://www.personalitypage.com/{}.html".format(trigger.group(2).upper()))
    elif trigger.group(2) == "test":
        bot.say("https://www.16personalities.com/free-personality-test")
        
    
@commands('intp')
def intp(bot,trigger):
    """Multiple INTP-related things.
    Try description, subreddit, or famous as arguments."""
    if trigger.group(2) is None:
        bot.say("Try $intp [description|subreddit|famous].")
    elif trigger.group(2) == "description":
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
