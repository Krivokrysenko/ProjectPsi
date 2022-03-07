import agents.agent
import ray

keywords = ["alarm"]

@ray.remote
class AlArm(agents.agent.Agent):
    def __init__(self):
        super().__init__()


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