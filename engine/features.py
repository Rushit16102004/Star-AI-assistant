import os
import re

import pywhatkit as kit
import pygame
import eel

from engine.command import speak
from engine.config import ASSISTANT_NAME


# Initialize pygame mixer module
pygame.mixer.init()

# Playing assistant sound function
@eel.expose
def playAssistantSound():
    music_dir = "www/assets/start_sound.mp3"
    pygame.mixer.music.load(music_dir)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    if query!="":
        speak("opening "+query)
        os.system('start '+query)
    else:
        speak("not found")


def find_app_in_database(app_name):
    import sqlite3

    conn = sqlite3.connect('star.db')
    cursor = conn.cursor()

    cursor.execute("SELECT path FROM applications WHERE name=?", (app_name,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None


def extract_app_name(query):
    pattern = r'(?:open|start)\s+(.+)'
    match = re.search(pattern, query, re.IGNORECASE)
    return match.group(1).strip() if match else None


def startCommandApp(query):
    app_name = extract_app_name(query)

    if app_name:
        app_path = find_app_in_database(app_name)
        if app_path:
            speak("opening " + app_name)
            os.system('start ' + app_path)
        else:
            speak("application not found in database")
    else:
        speak("not found")




def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

def extract_yt_term(command):
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None
