import os
import shutil
import subprocess

class OfflineTTS:
    def __init__(self, piper_model="models/en_US-lessac-medium.onnx"):
        self.piper_model = piper_model
        self.piper_bin = shutil.which("piper")
        self.fallback = None
        if not (self.piper_bin and os.path.exists(self.piper_model)):
            import pyttsx3
            self.fallback = pyttsx3.init()
            self.fallback.setProperty("rate", 160)

    def speak(self, text: str):
        print(f'\n🎧 [Whisper]: "{text}"\n')
        if self.piper_bin and os.path.exists(self.piper_model):
            player = "afplay" if shutil.which("afplay") else "aplay -r 22050 -f S16_LE -t raw"
            cmd = f'echo "{text}" | {self.piper_bin} --model {self.piper_model} --output-raw | {player}'
            subprocess.run(cmd, shell=True, stderr=subprocess.DEV_NULL)
        elif self.fallback:
            self.fallback.say(text)
            self.fallback.runAndWait()
