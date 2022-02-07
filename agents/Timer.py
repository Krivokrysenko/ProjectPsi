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
            timeractor = ActorSystem().createActor(TimerActor)
            return self.outputToNona(ActorSystem().ask(timeractor, amount))

class TimerActor(Actor):
    def receiveMessage(self, msg, sender):
        time.sleep(msg)
        print("beep beep beep")