# module imports
import configparser
from importlib import import_module
import json
# import enum codes
from agents.agent import Code

# code to dynamically import agents, might need to clean this up/move it
loadedmods = {}
instclasses = {}
agentKeywords = {}

config = configparser.ConfigParser()
config.read('config.ini')
for agent in config["agents"]:
    loadedmods[agent] = import_module(config["agents"][agent], "agents")
    instclasses[agent] = getattr(loadedmods[agent], config["agents"][agent][1:len(config["agents"][agent])])()
agentKeywords = json.loads(config["keywords"]["keywords"])

# Nona go brrrrrrrr

currentAgent = None

def acceptInput(userstring):
    tokens = userstring.split(" ")
    return summonAgent(tokens)

def summonAgent(tokens):
    for token in tokens:
        for agent in agentKeywords:
            keywords = agentKeywords[agent]
            if token in keywords:
                currentAgent = instclasses[agent]
                code, output = currentAgent.interpret(tokens)
                match code:
                    case Code.INFO:
                        return requestFromUser(output)
                    case Code.OUT:
                        return outputToUser(output)

def requestFromUser(request):
    outputToUser(request)
    answer = input()
    # send back to agent?
    return request

def outputToUser(output):
    print(output)
    return output

def loadAgent(agentName, filename):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config["agents"][agentName] = filename
    loadedmods[agentName] = import_module(filename, "agents")
    obj = getattr(loadedmods[agentName], filename[1:len(filename)])()
    configkeywords = json.loads(config["keywords"]["keywords"])
    configkeywords[agentName] = obj.keywords()
    config["keywords"]["keywords"] = json.dumps(configkeywords)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    instclasses[agentName] = obj
    agentKeywords[agentName] = obj.keywords()
    return "successfully loaded"

def unloadAgent(agentName):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.remove_option("agents", agentName)
    configkeywords = json.loads(config["keywords"]["keywords"])
    configkeywords.pop(agentName)
    config["keywords"]["keywords"] = json.dumps(configkeywords)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    loadedmods.pop(agentName)
    instclasses.pop(agentName)
    agentKeywords.pop(agentName)
    return "successfully unloaded"