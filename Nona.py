# module imports
import configparser
from importlib import import_module
import json
from thespian.actors import *

# import enum codes
from agents.agent import Code

# actor(s)/class(es) here
class NonaActor(Actor):
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

actsys = ActorSystem("multiprocTCPBase")
Nonaactor = actsys.createActor(NonaActor)

def acceptInput(userstring):
    tokens = userstring.split(" ")
    return summonAgent(tokens)

def summonAgent(tokens):
    for token in tokens:
        for agent in agentKeywords:
            keywords = agentKeywords[agent]
            if token in keywords:
                shorttermmemory["currentAgent"] = instclasses[agent]
                # this is when the nona actor asks the agent actor
                code, output = shorttermmemory["currentAgent"].interpret(tokens)
                match code:
                    case Code.INFO:
                        return requestFromUser(output)
                    case Code.OUT:
                        return outputToUser(output)

def requestFromUser(request):
    outputToUser(request)
    answer = input()
    tokens = answer.split(" ")
    if any(word in tokens for word in shorttermmemory["cancelKeywords"]):
        return outputToUser("Okay!")
    else:
        code, output = shorttermmemory["currentAgent"].interpret(tokens)
        match code:
            case Code.INFO:
                return requestFromUser(output)
            case Code.OUT:
                return outputToUser(output)

def outputToUser(output):
    print(output)
    return output

def addKeyword(agentName, keyword):
    agentKeywords[agentName] = agentKeywords[agentName] + [keyword]
    config = configparser.ConfigParser()
    config.read('config.ini')
    if agentName in config["keywords"]:
        config["keywords"][agentName] = json.dumps(json.loads(config["keywords"][agentName]) + [keyword])
    else:
        config["keywords"][agentName] = json.dumps([keyword])
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def loadAgent(agentName, filename):
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

def unloadAgent(agentName):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.remove_option("agents", agentName)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    loadedmods.pop(agentName)
    instclasses.pop(agentName)
    agentKeywords.pop(agentName)
    return "successfully unloaded"