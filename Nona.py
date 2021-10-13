# should probably make an init and all and stuff but just manual import for now
from agents import AlArm

# fun stuff to make agents go brrrrrrrrr

# i was gonna put like, data structures here or something

# Nona's jazz

def summonAgent(userstring):
    tokens = userstring.split(" ")
    if "alarm" in tokens:
        AlArm.alarm(tokens)

summonAgent(input())