import agents.agent

keywords = ["alarm"]

class AlArm(agents.agent.Agent):
    def __init__(self):
        super().__init__()

    # non-actor stuff

    def keywords(self):
        return ["alarm"]

    def interpret(self, tokens):
        return self.alarm(tokens)

    def alarm(self, tokens):
        time = 0
        unit = ""
        for token in tokens:
            if token.isdigit():
                time = token
                # this is an index out of bounds error in the making
                unit = tokens[tokens.index(token) + 1]
        return self.outputToNona("time: " + str(time) + "\n unit: " + unit)

    # actor stuff

    def receiveMessage(self, msg, sender):
        idkwhattodowiththis = self.interpret(msg)
        print("beep beep beep")