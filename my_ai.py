import speech_recognition as sr
import sounddevice as sd
import numpy as np
from gtts import gTTS
import playsound
import webbrowser
import os
import tempfile

def talk(text, lang="en"):
    print("[AI]:", text)
    tts = gTTS(text=text, lang=lang)
    tmp_file = tempfile.mktemp(suffix=".mp3")
    tts.save(tmp_file)
    playsound.playsound(tmp_file)
    os.remove(tmp_file)

def listen_command():
    recognizer = sr.Recognizer()
    duration = 4
    fs = 16000
    print("Speak...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    audio = sr.AudioData(np.array(audio_data).tobytes(), fs, 2)

    try:
        command = recognizer.recognize_google(audio, language="en-US").lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        talk("could you repeat")
        return ""
    except sr.RequestError:
        talk("Speech recognition service error")
        return ""

while True:
    cmd = listen_command()
    if not cmd:
        continue

    if "youtube" in cmd:
        talk("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "google" in cmd:
        talk("Opening Google")
        webbrowser.open("https://www.google.com")
        
    elif "my progress" in cmd:
        talk("Opening progress")
        webbrowser.open("https://cs50.me/cs50p")
        
    elif "Chat Gpt" in cmd:
        talk("Opening GPT")
        webbrowser.open("https://chatgpt.com/")
        
    elif "email" in cmd:
        talk("Opening email")
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
        
    elif ("weather") in cmd:
        talk("Opening weather")
        webbrowser.open("https://www.msn.com/en-xl/weather/forecast/in-Dzhalakuduk,Andijan-Region?loc=eyJsIjoiRHpoYWxha3VkdWsiLCJyIjoiQW5kaWphbiBSZWdpb24iLCJjIjoiVXpiZWtpc3RhbiIsImkiOiJVWiIsImciOiJlbi14bCIsIngiOiI3Mi42MzA2MTUyMzQzNzUiLCJ5IjoiNDAuNzIyMjgyNDA5NjY3OTcifQ%3D%3D&weadegreetype=C&ocid=msedgntp&cvid=68c7d176a4134f3593b94fffd1d45b2f")

    elif "stop" in cmd or "exit" in cmd or "close" in cmd:
        talk("bye calmoev!")
        break

    else:
        talk("Command not recognized")
