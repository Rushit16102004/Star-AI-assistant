import os
import re
import sqlite3
import struct
import subprocess
import webbrowser
from datetime import time
from pipes import quote

import pyautogui
import speech_recognition as sr
import pvporcupine
import pyaudio
import pywhatkit as kit
import pygame
import eel

from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term, remove_words

con = sqlite3.connect("star.db")
cursor = con.cursor()

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

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                os.startfile(results[0][0])

            elif len(results) == 0:
                cursor.execute(
                    'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening " + query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening " + query)
                    try:
                        os.system('start ' + query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
    
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["star","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)


# find contacts
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",
                    ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])

        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0


def whatsApp(mobile_no, message, flag, name):
    if flag == 'message':
        target_tab = 12
        star_message = "message sent successfully to " + name

    elif flag == 'call':
        target_tab = 10
        message = ''  # No message for calls
        star_message = "calling " + name
        # Construct the URL for voice call
        whatsapp_url = f"whatsapp://call?phone={mobile_no}"

    elif flag == 'video call':
        target_tab = 9
        message = ''  # No message for video calls
        star_message = "starting video call with " + name
        # Construct the URL for video call
        whatsapp_url = f"whatsapp://call?phone={mobile_no}"

    else:
        # Handle unsupported flag
        speak("Unsupported action")
        return

    # Encode the message for URL (only for messages)
    encoded_message = quote(message) if flag == 'message' else ''

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)

    pyautogui.hotkey('win', '2')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(star_message)