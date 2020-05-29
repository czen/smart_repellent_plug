import time
from plug_service import PlugAutomata
from plug_wrapper import SmartPlug
from config import settings

if __name__ == "__main__":
    automata = PlugAutomata(SmartPlug)
    automata.start()

    while True:
        if automata is not None:
           automata.wakeUp()
        time.sleep(settings["checkInterval"])

    self.automata = None
