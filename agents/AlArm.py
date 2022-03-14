import agents.agent

class AlArm(agents.agent.Agent):
    def __init__(self):
        self.keywords = ["alarm"]
        super().__init__()

    async def interpret(self, tokens):
        return await self.alarm(tokens)

    async def alarm(self, tokens):
        time = 0
        unit = ""
        for token in tokens:
            if token.isdigit():
                time = token
                # this is an index out of bounds error in the making
                unit = tokens[tokens.index(token) + 1]
        print("time: " + str(time) + "\n unit: " + unit)
        return await self.outputToNona("time: " + str(time) + "\n unit: " + unit)