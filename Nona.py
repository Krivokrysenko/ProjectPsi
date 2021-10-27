# should probably make an init and all and stuff but just manual import for now
from agents import AlArm

keywords = None

def acceptInput():
    return None

def summonAgent(userstring):
    tokens = userstring.split(" ")
    if "alarm" in tokens:
        AlArm.alarm(tokens)

def requestFromUser():
    return None

def outputToUser():
    return None

def loadAgent():
    return None

def unloadAgent():
    return None

summonAgent(input())