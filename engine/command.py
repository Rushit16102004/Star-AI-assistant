from token import STAR
from turtledemo.penrose import star
import pyttsx3
import speech_recognition as sr
import eel
import time

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 175)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()

def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening......')
        eel.DisplayMessage("listening......")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source,10,6)

    try:
        print('recognizing')
        eel.DisplayMessage("recognizing......")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
    except Exception as e:
        return ""

    return query.lower()

@eel.expose
def allCommands():

    try:
        query = takecommand()
        print(query)
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if (contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()

                elif "phone call" in query:
                    flag = 'call'

                elif "call" in query:
                    flag = 'call'

                else:
                    flag = 'video call'

                whatsApp(contact_no, query, flag, name)
        else:
            print("not run")
    except Exception as e:
        print(f"error: {e}")

    eel.ShowHood()


# def takecommand():
#     r = sr.Recognizer()Voice command.

#     with sr.Microphone() as source:
#         print('listening......')
#         r.pause_threshold = 1
#         r.adjust_for_ambient_noise(source)

#         while True:  # Loop to keep listening
#             try:
#                 print('recognizing')
#                 audio = r.listen(source, timeout=10)  # Listen for audio
#                 query = r.recognize_google(audio, language='en-in')
#                 print(f"user said: {query}")
#                 return query.lower()  # Return the recognized query
#             except sr.WaitTimeoutError:
#                 print("Listening timed out, please try again.")
#             except Exception as e:
#                 print("Error:", str(e))
#                 return ""
