from enum import Enum, auto
from thespian.actors import *

class Code(Enum):
    INFO = auto()
    OUT = auto()

class Agent:

    def keywords(self):
        return None

    def interpret(self, tokens):
        return None

    def requestMoreInfo(self, request):
        return Code.INFO, request

    def outputToNona(self, output):
        return Code.OUT, output

class AgentActor(Actor):
    def __init__(self): # I have no idea if this is helpful, considering
        super().__init__()
        self.AgentObj = Agent()

    print("blah")