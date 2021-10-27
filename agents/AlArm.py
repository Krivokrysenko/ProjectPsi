import agents.agent

keywords = ["alarm"]

class AlArm(agents.agent.Agent):

    # then the functions like
    def alarm(self, tokens):
        time = 0
        unit = ""
        for token in tokens:
            if token.isdigit():
                time = token
                # this is an index out of bounds error in the making
                unit = tokens[tokens.index(token) + 1]
        print(time)
        print(unit)