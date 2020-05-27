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

class PlugService(SMWinservice):

    _svc_name_ = 'plugService'
    _svc_display_name_ = 'python service to turn xiaomi smart plug by schedule'
    _svc_description_ = 'schedules xiaomi smart plug on/off after it appears online'

    hour = 60*60 # 1 hour in seconds
    activePeriod = hour
    maxOverallTime = 2*hour
    checkInterval = 60 # check every minute

    def start(self):
        self.isrunning = True
        self.lastStartTime = 0
        self.totalTime = 0
        self.currentActiveTime = 0
        self.state = "waiting" # waiting, on, off
        self.plug = None

    def stop(self):
        self.isrunning = False

    def main(self):
        i = 0
        while self.isrunning:



if __name__ == '__main__':
    PlugService.parse_command_line()