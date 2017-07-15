"""Various checks."""

from discord.ext import commands

def is_from_centipeda():
    return commands.check(lambda ctx: ctx.message.author.id == "185877810760515585")

def is_from_user(user_id):
    return commands.check(lambda ctx: ctx.message.author.id == user_id)

def msg_from_server(server_id):
    """Checks if message originated from given server id."""
    return commands.check(lambda ctx: ctx.message.server.id == server_id)

def msg_from_intp():
    """Checks if message originated from the #intp server."""
    return commands.check(lambda ctx: ctx.message.server.id=="188684307278069760")
