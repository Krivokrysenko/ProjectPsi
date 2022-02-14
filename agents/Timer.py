import agents.agent
import time
from thespian.actors import *

keywords = ["timer"]

class Timer(agents.agent.Agent):

    def keywords(self):
        return ["timer"]

    def interpret(self, tokens):
        return self.timer(tokens)

    def timer(self, tokens):
        amount = None
        for token in tokens:
            if token.isdigit():
                amount = int(token)
        if amount is None:
            return self.requestMoreInfo("How long do you want to set a timer for?")
        else:
            time.sleep(amount)
            return self.outputToNona("timer set for whatever the heck it was before")

class TimerActor(agents.agent.AgentActor):
    def __init__(self):
        super().__init__() # pycharm is happy with this here but i forgor what it does
        self.TimerObj = Timer()

    def receiveMessage(self, msg, sender):
        idkwhattodowiththis = self.TimerObj.interpret(msg)
        print("beep beep beep")