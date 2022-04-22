# https://github.com/alphacep/vosk-api

from codes import Codes

class Voice:
    def __init__(self, Nona):
        self.Nona = Nona
        self.name = Nona.name

    def NonaHear(self, text):
        self.Nona.addToQueue(Codes.INP, text)

