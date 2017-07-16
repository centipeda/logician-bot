"""For grabbing guitar tabs."""

import asyncio
import random
import discord
from discord.ext import commands

import grab_tab

class TabExtractor(object):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tab")
    async def get_tab(self, query : str):
        tab = grab_tab.get_tab(query)
        await self.bot.say("```{}```".format(tab))

def setup(bot):
    bot.add_cog(TabExtractor(bot))
