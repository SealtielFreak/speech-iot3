import pyttsx3


class Speech:
    def __init__(self, driver_name: str = "sapi5"):
        self.__engine = pyttsx3.init(driver_name)

    @property
    def volumne(self):
        return self.__engine.getProperty('volumne')

    @volumne.setter
    def volumne(self, value: int):
        self.__engine.setProperty('volumen', value)

    def speak(self, txt: str):
        self.__engine.say(txt)
        self.__engine.runAndWait()
