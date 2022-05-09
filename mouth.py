import pyttsx3

class Mouth:

    async def NonaSay(self, output):
        engine = pyttsx3.init()
        engine.say(output)
        engine.runAndWait()