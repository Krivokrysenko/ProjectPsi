from enum import Enum, auto
import ray

# TODO get rid of these enums?
class Code(Enum):
    INFO = auto()
    OUT = auto()

# TODO finish fleshing this out and change Timer/AlArm to extend this properly/use the API

class Agent:
    def __init__(self):
        super().__init__()

    def keywords(self):
        return None

    def interpret(self, tokens):
        return None

    def requestMoreInfo(self, request):
        return Code.INFO, request

    def outputToNona(self, output):
        return Code.OUT, output
