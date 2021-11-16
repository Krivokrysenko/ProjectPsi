from enum import Enum, auto

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