from config import settings

from config import settings
from ip_sniffer import get_ip
from miio import ChuangmiPlug

class SmartPlug:
    def __init__(self):
        self.ip = get_ip(settings["mac"])
        self.plug = ChuangmiPlug(self.ip, settings["token"])

    def on(self):
        self.plug.on()

    def off(self):
        self.plug.off()
