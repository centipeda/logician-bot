import discord
from random import choice as randchoice
from discord.ext import commands

class Pats:
    """A cog that pats"""

    def __init__(self, bot):
        self.bot = bot

        self.patgif = [
    	"http://i.imgur.com/IiQwK12.gif", 
    	"http://i.imgur.com/JCXj8yD.gif", 
    	"http://i.imgur.com/qqBl2bm.gif", 
    	"http://i.imgur.com/eOJlnwP.gif", 
    	"https://i.imgur.com/L8voKd1.gif",
    	"http://imgur.com/hzoLfUS.gif", 
    	"http://imgur.com/yo49xua.gif", 
    	"http://imgur.com/n6vY6Tj.gif", 
    	"http://imgur.com/Enedahe.gif", 
    	"http://imgur.com/hMpJ53w.gif", 
    	"http://imgur.com/40HkmUe.gif", 
    	"http://imgur.com/hSnItdb.gif", 
    	"http://imgur.com/GTMvOCt.gif"
    	]

    @commands.command(pass_context = True) #pass_context is for ctx
    async def pat(self, ctx, user : discord.Member=None):
        """ Gives a pat to someone or no one... """
        author = ctx.message.author
        pat = randchoice(self.patgif)
        if user != None:
            await self.bot.say("_{} pats {}_ \n".format(author.name, user.mention) + pat)
            if user.id == self.bot.user.id:
                await self.bot.say("*purrs*")
        else:
            await self.bot.say(pat)

def setup(bot):
    bot.add_cog(Pats(bot))
