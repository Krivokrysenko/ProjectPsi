import agents.agent
import asyncio

class Timer(agents.agent.Agent):
    def __init__(self):
        self.keywords = ["timer"]
        super().__init__()

    async def interpret(self, tokens):
        return await self.timer(tokens)

    async def timer(self, tokens):
        amount = None
        for token in tokens:
            if token.isdigit():
                amount = int(token)
        if amount is None:
            return await self.requestMoreInfo("How long do you want to set a timer for?")
        else:
            print("timer set for " + str(amount))
            await asyncio.sleep(amount)
            print("timer for " + str(amount) + ":")
            return await self.outputToNona("beep beep beep")