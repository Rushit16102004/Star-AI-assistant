import os
import eel

from engine.features import *
from engine.command import *
(eel.init("www"))

playAssistantSound()

eel.start('index.html', mode='edge', block=True)