"""Implements custom reactions to set messages."""

import discord
from discord.ext import commands

class CustomResponses(object):

    def __init__(self, bot):
        self.bot = bot
        self.reactions = self.load_reactions()

    async def on_message(self, message):
        for reaction in self.reactions:
            if reaction == message.content:
                await self.bot.send_message(message.channel, self.reactions[reaction])

    def load_reactions(self):
        c = self.bot.db.cursor()
        c.execute("SELECT trigger, reaction FROM reactions;")
        reacs = {}
        for row in c.fetchall():
            reacs[row[0]] = row[1]
        return reacs

    @commands.command()
    async def addreac(self, phrase: str, reaction: str):
        """Adds a custom reaction to Logic's database."""
        c = self.bot.db.cursor()
        c.execute("SELECT trigger FROM reactions;")
        for trigger in c.fetchall():
            if phrase == trigger[0]:
                await self.bot.say("Reaction already implemented!")
                return
        c.execute("INSERT INTO reactions (trigger, reaction) VALUES (?,?)",(phrase, reaction))
        await self.bot.say("Reaction `{}` added!".format(phrase))
        self.reactions = self.load_reactions()

    @commands.command()
    async def delreac(self, phrase: str):
        """Removes a custom reaction to Logic's database."""
        c = self.bot.db.cursor()
        c.execute("SELECT trigger FROM reactions;")
        for trigger in c.fetchall():
            if phrase == trigger[0]:
                c.execute("DELETE FROM reactions WHERE trigger = ?",(phrase,))
                await self.bot.say("Reaction `{}` deleted!".format(phrase))
        self.reactions = self.load_reactions()

    @commands.command()
    async def lsreac(self):
        """Lists all custom reactions in Logic's database."""
        c = self.bot.db.cursor()
        c.execute("SELECT trigger, reaction FROM reactions")
        reactions = []
        for row in c.fetchall():
            reactions.append(row[0] + " : " + row[1])
        await self.bot.say("```Loaded reactions:\n{}```".format("\n".join(reactions)))
        self.reactions = self.load_reactions()

def setup(bot):
    bot.add_cog(CustomResponses(bot))
