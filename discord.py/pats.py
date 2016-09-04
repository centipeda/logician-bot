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
    	"https://45.media.tumblr.com/229ec0458891c4dcd847545c81e760a5/tumblr_mpfy232F4j1rxrpjzo1_r2_500.gif", 
    	"https://media.giphy.com/media/KZQlfylo73AMU/giphy.gif", 
    	"https://media.giphy.com/media/12hvLuZ7uzvCvK/giphy.gif", 
    	"http://gallery1.anivide.com/_full/65030_1382582341.gif", 
    	"https://49.media.tumblr.com/8e8a099c4eba22abd3ec0f70fd087cce/tumblr_nxovj9oY861ur1mffo1_500.gif", 
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
    	else:
    		await self.bot.say(pat)

def setup(bot):
    bot.add_cog(Pats(bot))