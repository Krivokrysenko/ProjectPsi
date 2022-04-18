# module imports
import configparser
from importlib import import_module
import json
import asyncio
import queue

# TODO move this????
# import enum codes
from agents.agent import Code

class Nona:
    def __init__(self):
        self.loadedmodules = {}
        self.instantiatedclasses = {}
        self.agentkeywords = {}
        self.shorttermmemory = {}
        # queue itself is threadsafe, objects inside are not
        self.queue = queue.Queue()
        self.setup()

    def setup(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
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

    # async def listen(self):
    # TODO concurrent listening that adds voice input to queue

    # TODO this should pull inputs from queue
    async def acceptInput(self, userstring):
        tokens = userstring.split(" ")
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

    async def addToQueue(self, code, outreq):
        self.queue.put([code, outreq])

    async def pullFromQueue(self):
        # TODO IN stuff
        pulled = None if self.queue.empty() else self.queue.get()
        if pulled is not None:
            match pulled[0]:
                case Code.OUT:
                    print(pulled[1])
                case Code.REQ:
                    await self.requestFromUser(pulled[1])
            self.queue.task_done()

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

    async def loadAgent(self, agentName, filename):
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

    async def unloadAgent(self, agentName):
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