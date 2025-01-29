import struct
from datetime import time

import pvporcupine
import pyaudio

porcupine = None
paud = None
audio_stream = None
try:
    # pre-trained keywords
    porcupine = pvporcupine.create(keywords=["star", "alexa"])  # Updated keyword
    paud = pyaudio.PyAudio()
    audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True,
                        frames_per_buffer=porcupine.frame_length)

    # loop for streaming
    while True:
        keyword = audio_stream.read(porcupine.frame_length)
        keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

        # processing keyword comes from mic
        keyword_index = porcupine.process(keyword)

        # checking first keyword detected
        if keyword_index >= 0:
            print("hotword detected")

        # pressing shortcut key win+j
        import pyautogui as autogui  # type: ignore

        autogui.keyDown("shift")
        autogui.press("s")
        time.sleep(2)
        autogui.keyUp("shift")

except Exception as e:
    print(f"Error: {e}")  # Log the error
    if porcupine is not None:
        porcupine.delete()
    if audio_stream is not None:
        audio_stream.close()
    if paud is not None:
        paud.terminate()
