# module imports
import configparser
from importlib import import_module
import json
from thespian.actors import *

# import enum codes
from agents.agent import Code

# witchcraft goes here
# actsys = ActorSystem("multiprocTCPBase")
# Nonaactor = actsys.createActor(NonaActor)

# class here
class NonaClass:
    def acceptInput(self, userstring):
        tokens = userstring.split(" ")
        return self.summonAgent(tokens)

    def summonAgent(self, tokens):
        for token in tokens:
            for agent in agentKeywords:
                keywords = agentKeywords[agent]
                if token in keywords:
                    shorttermmemory["currentAgent"] = instclasses[agent]
                    # this is when the nona actor asks the agent actor
                    code, output = shorttermmemory["currentAgent"].interpret(tokens)
                    match code:
                        case Code.INFO:
                            return self.requestFromUser(output)
                        case Code.OUT:
                            return self.outputToUser(output)

    def requestFromUser(self, request):
        self.outputToUser(request)
        answer = input()
        tokens = answer.split(" ")
        if any(word in tokens for word in shorttermmemory["cancelKeywords"]):
            return self.outputToUser("Okay!")
        else:
            code, output = shorttermmemory["currentAgent"].interpret(tokens)
            match code:
                case Code.INFO:
                    return self.requestFromUser(output)
                case Code.OUT:
                    return self.outputToUser(output)

    def outputToUser(self, output):
        print(output)
        return output

    def addKeyword(self, agentName, keyword):
        agentKeywords[agentName] = agentKeywords[agentName] + [keyword]
        config = configparser.ConfigParser()
        config.read('config.ini')
        if agentName in config["keywords"]:
            config["keywords"][agentName] = json.dumps(json.loads(config["keywords"][agentName]) + [keyword])
        else:
            config["keywords"][agentName] = json.dumps([keyword])
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def loadAgent(self, agentName, filename):
        config = configparser.ConfigParser()
        config.read('config.ini')
        config["agents"][agentName] = filename
        loadedmods[agentName] = import_module(filename, "agents")
        obj = getattr(loadedmods[agentName], filename[1:len(filename)])()
        tempKeywords = obj.keywords()
        if agentName in config["keywords"]:
            tempKeywords = tempKeywords + json.loads(config["keywords"][agentName])
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        instclasses[agentName] = obj
        agentKeywords[agentName] = tempKeywords
        return "successfully loaded"

    def unloadAgent(self, agentName):
        config = configparser.ConfigParser()
        config.read('config.ini')
        config.remove_option("agents", agentName)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        loadedmods.pop(agentName)
        instclasses.pop(agentName)
        agentKeywords.pop(agentName)
        return "successfully unloaded"

# actor(s)/class(es) here
class NonaActor(Actor):
    class AgentActor(Actor):
        def __init__(self):
            super().__init__()
            self.NonaObj = NonaClass()

    def receiveMessage(self, msg, sender):
        print(msg)

# code to dynamically import agents, might need to clean this up/move it
loadedmods = {}
instclasses = {}
agentKeywords = {}

config = configparser.ConfigParser()
config.read('config.ini')
for agent in config["agents"]:
    loadedmods[agent] = import_module(config["agents"][agent], "agents")
    instclasses[agent] = getattr(loadedmods[agent], config["agents"][agent][1:len(config["agents"][agent])])()
    if agent in config["keywords"]:
        agentKeywords[agent] = instclasses[agent].keywords() + json.loads(config["keywords"][agent])
    else:
        agentKeywords[agent] = instclasses[agent].keywords()

# Nona go brrrrrrrr

shorttermmemory = {
    "cancelKeywords": json.loads(config["keywords"]["nonacancel"]),
    "currentAgent": None
}