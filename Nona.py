from agents.AlArm import AlArm

agentKeywords = []

def acceptInput(userstring):
    tokens = userstring.split(" ")
    summonAgent(tokens)

def summonAgent(tokens):
    if "alarm" in tokens:
        alarm = AlArm()
        signal = alarm.interpret(tokens)
        # some sort of control flow to call requestFromUser versus outputToUser based on the signal

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