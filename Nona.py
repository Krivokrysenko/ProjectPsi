# module imports
import configparser
from importlib import import_module
import json
from thespian.actors import *

# import enum codes
from agents.agent import Code

# class here
class NonaClass:
    def __init__(self):
        # code to dynamically import agents, might need to clean this up/move it
        self.loadedmods = {}
        self.instclasses = {}
        self.agentKeywords = {}

        config = configparser.ConfigParser()
        config.read('config.ini')
        for agent in config["agents"]:
            self.loadedmods[agent] = import_module(config["agents"][agent], "agents")
            self.instclasses[agent] = getattr(self.loadedmods[agent], config["agents"][agent][1:len(config["agents"][agent])])()
            if agent in config["keywords"]:
                self.agentKeywords[agent] = self.instclasses[agent].keywords() + json.loads(config["keywords"][agent])
            else:
                self.agentKeywords[agent] = self.instclasses[agent].keywords()

        # Nona go brrrrrrrr

        self.shorttermmemory = {
            "cancelKeywords": json.loads(config["keywords"]["nonacancel"]),
            "currentAgent": None
        }

    def acceptInput(self, userstring):
        tokens = userstring.split(" ")
        return self.summonAgent(tokens)

    def summonAgent(self, tokens):
        for token in tokens:
            for agent in self.agentKeywords:
                keywords = self.agentKeywords[agent]
                if token in keywords:
                    self.shorttermmemory["currentAgent"] = self.instclasses[agent]
                    # this is when the nona actor asks the agent actor
                    code, output = self.shorttermmemory["currentAgent"].interpret(tokens)
                    match code:
                        case Code.INFO:
                            return self.requestFromUser(output)
                        case Code.OUT:
                            return self.outputToUser(output)

    def requestFromUser(self, request):
        self.outputToUser(request)
        answer = input()
        tokens = answer.split(" ")
        if any(word in tokens for word in self.shorttermmemory["cancelKeywords"]):
            return self.outputToUser("Okay!")
        else:
            code, output = self.shorttermmemory["currentAgent"].interpret(tokens)
            match code:
                case Code.INFO:
                    return self.requestFromUser(output)
                case Code.OUT:
                    return self.outputToUser(output)

    def outputToUser(self, output):
        print(output)
        return output

    def addKeyword(self, agentName, keyword):
        self.agentKeywords[agentName] = self.agentKeywords[agentName] + [keyword]
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
        self.loadedmods[agentName] = import_module(filename, "agents")
        obj = getattr(self.loadedmods[agentName], filename[1:len(filename)])()
        tempKeywords = obj.keywords()
        if agentName in config["keywords"]:
            tempKeywords = tempKeywords + json.loads(config["keywords"][agentName])
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        self.instclasses[agentName] = obj
        self.agentKeywords[agentName] = tempKeywords
        return "successfully loaded"

    def unloadAgent(self, agentName):
        config = configparser.ConfigParser()
        config.read('config.ini')
        config.remove_option("agents", agentName)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        self.loadedmods.pop(agentName)
        self.instclasses.pop(agentName)
        self.agentKeywords.pop(agentName)
        return "successfully unloaded"

# actor(s)/class(es) here
class NonaActor(Actor):
    class AgentActor(Actor):
        def __init__(self):
            super().__init__()
            self.NonaObj = NonaClass()

    def receiveMessage(self, msg, sender):
        print(msg)

if __name__ == '__main__':
    # witchcraft goes here
    actsys = ActorSystem("multiprocTCPBase")
    Nonaactor = actsys.createActor(NonaActor)