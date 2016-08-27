# coding: utf-8
"""Random other commands."""

import random

from sopel.module import commands,require_admin
from sopel.module import rule
from sopel.config.types import StaticSection,ValidatedAttribute

class MiscConfig(StaticSection):
    ballansw = ["Yes.",
                "Not in any conceivable scenario.",
                "Undoubtedly.",
                "I doubt it, for some reason.",
                "Time will tell.",
                "Why do you need to know?",
                "No.",
                "Why?",
                "Perhaps.",
                "Ask another time.",
                "That seems plausible.",
                "That would be... unlikely.",
                "But... why?",
                "Nope.",
                "Maybe!",
                "Sorry, what was that?"]
    uses = ["equips","wields"]
    awords = ["utilizes","uses","applies","plies"]
    answers = ValidatedAttribute("answers",list,default=ballansw)
    quipfile = ValidatedAttribute("quipfile",str,default="/home/crit/.sopel/modules/1liners.cap")
    quiplist = ValidatedAttribute("quiplist",list,default=[])
    actionwords = ValidatedAttribute("actionwords",list,default=awords)
    equips = ValidatedAttribute("equips",list,default=uses)

def setup(bot):
    bot.config.define_section('misc',MiscConfig)
    quipfile = open(bot.config.misc.quipfile,"r")
    for line in quipfile.readlines():
        if line != "     \r\n":
            bot.config.misc.quiplist.append(line[5:-2])
    itms = bot.db.execute("SELECT item FROM inventory;").fetchall()
    bot.memory["inventory"] = [thing[0] for thing in itms]
    gold = bot.db.execute("SELECT gold FROM INVENTORY;").fetchone()[0]
    bot.memory["gold"] = int(gold)
    bot.memory["equipped"] = None

@commands("8ball","8b","eightball")
def eightball(bot,trigger):
    """Consult the magic 8-ball for answers."""
    if trigger.group(2) is None:
        return None
    elif trigger.group(2)[-1] != "?":
        bot.reply("Please ask a yes or no question.")
    else:
        # bot.reply(random.choice(bot.config.miscellaneous.answers))
        total = 0
        for char in trigger.group(2)[::-1]:
            total += ord(char)
        bot.reply(bot.config.misc.answers[total % len(bot.config.misc.answers)])

@commands("flip","flipcoin")
def flip_coin(bot,trigger):
    """Flips a coin and prints the result."""
    if trigger.group(2) is not None and type(eval(trigger.group(2))) == int:
        bot.reply(", ".join([random.choice(("Heads","Tails")) for n in range(eval(trigger.group(2)))]))
    else:
        bot.reply(random.choice(["Heads!","Tails!"]))
        
@commands("inventory","inv","in")
def inventory(bot,trigger):
    try:
        argmnts = trigger.group(2).split()
    except AttributeError:
        bot.say("Try $inv [list|put|remove|equip|dequip]")
        argmnts = None
    else:
        item = " ".join(argmnts[1::])
        requirethere = ["remove","equip","use"]
    if argmnts is None:
        pass
    elif item not in bot.memory["inventory"] and argmnts[0] in requirethere:
        bot.say("Item {} not in inventory!".format(item))
    elif item is None:
        item = "nothing"
    elif argmnts[0] == "list":
        bot.say("Current items in inventory: " + ", ".join(bot.memory["inventory"]))
    elif argmnts[0] == "put":
        bot.memory["inventory"].append(item)
        bot.db.execute("INSERT INTO inventory (item) VALUES (?);",(item,))
        bot.action("places a {} into his inventory".format(item))
    elif argmnts[0] == "remove":
        bot.memory["inventory"].remove(item)
        bot.action("removes {} from his inventory".format(item))
        bot.db.execute("DELETE FROM inventory WHERE item = ?;",(item,))
    elif argmnts[0] == "equip":
        if bot.memory["equipped"] == item:
            bot.say("Already equipped that!")
        elif bot.memory["equipped"] is not None and item in bot.memory["inventory"]:
            act = "puts away his {} and {} his {}".format(bot.memory["equipped"],random.choice(bot.config.misc.equips),item)
            bot.action(act)
            bot.memory["equipped"] = item
        else:
            bot.memory["equipped"] = item
            bot.action(random.choice(bot.config.misc.equips) + " his " + item)
    elif argmnts[0] == "use":
        if item is not None and item in bot.memory["inventory"]:
            act = "{} his {}".format(random.choice(bot.config.misc.actionwords),item)
        elif bot.memory["equipped"] is None or bot.memory["equipped"] == "nothing":
            bot.say("Nothing equipped!")
            pass
        else:
            act = "{} his {}".format(random.choice(bot.config.misc.actionwords),bot.memory["equipped"])
        bot.action(act)
        
    elif argmnts[0] == "dequip":
        if bot.memory["equipped"] is None:
            bot.say("Nothing equipped!")
        else:
            bot.action("dequips his {}".format(item))
            bot.memory["equipped"] = None
    elif argmnts[0] == "equipped":
        if bot.memory["equipped"] is None or bot.memory["equipped"] == "nothing":
            bot.say("Nothing equipped!")
        else:
            bot.say("My {} is currently equipped.".format(bot.memory["equipped"]))

@commands("quip")
def quip(bot,trigger):
    """Has Logician say something from his quiplist."""
    if trigger.group(2) is not None and type(eval(trigger.group(2))) is int:
        bot.say(bot.config.misc.quiplist[eval(trigger.group(2)) - 1])
    else:
        bot.say(random.choice(bot.config.misc.quiplist))

@commands("complain","complaint","cmpln")
def complain(bot, trigger):
    """Registers a complaint with Logician"""
    complaint = trigger.group(2)
    bot.db.execute("INSERT INTO complaints (victim,complaint) VALUES (?,?);",(trigger.nick,complaint))
    bot.say("Complaint '{}' filed. Thanks for your input!".format(complaint))

@require_admin("Only my administrators can view complaints.")
@commands("complaints")
def complaints(bot, trigger):
    """Displays all the currently registered complaints."""
    compls = bot.db.execute("SELECT * FROM complaints;").fetchall()
    for comp in compls:
        bot.say("Complaint #{}: '{}', filed by {}".format(str(comp[0]),comp[2],comp[1]),trigger.nick)

@commands("douse","mindbleach","bleach")
def douse(bot,trigger):
    """Usage: $douse user"""
    bot.action("douses " + trigger.group(2) + " with mind bleach")

@commands("slap")
def slap(bot,trigger):
    """Usage: $slap user"""
    bot.say("I'd rather not.")

@commands("fliptable")
def fliptable(bot,trigger):
    """Usage: $fliptable"""
    bot.say("(╯°□°)╯︵ ┻━┻")

@commands("unflip")
def unfliptable(bot,trigger):
    """Usage: $unfliptable"""
    bot.say("┬─┬﻿ ノ( ゜-゜ノ)")

@commands("lenny")
def lenny(bot,trigger):
    """Usage: $lenny"""
    lennyface(bot,trigger)

@rule("[Yy]ou like that, Logic(ian)?")
def lennyface(bot,trigger):
    bot.say("( ͡° ͜ʖ ͡°)")
