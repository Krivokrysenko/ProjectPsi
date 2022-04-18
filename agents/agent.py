import enum

class Code(enum.Enum):
    OUT = enum.auto
    REQ = enum.auto
    # TODO IN code that marks inputs

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