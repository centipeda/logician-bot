"""Play a game of Tic-Tac-Toe with Logician!"""

import tictactoe
import discord
from discord.ext import commands

class TicTacToe(object):

    def __init__(self, bot):
        self.bot = bot
        self.playing = False
        self.game = tictactoe.BeginningState()
        self.ai = tictactoe.AIPlayer()

    @commands.group(pass_context=True)
    async def ttt(self, ctx):
        """Begins, plays, or ends a game of tic-tac-toe."""

    @ttt.group(pass_context = True)
    async def play(self, ctx, x : int, y : int):
        """If a game of tic-tac-toe has not already been started, begins one.
        If a starting move is given, lets you move first, otherwise, Logic
        will."""
        if not self.playing:
            print("Beginning tic-tac-toe")
            self.playing = True
            await self.bot.reply("Let's play!")
            if x is not None and y is not None:
                print("{} moving first".format(ctx.message.author))
                self.game.board[x][y] = tictactoe.OPPONENT_SYMBOL
                await self.bot.say("Your move: {} {}".format(x,y))
                await self.bot.say("```{}```".format(self.game.__str__()))
                await self.bot.say("My turn!")
                self.game = self.ai.move(self.game)
                await self.bot.say("```{}```".format(self.game.__str__()))
            else:
                print("I'm moving first")
                self.game = self.ai.starter_move(self.game)
                await self.bot.say("```{}```".format(self.game.__str__()))

        else:
            self.game.board[x][y] = tictactoe.OPPONENT_SYMBOL
            await self.bot.say("Your move: {} {}".format(x,y))
            await self.bot.say("```{}```".format(self.game.__str__()))
            if await self.check_win():
                return
            await self.bot.say("My turn!")
            self.game = self.ai.move(self.game)
            await self.bot.say("```{}```".format(self.game.__str__()))
            if await self.check_win():
                return

    @ttt.group(pass_context = True)
    async def end(self, ctx):
        """Ends the current game of tic-tac-toe."""
        if self.playing:
            await self.bot.say("You admit defeat! Ha-ha!")
            await self.bot.say("```Final state:\n{}```".format(self.game.__str__()))
            self.playing = False
            self.game = tictactoe.BeginningState()

    @ttt.group()
    async def board(self):
        """Shows the current state of the board, if a game is currently being
        played."""
        if self.playing:
            await self.bot.say("Board state:")
            await self.bot.say("```{}```".format(self.game.__str__()))

    async def check_win(self):
        pts = tictactoe.check_win(self.game.board)
        if pts is not None:
            if pts == 10:
                await self.bot.say("Hah! I knew I'd win!")
            elif pts == -10:
                await self.bot.say("What?! How?!")
            elif pts == 0:
                await self.bot.say("A draw, then.")

            await self.bot.say("```Final state:\n{}```".format(self.game.__str__()))
            self.playing = False
            self.game = tictactoe.BeginningState()

            return True
        else:
            return False

def setup(bot):
    bot.add_cog(TicTacToe(bot))
