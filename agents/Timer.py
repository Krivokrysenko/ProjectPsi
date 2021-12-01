import agents.agent

keywords = ["timer"]

class Timer(agents.agent.Agent):

    def keywords(self):
        return ["timer"]

    def interpret(self, tokens):
        return self.timer(tokens)

    def timer(self, tokens):
        time = 0
        unit = ""
        for token in tokens:
            if token.isdigit():
                time = token
                # this is an index out of bounds error in the making
                unit = tokens[tokens.index(token) + 1]
        return self.outputToNona("time: " + str(time) + "\n unit: " + unit)