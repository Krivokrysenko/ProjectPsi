import agents.agent
import asyncio

class Timer(agents.agent.Agent):
    def getKeywords(self):
        return ["timer"]

    async def interpret(self, tokens):
        await self.timer(tokens)

    async def timer(self, tokens):
        # TODO set a timer for an hour? set a timer for an hour and 30 minutes?
        conversions = {
            "seconds": 1,
            "minutes": 60,
            "hours": 60*60
        }
        amount = None
        for token in tokens:
            if token.isdigit():
                amount = int(token)
        if amount is None:
            await self.requestMoreInfo("How long do you want to set a timer for?")
        else:
            for unit in conversions:
                if unit in tokens:
                    time = amount * conversions[unit]
                    print("timer set for " + str(time))
                    await asyncio.sleep(time)
                    await self.outputToNona("timer for " + str(time) + ": beep beep beep")