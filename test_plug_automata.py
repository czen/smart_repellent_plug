from plug_service import PlugAutomata
from plug_service import TimeWrapper
import unittest
import time
from unittest import mock

testTime = TimeWrapper.getTime()

def mockTime():
    global testTime
    return testTime

class SmartPlugMock:

    _instance_ = None

    @classmethod
    def getInstance(cls):
        return cls._instance_

    def __init__(self):
        self.isItOn = False
        SmartPlugMock._instance_ = self

    def on(self):
        self.isItOn = True

    def off(self):
        self.isItOn = False

    def status(self):
        return True

    def isAlive(self):
        return True

    def isOn(self):
        return self.isItOn

class TestAutomata(unittest.TestCase):

    @mock.patch('time.time', mock.MagicMock(side_effect=mockTime))
    def testOnOff(self):
        global testTime
        hour = 60*60
        minute = 60
        a = PlugAutomata(SmartPlugMock)
        a.start()
        a.wakeUp()
        theirPlug = SmartPlugMock.getInstance()
        self.assertEqual(a.totalTime, 0)
        testTime = testTime + hour
        a.wakeUp()
        self.assertEqual(a.totalTime, hour)
        testTime = testTime + hour
        a.wakeUp()
        self.assertEqual(a.totalTime, 2*hour)
        self.assertEqual(theirPlug.isItOn, False)
        testTime = testTime + hour
        a.wakeUp()
        self.assertEqual(a.totalTime, 2*hour)
        self.assertEqual(theirPlug.isItOn, False)
        testTime = testTime + 2*hour + minute
        a.wakeUp()
        self.assertEqual(a.totalTime, 2*hour)
        self.assertEqual(theirPlug.isItOn, True)
        testTime = testTime + minute
        a.wakeUp()
        self.assertEqual(a.totalTime, 2 * hour + minute)
        self.assertEqual(theirPlug.isItOn, False)
        testTime = testTime + hour
        a.wakeUp()
        self.assertEqual(theirPlug.isItOn, False)
        testTime = testTime + hour
        a.wakeUp()
        self.assertEqual(theirPlug.isItOn, False)


if __name__ == '__main__':
    unittest.main()