"""An IRC-based cipher puzzle game, inspired by sigma__

To submit puzzles, message Logician with $addpuzzle [text],
and the puzzle will be stored in the puzzle database and be announced to all active channels.

To submit a solve, usge $solve [n] [answer], where n is the puzzle ID and answer is your attempt."""

import string
import pickle
import random
from sopel.module import commands
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.db import SopelDB

class CipuzzleSection(StaticSection):
    alpha = list(string.ascii_lowercase)
    alphabet = ValidatedAttribute('alphabet',list,default=alpha)

def setup(bot):
    bot.config.define_section('cipherpuzzle',CipuzzleSection)

@commands("addpuzzle","submit")
def addpuzzle(bot,trigger):
    """Adds a puzzle to the Logician database."""
    if trigger.is_privmsg:
        bot.reply("Encoding!")
        coded = encode(bot,trigger.group(2))
        bot.reply("Encoded: " + coded[0])
        bot.reply("Given: " + coded[1])

@commands("solve","solvepuzzle","solvefor")
def solve(bot,trigger):
    """Checks if a given solution matches a puzzle's real solution."""
    pass


def encode(bot,string):
    alpha = bot.config.cipherpuzzle.alphabet
    solved = string
    shufflemap = alpha[:]
    random.shuffle(shufflemap)
    coded = []
    for word in string.lower().split():
        coded.append("".join([shufflemap[alpha.index(char)] for char in word if (char in alpha)]))
    encoded = " ".join(coded)
    # remember, encoded is first, then solved
    return encoded, solved
