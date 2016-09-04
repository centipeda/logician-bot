"""Commands for sending animated .gif responses."""

import discord
from discord.ext import commands

class GifResponses(object):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trap(self):
        """It's a trap!"""
        await self.bot.say("http://i.imgur.com/LaJ9Kmo.gif")

    @commands.command()
    async def bees(self):
        """Not the beeeeees!"""
        await self.bot.say("http://i.imgur.com/TybTuTL.gif")

    @commands.command()
    async def travolta(self):
        """...What? Huh?"""
        await self.bot.say("http://i.imgur.com/j51uHm1.gif")

    @commands.command()
    async def buckethead(self):
        """Always have a backup."""
        await self.bot.say("http://i.imgur.com/xIolo.gif")

def setup(bot):
    bot.add_cog(GifResponses(bot))
