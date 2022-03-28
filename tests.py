import unittest
import Nona
import asyncio
# https://promity.com/2020/06/03/testing-asynchronous-code-in-python/
import pytest

@pytest.mark.asyncio
async def test_keywords():
    NonaObj = Nona.Nona()
    await NonaObj.loadAgent("alarm", ".AlArm")
    assert NonaObj.agentkeywords["alarm"][0] == "alarm"
    assert NonaObj.agentkeywords["alarm"][1] == "set an alarm"
    assert NonaObj.agentkeywords["alarm"][2] == "remind me at"
    await NonaObj.unloadAgent("alarm")
    assert NonaObj.loadedmodules == {}
    assert NonaObj.instantiatedclasses == {}
    assert NonaObj.agentkeywords == {}

@pytest.mark.asyncio
async def test_addKeyword():
    NonaObj = Nona.Nona()
    await NonaObj.loadAgent("alarm", ".AlArm")
    previous = NonaObj.agentkeywords["alarm"]
    await NonaObj.addKeyword("alarm", "al arm")
    actual = NonaObj.agentkeywords["alarm"]
    expected = previous + ["al arm"]
    assert actual == expected
    await NonaObj.unloadAgent("alarm")

@pytest.mark.asyncio
async def test_addKeyword2():
    NonaObj = Nona.Nona()
    await NonaObj.loadAgent("timer", ".Timer")
    await NonaObj.addKeyword("timer", "set a timer")
    await NonaObj.unloadAgent("timer")

@pytest.mark.asyncio
async def test_requestFromUser():
    NonaObj = Nona.Nona()
    await NonaObj.loadAgent("timer", ".Timer")
    await NonaObj.acceptInput("timer 4")
    await NonaObj.acceptInput("timer 2")
    await asyncio.sleep(7)
    await NonaObj.unloadAgent("timer")

@pytest.mark.asyncio
async def test_loadfortesting():
    NonaObj = Nona.Nona()
    await NonaObj.loadAgent("alarm", ".AlArm")
    await NonaObj.loadAgent("timer", ".Timer")

@pytest.mark.asyncio
async def test_unloadfortesting():
    NonaObj = Nona.Nona()
    await NonaObj.unloadAgent("alarm")
    await NonaObj.unloadAgent("timer")

def test_resetcongiffortesting():
    conf = open("config.ini", "w")
    conf.write('[agents]\n\n[keywords]\nnonacancel = ["nevermind", "never", "mind", "cancel"]\nalarm = ["set an alarm", "remind me at"]\n')
    conf.close()