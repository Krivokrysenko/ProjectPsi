import agents.agent
import asyncio

class Timer(agents.agent.Agent):
    def getKeywords(self):
        return ["timer"]

    async def interpret(self, tokens):
        await self.timer(tokens)

    async def timer(self, tokens):
        amount = None
        for token in tokens:
            if token.isdigit():
                amount = int(token)
        if amount is None:
            await self.requestMoreInfo("How long do you want to set a timer for?")
        else:
            print("timer set for " + str(amount))
            await asyncio.sleep(amount)
            print("timer for " + str(amount) + ":")
            await self.outputToNona("beep beep beep")