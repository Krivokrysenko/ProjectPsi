# module imports
import configparser
from importlib import import_module
import json
import asyncio

# import enum codes
from agents.agent import Code

# class here
class NonaClass:
    def __init__(self):
        self.loadedmodules = {}
        self.instantiatedclasses = {}
        self.agentkeywords = {}
        self.shorttermmemory = {}

    async def setup(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        for agent in config["agents"]:
            self.loadedmodules[agent] = import_module(config["agents"][agent], "agents")
            self.instantiatedclasses[agent] = getattr(self.loadedmodules[agent],
                                                      config["agents"][agent][1:len(config["agents"][agent])])()
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
        return await self.summonAgent(tokens)

    async def summonAgent(self, tokens):
        for token in tokens:
            for agent in self.agentkeywords:
                keywords = self.agentkeywords[agent]
                if token in keywords:
                    self.shorttermmemory["currentAgent"] = self.instantiatedclasses[agent]
                    # this is when the nona actor asks the agent actor
                    code, output = await self.shorttermmemory["currentAgent"].interpret(tokens)
                    if code == Code.INFO:
                        return await self.requestFromUser(output)
                    elif code == Code.OUT:
                        return await self.outputToUser(output)

    async def requestFromUser(self, request):
        await self.outputToUser(request)
        answer = input()
        tokens = answer.split(" ")
        if any(word in tokens for word in self.shorttermmemory["cancelKeywords"]):
            return await self.outputToUser("Okay!")
        else:
            code, output = await self.shorttermmemory["currentAgent"].interpret(tokens)
            if code == Code.INFO:
                return await self.requestFromUser(output)
            elif code == Code.OUT:
                return await self.outputToUser(output)

    async def outputToUser(self, output):
        print(output)
        return output

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
        obj = getattr(self.loadedmodules[agentName], filename[1:len(filename)])()
        tempKeywords = obj.keywords
        if agentName in config["keywords"]:
            tempKeywords = tempKeywords + json.loads(config["keywords"][agentName])
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        self.instantiatedclasses[agentName] = obj
        self.agentkeywords[agentName] = tempKeywords
        return "successfully loaded"

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
        return "successfully unloaded"

# TODO remove this

async def test2():
    while True:
        await asyncio.sleep(3)
        print("oop")

async def test():
    asyncio.create_task(test2())
    while True:
        await asyncio.sleep(1)
        print("loop")

if __name__ == '__main__':
    # https://tutorialedge.net/python/concurrency/asyncio-event-loops-tutorial/
    NonaLoop = asyncio.new_event_loop()
    NonaLoop.create_task(test())
    NonaLoop.run_forever()