from plug_service import PlugAutomata
import unittest
import time
from unittest import mock

testTime = time.time()

def mockTime():
    global testTime
    return testTime

class SmartPlugMock:
    def __init__(self):
        self.isOn = False

    def on(self):
        self.isOn = True

    def off(self):
        self.isOn = False

    def status(self):
        return True

    def isAlive(self):
        return True

    def isOn(self):
        return self.isOn

class TestAutomata(unittest.TestCase):

    @mock.patch('time.time', mock.MagicMock(side_effect=mockTime))
    def testOnOff(self):
        global testTime
        a = PlugAutomata(SmartPlugMock)
        a.start()
        self.assertEqual(a.totalTime, 0)
        testTime = testTime + 60
        a.wakeUp()
        self.assertEqual(a.totalTime, 60)
        testTime = testTime + 60*60
        a.wakeUp()
        testTime = testTime + 60 * 60
        a.wakeUp()

if __name__ == '__main__':
    unittest.main()