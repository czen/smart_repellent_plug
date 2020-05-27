'''
To make this work with Python3.8 and pywin32 v.227
copy C:\Python3\Lib\site-packages\pywin32_system32\pywintypes38.dll
to   C:\Python3\Lib\site-packages\win32\pywintypes38.dll
because windows will run pythonservice.exe from site-packages\win32 and dll needs to be there

paths may change depending on where python is installed

'''

import time
import random
from service import SMWinservice
from plug_wrapper import SmartPlug
from config import settings

class PlugAutomata:
    def __init__(self, plugClass):
        self.lastStartTime = 0
        self.lastCheckTime = 0
        self.totalTime = 0
        self.currentActiveTime = 0
        self.currentOffTime = 0
        self.state = "waiting"  # waiting, on, off
        self.plugClass = plugClass
        self.plug = None

    def start(self):
        self.gotoWaiting()

    def checkStatus(self):
        if self.plug is None:
            return False
        return self.plug.isAlive()

    def gotoWaiting(self):
        self.lastStartTime = 0
        self.lastCheckTime = 0
        self.totalTime = 0
        self.currentActiveTime = 0
        self.currentOffTime = 0
        self.state = "waiting"
        self.plug = None

    def startOver(self):
        self.lastStartTime = time.time()
        self.totalTime = 0
        self.lastCheckTime = time.time()
        self.currentActiveTime = 0
        self.currentOffTime = 0
        self.state = "on"
        self.plug = self.plugClass()

    def updateSpentTime(self):
        currentTime = time.time()
        if self.state == "on":
            self.totalTime = self.totalTime + currentTime - self.lastCheckTime
            self.currentActiveTime = self.currentActiveTime + currentTime - self.lastCheckTime
        elif self.state == "off":
            self.currentOffTime = self.currentOffTime + currentTime - self.lastCheckTime
        self.lastCheckTime = currentTime

    def checkTime(self):
        currentTime = time.time()
        diff = currentTime - self.lastCheckTime
        self.lastCheckTime = currentTime
        return diff

    def goOff(self):
        self.currentActiveTime = 0
        self.currentOffTime = 0
        self.state = "off"

    def goOn(self):
        self.currentActiveTime = 0
        self.currentOffTime = 0
        self.state = "on"

    def wakeUp(self):
        if self.state == "waiting":
            if not self.checkStatus():
                self.state = "waiting"
            else:
                self.startOver()
        elif self.state == "on":
            if not self.checkStatus():
                self.gotoWaiting()
            if self.plug.isOn():
                self.updateSpentTime()
                if self.currentActiveTime > settings["activePeriod"]:
                    self.goOff()
                else:
                    pass
            else:
                self.gotoWaiting()
        elif self.state == "off":
            if not self.checkStatus():
                self.gotoWaiting()
            if self.plug.isOn():
                self.startOver()
            else:
                self.updateSpentTime()
                if self.currentOffTime > settings["passivePeriod"]:
                    self.goOn()
                else:
                    pass

class PlugService(SMWinservice):

    _svc_name_ = 'plugService'
    _svc_display_name_ = 'python service to turn xiaomi smart plug by schedule'
    _svc_description_ = 'schedules xiaomi smart plug on/off after it appears online'

    def start(self):
        self.automata = PlugAutomata(SmartPlug)
        self.isrunning = True
        self.automata.start()

    def stop(self):
        self.isrunning = False
        self.automata = None

    def main(self):
        while self.isrunning:
            if self.automata is not None:
                self.automata.wakeUp()
            time.sleep(settings["checkInterval"])

if __name__ == '__main__':
    PlugService.parse_command_line()