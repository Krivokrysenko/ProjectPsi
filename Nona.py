# should probably make an init and all and stuff but just manual import for now
from agents.AlArm import AlArm

agentKeywords = None

def acceptInput():
    return None

def summonAgent(userstring):
    tokens = userstring.split(" ")
    if "alarm" in tokens:
        alarm = AlArm()
        alarm.alarm(tokens)

def requestFromUser():
    return None

def outputToUser():
    return None

def loadAgent():
    return None

def unloadAgent():
    return None

summonAgent(input())