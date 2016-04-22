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

@commands('description','descriptions')
def list_descriptions(bot,trigger):
    """Provides links to descriptions of the INTP type."""
    bot.say('Some INTP descriptions:')
    for link in bot.config.mbti.descriptions:
        bot.say(link)
        
@commands('subreddit','subreddits')
def subreddit(bot,trigger):
    """Provides links to MBTI-related subreddits."""
    bot.reply(bot.config.mbti.subreddit)

@commands('about','aboutme')
def about(bot,trigger):
    """Basic information about Logician."""
    bot.say("I\'m a bot originally created by centipeda for #reddit-intp. I run using Sopel. I don\'t do very much right now, but more coming soon!")

@commands('famous','famousintp')
def famous(bot,trigger):
    """Links to examples of famous INTPs."""
    bot.reply("Some famous INTPs: " + bot.config.mbti.famous)
