import os.path
from random import choice as rchoice
import datetime
import copy
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
import internal_checks

class TopicChooser(object):
    """Rotates topics at a chosen interval."""

    def __init__(self, bot):
        self.bot = bot
        self.path = "data/topic/settings.json"
        self.settings = dataIO.load_json(self.path)
        self.bot.loop.create_task(self._rotate_topic())

    def _select_topic(self, mode):
        if mode == "old":
            tid = rchoice(list(self.settings["topics"].keys()))
        elif mode == "new":
            tid = self.settings["topic_queue"].pop()
            dataIO.save_json(self.path, self.settings)
        else:
            tid = mode
        return self.settings["topics"][tid]["content"]

    async def _monitor_topic(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            await self._rotate_topic()
            asyncio.sleep(self.settings["interval"] * 3600) # in hours

    async def _rotate_topic(self, topicid = None):
            chanstr = 'Daily topic: "{}". Please be civil.'
            chan = self.bot.get_channel(self.settings["topic_channel"])
            if topicid is None:
                if self.settings["topic_queue"] == []:
                    print("choosing from old topics")
                    topic = self._select_topic("old")
                else:
                    print("choosing from new topic queue")
                    topic = self._select_topic("new")
            else:
                topic = self._select_topic(str(topicid))

            await self.bot.edit_channel(chan, topic=chanstr.format(topic))
            self.settings["current_topic"] = topic
            dataIO.save_json(self.path, self.settings)
            print("successfuly changed topic to {}".format(topic))

    @internal_checks.is_from_centipeda()
    @commands.group()
    async def rotatetopic(self):
        """Randomly rotates the topic to a preregistered one."""
        await self._rotate_topic()
        await self.bot.say("Forcibly rotated topic.")

    @internal_checks.is_from_centipeda()
    @commands.command()
    async def switchtopic(self, topicid : int):
        """Switches the topic to the given topicid."""
        await self._rotate_topic(topicid)

    @commands.command()
    async def lstopic(self, topicid : int):
        """Lists the information about a given registered topic. Uses its topicid."""
        topic = self.settings["topics"][str(topicid)]
        await self.bot.say(topic)

    @internal_checks.is_from_centipeda()
    @commands.command()
    async def deltopic(self, topicid : int):
        """Deletes a topic given its id."""
        self.settings["topics"].pop(str(topicid), None)
        await self.bot.say("Deleted topic with id #{}".format(topicid))
        dataIO.save_json(self.path, self.settings)

    @commands.command(pass_context=True)
    async def addtopic(self, ctx, topic : str):
        """Adds a topic to the topic queue."""
        topics = [(tid,self.settings["topics"][tid]["content"]) for tid in self.settings["topics"].keys()]
        for tid, top in topics:
            if top == topic:
                self.settings["topic_queue"].insert(0, tid)
                await self.bot.say("Added {} (id {}) to topic queue.".format(top, tid))
                break
        else:
            if self.settings["topics"] == {}:
                newid = 0
            else:
                ids = [int(i) for i in self.settings["topics"].keys()]
                newid = str(sorted(ids)[-1] + 1)
            data = {"content":topic,
                    "creator": ctx.message.author.name,
                    "created_at": datetime.datetime.utcnow().ctime()
                    }
            self.settings["topics"][newid] = data
            self.settings["topic_queue"].insert(0, newid)
            await self.bot.say("Added new topic {} (id {}) to topic queue.".format(topic, newid))
        dataIO.save_json(self.path, self.settings)

    @commands.command()
    async def topicqueue(self, topicid : int=None):
        """Lists the current topic queue."""
        if topicid is None:
            liststr = "```Current topic: {}\n{}```"
            tops = [(tid,self.settings["topics"][tid]["content"]) for tid in self.settings["topic_queue"]]
            fin = "\n".join(["#{} : {}".format(tid,top) for tid,top in tops[::-1]])
            await self.bot.say(liststr.format(self.settings["current_topic"],fin))
        else:
            try:
                topic = self.settings["topics"][str(topicid)]
            except:
                await self.bot.say("Topic not found.")
                return
            else:
                infostr = "```Listing topic #{}:\nContent: {}\nCreator: {}\nCreated: {}```"
                await self.bot.say(infostr.format(topicid,topic["content"],topic["creator"],topic["created_at"]))

def check_folder():
    if not os.path.exists("data/topic"):
        print("creating data/topic")
        os.makedirs("data/topic")

def check_file():
    defaults = { "interval" : 60,
                 "topic_channel" : "226682975729876995",
                 "current_topic" : "testing",
                 "topic_queue" : [],
                 "topics" : {}
                 }
    s = "data/topic/settings.json"
    if not dataIO.is_valid_json(s):
        print("creating topic/settings.json")
        dataIO.save_json(s, defaults)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(TopicChooser(bot))
