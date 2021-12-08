import agents.agent
from concurrent.futures import *
import time

keywords = ["timer"]

executor = ThreadPoolExecutor()

class Timer(agents.agent.Agent):

    def keywords(self):
        return ["timer"]

    def interpret(self, tokens):
        return executor.submit(self.timer, tokens).result()

    def timer(self, tokens):
        amount = None
        for token in tokens:
            if token.isdigit():
                amount = int(token)
        if amount is None:
            return self.requestMoreInfo("How long do you want to set a timer for?")
        else:
            print("timer set for " + str(amount) + " seconds")
            time.sleep(amount)
            return self.outputToNona("beep beep beep")