from enum import Enum, auto

# TODO get rid of these enums?
class Code(Enum):
    INFO = auto()
    OUT = auto()

# TODO finish fleshing this out and change Timer/AlArm to extend this properly/use the API

class Agent:
    def __init__(self, Nona):
        self.Nona = Nona
        self.keywords = self.getKeywords()

    def getKeywords(self):
        return []

    async def interpret(self, tokens):
        return None

    async def requestMoreInfo(self, request):
        return Code.INFO, request

    async def outputToNona(self, output):
        return Code.OUT, output