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
        amount = 0
        for token in tokens:
            if token.isdigit():
                amount = int(token)
        time.sleep(amount)
        return self.outputToNona("beep beep beep")