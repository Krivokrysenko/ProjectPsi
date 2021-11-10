import configparser
from importlib import import_module

# code to dynamically import agents, might need to clean this up/move it

loadedmods = {}

config = configparser.ConfigParser()
config.read('config.ini')
for agent in config["agents"]:
    loadedmods[agent] = import_module(config["agents"][agent], "agents")

# import enum codes

from agents.agent import Code

# uh dunno what i'm doing with this yet

agentKeywords = []

# Nona go brrrrrrrr

def acceptInput(userstring):
    tokens = userstring.split(" ")
    summonAgent(tokens)

def summonAgent(tokens):
    if "alarm" in tokens:
        AlArm = getattr(loadedmods["alarm"], "AlArm")
        alarm = AlArm()
        code, output = alarm.interpret(tokens)
        match code:
            case Code.INFO:
                requestFromUser(output)
            case Code.OUT:
                outputToUser(output)

def requestFromUser(request):
    outputToUser(request)
    answer = input()
    # send back to agent?

def outputToUser(output):
    print(output)

def loadAgent(agentName, filename):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config["agents"][agentName] = filename
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    loadedmods[agentName] = import_module(filename, "agents")

def unloadAgent(agentName, filename):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config["agents"][agentName] = filename
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# """testing"""

# loadAgent("alarm", ".AlArm")
acceptInput(input())