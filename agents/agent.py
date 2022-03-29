class Agent:
    def __init__(self, Nona):
        self.Nona = Nona
        self.keywords = self.getKeywords()

    def getKeywords(self):
        return []

    async def interpret(self, tokens):
        pass

    async def requestMoreInfo(self, request):
        self.Nona.requestFromUser(request)

    async def outputToNona(self, output):
        self.Nona.outputToUser(output)