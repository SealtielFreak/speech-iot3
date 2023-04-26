import pyttsx3

import iot3.config

console = iot3.config.console


class Speech:
    def __init__(self, driver_name=None):
        if driver_name is None:
            self.__engine = pyttsx3.init()
        else:
            self.__engine = pyttsx3.init("sapi5")

        voices = self.__engine.getProperty('voices')

        for voice in voices:
            if voice.name == iot3.config.DEFAULT_SPEAK_LANGUAGE:
                self.__engine.setProperty('voice', voice.id)

        console.log(f"Voices selected: {self.__engine.getProperty('voice')}")


    @property
    def volumne(self):
        return self.__engine.getProperty('volumne')

    @volumne.setter
    def volumne(self, value: int):
        self.__engine.setProperty('volumen', value)

    def speak(self, txt: str):
        self.__engine.say(txt)
        self.__engine.runAndWait()
