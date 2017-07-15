"""Implements custom reactions to set messages."""

import discord
from discord.ext import commands

class CustomResponses(object):

    def __init__(self, bot):
        self.bot = bot
        self.refNumToId, self.refIdToNum , self.reactions = self.load_refs()
        self.reactions = self.load_reactions()

    async def on_message(self, message):
        if message.server is not None:
            server = message.server.id
            for reaction in self.reactions[server]:
                if reaction == message.content:
                    await self.bot.send_message(message.channel,
                                                self.reactions[server][reaction])

    def load_refs(self):
        """Loads the reference key to translate between serv_num and
        server_id."""
        c = self.bot.db.cursor()
        c.execute("SELECT server_num, server_id FROM servers;")
        servers = c.fetchall()
        reacs = {}
        ref = {}
        revref = {}
        for servnum, servid in servers:
            servnum = str(servnum)
            servid = str(servid)
            ref[servnum] = servid
            revref[servid] = servnum
            reacs[servid] = {}
        return ref, revref, reacs

    def load_reactions(self):
        """Loads each server's set of reactions into memory."""
        c = self.bot.db.cursor()
        reacs = self.reactions
        c.execute("SELECT trigger, reaction, server_num FROM reactions;")
        for trigger, reaction, serverNum in c.fetchall():
            reacs[self.refNumToId[str(serverNum)]][trigger] = reaction
        return reacs

    @commands.command(pass_context = True)
    async def addreac(self, ctx, phrase: str, reaction: str):
        """Adds a custom reaction to Logic's database."""
        c = self.bot.db.cursor()
        c.execute("SELECT trigger, server_num FROM reactions;")
        for trigger, server in c.fetchall():
            if phrase == trigger and ctx.message.server.id == self.refNumToId[server]:
                await self.bot.say("Reaction already implemented!")
                return
        cmd = "INSERT INTO reactions (trigger, reaction, server_num) VALUES (?,?,?)"
        servnum = self.refIdToNum[ctx.message.server.id]
        self.bot.db.execute(cmd,(phrase, reaction, servnum))
        self.bot.db.commit()
        await self.bot.say("Reaction `{}` added!".format(phrase))
        self.reactions = self.load_reactions()

    @commands.command(pass_context = True)
    async def delreac(self, ctx, phrase: str):
        """Removes a custom reaction to Logic's database."""
        c = self.bot.db.cursor()
        c.execute("SELECT trigger FROM reactions;")
        for trigger in c.fetchall():
            if phrase == trigger[0]:
                cmd = "DELETE FROM reactions WHERE trigger = ? AND server_num = ? "
                self.bot.db.execute(cmd,(phrase,self.refIdToNum[ctx.message.server.id]))
                self.bot.db.commit()
                await self.bot.say("Reaction `{}` deleted!".format(phrase))
        self.reactions = self.load_reactions()

    @commands.command(pass_context = True)
    async def lsreac(self, ctx):
        """Lists all custom reactions in Logic's database."""
        c = self.bot.db.cursor()
        cmd = "SELECT trigger, reaction FROM reactions WHERE server_num = ?"
        c.execute(cmd, (self.refIdToNum[ctx.message.server.id]),)
        reactions = []
        for row in c.fetchall():
            reactions.append(row[0] + " : " + row[1])
        await self.bot.say("```Loaded reactions:\n{}```".format("\n".join(reactions)))
        self.reactions = self.load_reactions()

def setup(bot):
    bot.add_cog(CustomResponses(bot))
