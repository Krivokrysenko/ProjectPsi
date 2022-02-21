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
        self.loadedmodules = {}
        self.instantiatedclasses = {}
        self.agentkeywords = {}

        # TODO make this create actor objects instead of class objects
        config = configparser.ConfigParser()
        config.read('config.ini')
        for agent in config["agents"]:
            self.loadedmodules[agent] = import_module(config["agents"][agent], "agents")
            self.instantiatedclasses[agent] = getattr(self.loadedmodules[agent],
                                                      config["agents"][agent][1:len(config["agents"][agent])])()
            if agent in config["keywords"]:
                self.agentkeywords[agent] = self.instantiatedclasses[agent].keywords() + json.loads(
                    config["keywords"][agent])
            else:
                self.agentkeywords[agent] = self.instantiatedclasses[agent].keywords()

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
            for agent in self.agentkeywords:
                keywords = self.agentkeywords[agent]
                if token in keywords:
                    self.shorttermmemory["currentAgent"] = self.instantiatedclasses[agent]
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
        self.agentkeywords[agentName] = self.agentkeywords[agentName] + [keyword]
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
        self.loadedmodules[agentName] = import_module(filename, "agents")
        obj = getattr(self.loadedmodules[agentName], filename[1:len(filename)])()
        tempKeywords = obj.keywords()
        if agentName in config["keywords"]:
            tempKeywords = tempKeywords + json.loads(config["keywords"][agentName])
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        self.instantiatedclasses[agentName] = obj
        self.agentkeywords[agentName] = tempKeywords
        return "successfully loaded"

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
        return "successfully unloaded"


# actor(s)/class(es) here
class NonaActor(Actor):
    def __init__(self):
        super().__init__()
        self.NonaObj = NonaClass()
        self.agentactors = {}
        for agent in self.NonaObj.loadedmodules:
            self.agentactors[agent] = self.createActor(self.NonaObj.loadedmodules[agent])

    def receiveMessage(self, msg, sender):
        match msg:
            case "test":
                self.send(sender, self.agentactors)


# TODO actually figure out the actors communication
if __name__ == '__main__':
    actsys = ActorSystem("multiprocTCPBase")
    Nona = actsys.createActor(NonaActor)
    print(actsys.ask(Nona, "test"))
