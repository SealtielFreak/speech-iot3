import random
from typing import List

from speech_recognition import Recognizer, Microphone

import iot3.config
from iot3.speech import Speech

console = iot3.config.console


class Listener:
    def __init__(self, speech: Speech, err_msg: List[str], default_engine: str = iot3.config.DEFAULT_SPEECH_ENGINE):
        self.__last_command = ""
        self.__speech = speech
        self.__err_msg = err_msg
        self.__recognizer = Recognizer()

        self.__default_recognizer_engine = default_engine
        self.__default_list_recognizer_engine = {
            "google": self.__recognizer.recognize_google,
            "whisper": self.__recognizer.recognize_whisper,
            "sphinx": self.__recognizer.recognize_sphinx
        }

    @property
    def recognizer_engine(self):
        return self.__default_list_recognizer_engine[self.__default_recognizer_engine]

    @property
    def last_command(self):
        return self.__last_command

    def take_command(self, required=True) -> str:
        query = ""

        with Microphone() as source:
            console.log("Listening command...")

            self.__recognizer.pause_threshold = 1
            self.__recognizer.adjust_for_ambient_noise(source)
            audio = self.__recognizer.listen(source)

        try:
            console.log("Recognizing voice...")
            query = self.recognizer_engine(audio, language=iot3.config.DEFAULT_LANGUAGE, show_all=False)
            console.log(f"User said: {query}\n")
        except Exception as e:
            if required:
                console.log("Unable to Recognize your voice.", e)
                self.__speech.speak(random.sample(self.__err_msg, 1)[-1])

        self.__last_command = query.lower()

        return self.last_command
