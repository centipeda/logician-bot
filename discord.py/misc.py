"""Various miscellaneous commands with little to no utility."""

import asyncio
import random
import discord
from discord.ext import commands

class Misc(object):

    def __init__(self, bot):
        self.bot = bot
        self.ball = ["yes",
                     "no",
                     "perhaps",
                     "only time will tell",
                     "signs point to yes",
                     "ask again another time",
                     "undoubtedly",
                     "not a chance in hell",
                     "of course",
                     "without a doubt",
                     "the odds are not in your favor",
                     "never. Ever"]
        self.windowspasta = self._load_files()

    def _load_files(self):
        with open("windows.txt","r") as f:
            pasta = "".join(f.readlines())
        return pasta

    @commands.command(name="poweruser", pass_context=True)
    async def linux(self, ctx, win : str, lin : str):
        fin = self.windowspasta.format(win,lin)
        print(ctx.message.author.id)
        print(self.bot.owner)
        await self.bot.say(fin)

    @commands.command(name="8ball")
    async def eightball(self, *, query : str):
        print(query[-1])
        if query[-1] != "?":
            await self.bot.reply("ask me a yes or no question.")
        else:
            await self.bot.reply(random.choice(self.ball) + ".")

    @commands.command(name="rate")
    async def rate_user(self, name : str):
        print("rating {}".format(name))
        if name.lower() == "coleen":
            await self.bot.say("I rate {} 100 / 100.".format(name))
        else:
            rating = sum([ord(c) for c in name]) % 100
            await self.bot.say("I rate {} {} / 100.".format(name, rating))

def setup(bot):
    bot.add_cog(Misc(bot))
