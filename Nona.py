# module imports
import configparser
from importlib import import_module
import json
import asyncio
import queue
from word2number import w2n

from codes import Codes
import voice

class Nona:
    def __init__(self):
        self.on = True  # flip to False while shutting down
        self.name = "nona"  # summon keyword, overwritten by config in setup
        self.voice = voice.Voice(self) # gets remade in setup with config name
        self.loadedmodules = {}
        self.instantiatedclasses = {}
        self.agentkeywords = {}
        self.shorttermmemory = {}
        self.queue = queue.Queue() # queue itself is threadsafe, objects inside are not
        self.setup()
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.voice.NonaListener())
        asyncio.ensure_future(self.pullFromQueue())
        loop.run_forever()

    def setup(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.name = config["name"]["name"]
        self.voice = voice.Voice(self)
        for agent in config["agents"]:
            self.loadedmodules[agent] = import_module(config["agents"][agent], "agents")
            self.instantiatedclasses[agent] = getattr(self.loadedmodules[agent], config["agents"][agent][1:len(config["agents"][agent])])(self)
            if agent in config["keywords"]:
                self.agentkeywords[agent] = self.instantiatedclasses[agent].keywords + json.loads(
                    config["keywords"][agent])
            else:
                self.agentkeywords[agent] = self.instantiatedclasses[agent].keywords
        self.shorttermmemory = {
            "cancelKeywords": json.loads(config["keywords"]["nonacancel"]),
            "currentAgent": None
        }

    async def addToQueue(self, code, outreq):
        self.queue.put([code, outreq])

    async def pullFromQueue(self):
        while self.on:
            pulled = None if self.queue.empty() else self.queue.get()
            if pulled is not None:
                match pulled[0]:
                    case Codes.OUT:
                        # TODO voice output
                        print(pulled[1])
                    case Codes.REQ:
                        await self.requestFromUser(pulled[1])
                    case Codes.INP:
                        await self.acceptInput(pulled[1])
                self.queue.task_done()
            await asyncio.sleep(0.01)

    # TODO ignore if it the name isn't in there
    async def acceptInput(self, userstring):
        tokens = []
        for word in userstring.split(" "):
            try:
                attempt = w2n.word_to_num(word)
            except:
                tokens.append(word)
            else:
                tokens.append(str(attempt))
        await self.summonAgent(tokens)

    async def summonAgent(self, tokens):
        for token in tokens:
            for agent in self.agentkeywords:
                keywords = self.agentkeywords[agent]
                if token in keywords:
                    self.shorttermmemory["currentAgent"] = self.instantiatedclasses[agent]
                    # this is when the nona actor asks the agent actor
                    asyncio.create_task(self.shorttermmemory["currentAgent"].interpret(tokens))

    async def requestFromUser(self, request):
        print(request)
        answer = input()
        tokens = answer.split(" ")
        if any(word in tokens for word in self.shorttermmemory["cancelKeywords"]):
            print("Okay!")
        else:
            asyncio.create_task(self.shorttermmemory["currentAgent"].interpret(tokens))

    async def addKeyword(self, agentName, keyword):
        self.agentkeywords[agentName] = self.agentkeywords[agentName] + [keyword]
        config = configparser.ConfigParser()
        config.read('config.ini')
        if agentName in config["keywords"]:
            config["keywords"][agentName] = json.dumps(json.loads(config["keywords"][agentName]) + [keyword])
        else:
            config["keywords"][agentName] = json.dumps([keyword])
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    # TODO these only work when not async which might be an issue down the line

    def loadAgent(self, agentName, filename):
        config = configparser.ConfigParser()
        config.read('config.ini')
        config["agents"][agentName] = filename
        self.loadedmodules[agentName] = import_module(filename, "agents")
        obj = getattr(self.loadedmodules[agentName], filename[1:len(filename)])(self)
        tempKeywords = obj.keywords
        if agentName in config["keywords"]:
            tempKeywords = tempKeywords + json.loads(config["keywords"][agentName])
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        self.instantiatedclasses[agentName] = obj
        self.agentkeywords[agentName] = tempKeywords

    def unloadAgent(self, agentName):
        config = configparser.ConfigParser()
        config.read('config.ini')
        config.remove_option("agents", agentName)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        if agentName in self.loadedmodules:
            self.loadedmodules.pop(agentName)
        if agentName in self.instantiatedclasses:
            self.instantiatedclasses.pop(agentName)
        if agentName in self.agentkeywords:
            self.agentkeywords.pop(agentName)

if __name__ == "__main__":
    Nona = Nona()