import enum

class Code(enum.Enum):
    OUT = enum.auto
    REQ = enum.auto

class Agent:
    def __init__(self, Nona):
        self.Nona = Nona
        self.keywords = self.getKeywords()

    def getKeywords(self):
        return []

    async def interpret(self, tokens):
        pass

    async def requestMoreInfo(self, request):
        await self.Nona.addToQueue(Code.REQ, request)

    async def outputToNona(self, output):
        await self.Nona.addToQueue(Code.OUT, output)