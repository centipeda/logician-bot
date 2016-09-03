"""Rotates status messages."""

import asyncio
import discord
from discord.ext import commands

class StatusRotater(object):

    def __init__(self, bot):
        self.bot = bot
        self.statuses = ["to the crowd",
                         "ever so softly",
                         "right behind you",
                         "it like a fiddle",
                         "the game of love"]
        self.currentStatus = 0
        self.bot.loop.create_task(self.rotate_statuses())
        print("Loaded!")

    async def rotate_statuses(self):
        while not self.bot.is_closed:
            if self.currentStatus == len(self.statuses):
                self.currentStatus = 0
            print("Rotating status to {}".format(self.statuses[self.currentStatus]))
            await self.bot.change_status(discord.Game(name=self.statuses[self.currentStatus]))
            await asyncio.sleep(10)
            self.currentStatus += 1


def setup(bot):
    bot.add_cog(StatusRotater(bot))
