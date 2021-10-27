from agents.AlArm import AlArm

agentKeywords = []

def acceptInput(userstring):
    tokens = userstring.split(" ")
    summonAgent(tokens)

def summonAgent(tokens):
    if "alarm" in tokens:
        alarm = AlArm()
        alarm.interpret(tokens)

def requestFromUser(request):
    outputToUser(request)
    answer = input()
    # send back to agent?

def outputToUser(output):
    print(output)

def loadAgent():
    return None

def unloadAgent():
    return None

acceptInput(input())