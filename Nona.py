# module imports
import configparser
from importlib import import_module
import json
import asyncio

class Nona:
    def __init__(self):
        self.loadedmodules = {}
        self.instantiatedclasses = {}
        self.agentkeywords = {}
        self.shorttermmemory = {}
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
        # TODO test this/does this actually work
        # TODO queue system?
        await self.outputToUser(request)
        answer = input()
        tokens = answer.split(" ")
        if any(word in tokens for word in self.shorttermmemory["cancelKeywords"]):
            # TODO keep this or move to outputToUser?
            print("Okay!")
        else:
            asyncio.create_task(self.shorttermmemory["currentAgent"].interpret(tokens))

    async def outputToUser(self, output):
        # TODO add queue system?
        print(output)

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