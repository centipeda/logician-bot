"""Used for setting MBTI roles in #INTP."""

import discord
from discord.ext import commands
import internal_checks as checks

class MBTITypes(object):

    def __init__(self, bot):
        self.bot = bot
        self.types = ["INTP","INFP","ISTP","ISFJ",
                      "ESFJ","ENTJ","INTJ","ISFP",
                      "ESTJ","ESFP","ISTJ","INFJ",
                      "ENFP","ENFJ","ENTP","ESTP"]
        self.testLink = "http://www.humanmetrics.com/cgi-win/jtypes2.asp"

    @commands.command(pass_context=True)
    @checks.msg_from_intp()
    async def type(self, ctx, mbti_type: str):
        """Sets a user's MBTI type role."""
        mbti = mbti_type.upper()
        usr = ctx.message.author
        serv = ctx.message.server
        if mbti in self.types:
            for role in usr.roles:
                if role.name in self.types:
                    await self.bot.remove_roles(usr, role)
                    print("removing role {}".format(role))
            for role in serv.roles:
                if role.name == mbti:
                    await self.bot.add_roles(usr, role)
                    print("adding role {}".format(role))
                    await self.bot.reply("successfully changed type role to {}.".format(mbti))

    @commands.command()
    @checks.msg_from_intp()
    async def test(self):
        """Prints an example MBTI test."""
        await self.bot.say("MBTI Test: {}".format(self.testLink))

def setup(bot):
    bot.add_cog(MBTITypes(bot))
