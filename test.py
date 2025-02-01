import struct
from datetime import time
import speech_recognition as sr  # New library for speech recognition
import pyaudio

porcupine = None
paud = None
audio_stream = None
recognizer = sr.Recognizer()  # Initialize the recognizer

try:
    paud = pyaudio.PyAudio()
    audio_stream = paud.open(rate=16000, channels=1, format=pyaudio.paInt16, input=True,
                        frames_per_buffer=1024)

    # loop for streaming
    while True or False:
        audio_data = audio_stream.read(1024)
        # Convert audio data to audio file for recognition
        source = sr.AudioData(audio_data, 16000, 2)  # Create AudioData object
        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(source)
            if "computer" in text or "alexa" in text:  # Check for keywords
                print("hotword detected")
                # pressing shortcut key win+j
                import pyautogui as autogui  # type: ignore

                autogui.keyDown("shift")
                autogui.press("s")
                time.sleep(2)
                autogui.keyUp("shift")
        except sr.UnknownValueError:
            pass  # Ignore unrecognized speech
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        finally:
            del source  # Clean up the AudioData object

except Exception as e:
    print(f"Error: {e}")  # Log the error
    if audio_stream is not None:
        audio_stream.close()
    if paud is not None:
        paud.terminate()
