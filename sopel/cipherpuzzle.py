"""An IRC-based cipher puzzle game, inspired by sigma__

To submit puzzles, message Logician with $addpuzzle [text],
and the puzzle will be stored in the puzzle database and be announced to all active channels.

To submit a solve, usge $solve [n] [answer], where n is the puzzle ID and answer is your attempt."""

import string
import random
import traceback
from StringIO import StringIO
from sopel.module import commands,require_admin,require_privmsg
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.db import SopelDB
import sqlite3

# columns in order - ID,raw,encoded,solved,first
class CipuzzleSection(StaticSection):
    alpha = list(string.ascii_lowercase)
    alphabet = ValidatedAttribute('alphabet',list,default=alpha)

def setup(bot):
    bot.config.define_section('cipherpuzzle',CipuzzleSection)
    bot.db.connect()

@commands("cipuzzle","cipherpuzzle")
def aboutcip(bot,trigger):
    """Displays information about cipherpuzzle.
    Usage: $cipuzzle"""
    bot.reply("Cipher-puzzle is a text-based puzzle game wherein each letter of a phrase is encrypted with something similar to a simple Caesar replacement cipher.",trigger.nick)
    bot.reply("Your goal is to decrypt a message and send it via $solve.",trigger.nick)
    bot.reply("New puzzles of your own can be sent with $addpuzzle via private message, and they will be added into Logic's database, provided they aren't thinly disguised SQL injection attacks.",trigger.nick)
    bot.reply("Start by checking the list of puzzles via $listpuzzles. Good luck!",trigger.nick)

@require_privmsg("You should probably submit that via /msg.")
@commands("addpuzzle","submit")
def addpuzzle(bot,trigger):
    """Adds a puzzle to the Logician database.
    Usage: $addpuzzle puzzle"""
    bot.reply("Encoding!")
    coded = encode(bot,trigger.group(2))
    bot.reply("Encoded: " + coded[0])
    bot.reply("Given: " + coded[1])
    try:
        bot.db.execute("INSERT INTO puzzlelist (raw,encoded,solved,owner) VALUES (?,?,?,?);",[coded[1],coded[0],0,trigger.sender])
    except sqlite3.OperationalError:
        bot.say("Oops, looks like something went wrong. Try again, or tell centipeda.")
    x = bot.db.execute("SELECT * FROM puzzlelist WHERE ID = (SELECT MAX(ID) FROM puzzlelist);")
    id = str([x for x in x][0][0])
    bot.reply("Puzzle ID is " + id)

@commands("listpuzzles","puzzlelist","showpuzzles")
def listpuzzles(bot,trigger):
    """Outputs all the puzzles currently in the Logician cipherpuzzle database.
    Usage: $listpuzzles"""
    try:
        puz = int(trigger.group(2))
    except (ValueError, TypeError):
	puzzles = bot.db.execute("SELECT id, encoded, owner FROM puzzlelist;").fetchall()
        bot.say("Puzzles in database:",trigger.nick)
        for puzzle in puzzles:
            bot.say("Puzzle #{}: '{}', added by {}".format(puzzle[0],puzzle[1],puzzle[2]),trigger.nick)
    else:
        try:
            p = bot.db.execute("SELECT id, encoded, owner FROM puzzlelist where ID = ?;",(puz,)).fetchone()
            bot.say("Puzzle #{}: '{}', added by {}".format(p[0],p[1],p[2]))
	except:
            return 1

@require_privmsg("Ask via private message.")
@commands("showsolved")
def showsolved(bot,trigger):
    """Outputs solutions to currently solved puzzles.
    Usage: /msg (or /query) Logician $showsolved"""
    p = bot.db.execute("SELECT * FROM puzzlelist where solved = 1;")
    solved = [p for p in p]
    bot.say("Currently solved puzzles:",trigger.sender)
    for puzzle in solved:
        bot.say("Puzzle #{}: {}".format(puzzle[0],puzzle[2]),trigger.sender)
        bot.say("Solution: {}".format(puzzle[1]),trigger.sender)
        bot.say("First solved by {}".format(puzzle[4]))
        

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
            bot.reply("Yep, that's it! '{}' is the answer to puzzle #{}.".format(attempt,puzzleid))
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
    """Used by $addpuzzle to encode puzzles."""
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
