import sys
import json
import threading
import os

voice: dict = {
    "en-us": "joe",
    "pt-pt": "tugão"
    }


def say(text, lang):
    process = f"echo \"{text}\" | ./features/audio_processing/piper/piper --model ./features/audio_processing/piper/voices/{voice[lang]}/{voice[lang]}-medium.onnx -f speach.mp3"
    playit = "aplay speach.mp3"
    os.system(f'{process}')
    os.system(f'{playit}')


class Audio:
    def __init__(self, lang) -> None:
        self.lang = lang

    def stt(self):
        return "Under contruction."
                    

    def tts(self, text):
        try:
            speach = threading.Thread(target=say, args=(text, self.lang))
            speach.start()
            return 1
        except:
            return 0
