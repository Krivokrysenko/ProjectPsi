# module imports
import configparser
import time
from importlib import import_module
import json
import ray

# TODO move this?
ray.init()
# use this to debug by forcing onto single process:
# ray.init(local_mode=True)

# import enum codes
from agents.agent import Code

# class here
class NonaClass:
    def __init__(self):
        # code to dynamically import agents, might need to clean this up/move it
        self.loadedmodules = {}
        self.instantiatedclasses = {}
        self.agentkeywords = {}

        # TODO make this create actor objects instead of class objects (this is still an issue with ray lol)
        config = configparser.ConfigParser()
        config.read('config.ini')
        for agent in config["agents"]:
            self.loadedmodules[agent] = import_module(config["agents"][agent], "agents")
            self.instantiatedclasses[agent] = getattr(self.loadedmodules[agent],
                                                      config["agents"][agent][1:len(config["agents"][agent])]).remote()
            if agent in config["keywords"]:
                self.agentkeywords[agent] = ray.get(self.instantiatedclasses[agent].keywords.remote()) + json.loads(
                    config["keywords"][agent])
            else:
                self.agentkeywords[agent] = ray.get(self.instantiatedclasses[agent].keywords.remote())

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
                    code, output = ray.get(self.shorttermmemory["currentAgent"].interpret.remote(tokens))
                    if code == Code.INFO:
                        return self.requestFromUser(output)
                    elif code == Code.OUT:
                        return self.outputToUser(output)

    def requestFromUser(self, request):
        self.outputToUser(request)
        answer = input()
        tokens = answer.split(" ")
        if any(word in tokens for word in self.shorttermmemory["cancelKeywords"]):
            return self.outputToUser("Okay!")
        else:
            code, output = ray.get(self.shorttermmemory["currentAgent"].interpret.remote(tokens))
            if code == Code.INFO:
                return self.requestFromUser(output)
            elif code == Code.OUT:
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
        obj = getattr(self.loadedmodules[agentName], filename[1:len(filename)]).remote()
        tempKeywords = ray.get(obj.keywords.remote())
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


# TODO finish conversion (ray.get, etc)
if __name__ == '__main__':
    print("hi :-)")