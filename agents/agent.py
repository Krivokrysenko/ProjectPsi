from enum import Enum, auto
from thespian.actors import *


# TODO get rid of these enums cause you can replace them with thespian ask/tell
class Code(Enum):
    INFO = auto()
    OUT = auto()


# TODO finish fleshing this out and change Timer/AlArm to extend this properly/use the API
class Agent(Actor):
    def __init__(self):
        super().__init__()

    # non-actor stuff

    def keywords(self):
        return None

    def interpret(self, tokens):
        return None

    def requestMoreInfo(self, request):
        return Code.INFO, request

    def outputToNona(self, output):
        return Code.OUT, output

    # actor stuff

    def receiveMessage(self, msg, sender):
        self.interpret(msg)
