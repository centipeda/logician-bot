"""Used for setting MBTI roles in #INTP."""

import discord
from discord.ext import commands

def check_server(message):
    return message.server.id == "188684307278069760"

def is_intp_server():
    return commands.check(lambda ctx: check_server(ctx.message))

class MBTITypes(object):

    def __init__(self, bot):
        self.bot = bot
        self.types = ["INTP","INFP","ISTP","ISFJ",
                      "ESFJ","ENTJ","INTJ","ISFP",
                      "ESTJ","ESFP","ISTJ","INFJ",
                      "ENFP","ENFJ","ENTP","ESTP"]

    @commands.command(pass_context=True)
    @is_intp_server()
    async def type(self, ctx, mbti_type: str):
        """Sets a user's MBTI type role."""
        mbti = mbti_type.upper()
        usr = ctx.message.author
        serv = ctx.message.server
        for role in usr.roles:
            if role.name in self.types:
                await self.bot.remove_roles(usr, role)
                print("removing role {}".format(role))
        if mbti in self.types:
            for role in serv.roles:
                if role.name == mbti:
                    await self.bot.add_roles(usr, role)
                    print("adding role {}".format(role))
                    await self.bot.reply("Successfully changed type to {}.".format(mbti))

def setup(bot):
    bot.add_cog(MBTITypes(bot))
