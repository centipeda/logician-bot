"""An IRC-based cipher puzzle game, inspired by sigma__

To submit puzzles, message Logician with $addpuzzle [text],
and the puzzle will be stored in the puzzle database and be announced to all active channels.

To submit a solve, usge $solve [n] [answer], where n is the puzzle ID and answer is your attempt."""

import string
import random
import traceback
from StringIO import StringIO
from sopel.module import commands,require_admin
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.db import SopelDB
import sqlite3

class CipuzzleSection(StaticSection):
    alpha = list(string.ascii_lowercase)
    alphabet = ValidatedAttribute('alphabet',list,default=alpha)

def setup(bot):
    bot.config.define_section('cipherpuzzle',CipuzzleSection)
    bot.db.connect()

@commands("addpuzzle","submit")
def addpuzzle(bot,trigger):
    """Adds a puzzle to the Logician database."""
    if trigger.is_privmsg:
        bot.reply("Encoding!")
        coded = encode(bot,trigger.group(2))
        bot.reply("Encoded: " + coded[0])
        bot.reply("Given: " + coded[1])
        try:
            bot.db.execute("INSERT INTO puzzlelist (raw,encoded) VALUES (?,?,?);",(coded[1],coded[0],0))
        except sqlite3.OperationalError:
            bot.say("...Hey, did you try an SQL injection attack?")

        x = bot.db.execute("SELECT * FROM puzzlelist WHERE ID = (SELECT MAX(ID) FROM puzzlelist);")
        id = [x for x in x][0]
        bot.reply("Puzzle ID is " + id)

@commands("listpuzzles","puzzlelist","showpuzzles")
def listpuzzles(bot,trigger):
    """Outputs all the puzzles currently in the Logician cipherpuzzle database."""
    p = bot.db.execute("SELECT id, encoded FROM puzzlelist;")
    puzzles = [p for p in p]
    bot.say("Puzzles in database:")
    for puzzle in puzzles:
        bot.say("Puzzle #{}: {}".format(puzzle[0],puzzle[1]))

@commands("showsolved")
def showsolved(bot,trigger):
    """Outputs solutions to currently solved puzzles."""
    p = bot.db.execute("SELECT * FROM puzzlelist where solved = 1;")
    solved = [p for p in p]
    bot.say("Currently solved puzzles:",trigger.sender)
    for puzzle in solved:
        bot.say("Puzzle #{}: {}".format(puzzle[0],puzzle[2]),trigger.sender)
        bot.say("Solution: {}".format(puzzle[1]),trigger.sender)
        

@commands("solve","solvepuzzle","solvefor")
def solve(bot,trigger):
    """Checks if a given solution matches a puzzle's real solution.
    Usage: $solve 1 the quick brown fox
    Output: Sorry, "the quick brown fox" isn't the solution to puzzle 1."""
    if trigger.group(2) is None or len(trigger.group(2)) <= 1:
        pass
    else:
        split = trigger.group(2).split()
        puzzleid = split[0]
        attempt = " ".join(split[1::])
        p = bot.db.execute("SELECT * FROM puzzlelist where ID = ?;",(puzzleid,))
        puzzle = [p for p in p]
        if (str(puzzle[0][1]) == str(attempt)):
            bot.reply("Yep, that's it. '{}' is the answer to puzzle #{}.".format(attempt,puzzleid))
            bot.db.execute("UPDATE puzzlelist SET solved = 1 WHERE ID = ?;",(puzzleid,))
        else:
            bot.reply("Sorry, that's not it. Try again?")
        
        
@require_admin
@commands("resetpuzzle")
def resetpuzzle(bot,trigger):
    """Sets a puzzle to unsolved again if it was solved. Admin-only command."""
    pass

@require_admin
@commands("removepuzzle","delpuzzle","deletepuzzle")
def removepuzzle(bot,trigger):
    """Removes a puzzle from the database. Admin-only command."""
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
