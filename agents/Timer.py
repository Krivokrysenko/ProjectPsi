import agents.agent
import time
from thespian.actors import *

keywords = ["timer"]

# TODO do not use sleep or time or whatever just send a delayed message to yourself or nona for the love of goosh
class Timer(agents.agent.Agent):
    def __init__(self):
        super().__init__() # pycharm is happy with this here but i forgor what it does

    # non-actor stuff

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
            return self.outputToNona("beep beep beep")

    # actor stuff

    def receiveMessage(self, msg, sender):
        idkwhattodowiththis = self.interpret(msg)
        print("congrats ya did it")