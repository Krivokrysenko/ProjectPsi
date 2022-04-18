from codes import Codes

class Agent:
    def __init__(self, Nona):
        self.Nona = Nona
        self.keywords = self.getKeywords()

    def getKeywords(self):
        return []

    async def interpret(self, tokens):
        pass

    async def requestMoreInfo(self, request):
        await self.Nona.addToQueue(Codes.REQ, request)

    async def outputToNona(self, output):
        await self.Nona.addToQueue(Codes.OUT, output)