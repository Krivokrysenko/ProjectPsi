import agents.agent
import asyncio

# TODO make this work

class AlArm(agents.agent.Agent):
    def getKeywords(self):
        return ["alarm"]

    async def interpret(self, tokens):
        await self.alarm(tokens)

    async def alarm(self, tokens):
        time = 0
        unit = ""
        for token in tokens:
            if token.isdigit():
                time = token
                # this is an index out of bounds error in the making
                unit = tokens[tokens.index(token) + 1]
        print("time: " + str(time) + "\n unit: " + unit)
        await self.outputToNona("time: " + str(time) + "\n unit: " + unit)