import pyttsx3
import speech_recognition as sr
import eel

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 175)
    print(voices)
    engine.say(text)
    engine.runAndWait()

@eel.expose
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
        speak(query)
        eel.ShowHood()
    except Exception as e:
        return ""

    return query.lower()


# def takecommand():
#     r = sr.Recognizer()

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
