"""Administrator/owner only commands."""

import discord
from discord.ext import commands

def check_owner_id(message):
    return message.author.id == "185877810760515585"

def is_owner():
    return commands.check(lambda ctx: check_owner_id(ctx.message))

class Administration(object):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_owner()
    async def loadext(self, extension_name: str):
        """Loads an extension. Admin-only."""
        try:
            self.bot.load_extension(extension_name)
        except Exception as e:
            print("{}: {}".format(type(e).__name__,e))
            await self.bot.say("Failed to load extension `{}`.".format(extension_name))
            return
        print("Successfully loaded extension {}.".format(extension_name))
        await self.bot.say("Loaded extension `{}`.".format(extension_name))

    @commands.command()
    @is_owner()
    async def unloadext(self, extension_name: str):
        """Unloads an extension. Admin-only."""
        self.bot.unload_extension(extension_name)
        print("Unloaded " + extension_name)
        await self.bot.say("Unloaded extension `{}`.".format(extension_name))

    @commands.command()
    @is_owner()
    async def reloadext(self, extension_name: str):
        """Reloads an extension. Admin-only."""
        self.bot.unload_extension(extension_name)
        try:
            self.bot.load_extension(extension_name)
        except Exception as e:
            print(e)
            await self.bot.say("Failed to load extension `{}`.".format(extension_name))
            return
        await self.bot.say("Reloaded extension `{}`.".format(extension_name))

    @commands.command(hidden=True)
    @is_owner()
    async def restart(self):
        """Restarts."""
        await self.bot.say("See you in a bit!")
        await self.bot.close()

    @commands.command(hidden=True)
    @is_owner()
    async def shutdown(self):
        """Shuts down."""
        await self.bot.say("Bye-bye!")
        self.bot.shutting_down = True
        await self.bot.logout()

def setup(bot):
    bot.add_cog(Administration(bot))
