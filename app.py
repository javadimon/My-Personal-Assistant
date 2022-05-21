import os
import queue
import sounddevice as sd
import vosk
import sys
import json
import time
import speaker
from modules import weather

model = vosk.Model(
    "C:\\PythonProjects\\My-Personal-Assitant\\vosk-model-small-ru-0.22")


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def listen():
    try:
        global q
        q = queue.Queue()
        with sd.RawInputStream(samplerate=44100, blocksize=8000, device=None, dtype='int16', channels=1,
                               callback=callback):
            print('#' * 10, 'Switching to listen mode. Press Ctrl+C to exit', '#' * 10)

            recognizer = vosk.KaldiRecognizer(model, 44100)
            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    json_result = recognizer.Result()
                    text = json.loads(json_result)["text"]
                    if text:
                        print(text)
                        return text

    except Exception as e:
        print(e)
        exit("Fatal error" + ": " + str(e))


is_working_mode = False

if __name__ == '__main__':

    while True:

        text = listen()

        if "очнись" in text:
            is_working_mode = True
            speaker.speak("Слушаю")
            continue

        if "отбой" in text:
            is_working_mode = False
            speaker.speak("Отключаюсь")
            continue

        if is_working_mode:
            if "погод" in text:
                weather.get_weather_info()

# Типа скачай мне 5 фильмов ужасов с 2010 по 2022 с призами на фестивалях, но не самые популярные,
# желательно дебюты с возрастным рейтингом только 18+