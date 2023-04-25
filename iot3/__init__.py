import datetime
import random
import time
from typing import Text, Union

from rich import pretty
from serial import Serial

import iot3.config
from iot3.commands import ScriptCommandManager, ScriptCommand
from iot3.listener import Listener
from iot3.speech import Speech

speech = Speech()
listener = Listener(speech, ['Disculpa pero no te entiendo', '¿Me puedes repetir?'])

random_sample = lambda l: random.sample(l, 1)[0]
random_speak = lambda l: speech.speak(random_sample(l))


def send_to_arduino(command: Text):
    try:
        arduino = Serial("COM3", 9600)

        time.sleep(2)

        arduino.write(command.encode())
        arduino.close()
    except:
        return False

    return True


def wish_me():
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour < 12:
        speech.speak("Buenos dias!")
    elif 12 <= hour < 18:
        speech.speak("Buenas tardes!")
    else:
        speech.speak("Buenas noches !")


def user_welcome():
    speech.speak("¿Cual es tu nombre?")
    uname = ""

    while uname == "":
        listener.take_command()
        uname = listener.last_command

        if uname == "":
            speech.speak("No entendi tu nombre, ¡Intentemos una vez mas!")

    speech.speak("¡Bienvenido!")
    speech.speak(uname)
    speech.speak("¿Que puedo hacer por ti hoy?")


if __name__ == '__main__':

    pretty.install()

    manager = ScriptCommandManager()


    @manager.bind("Close", ("adios", "acabamos"))
    class CloseCommand(ScriptCommand):
        def run(self):
            raise SystemExit


    @manager.bind("Time", ("hora", "tiempo"))
    class TimeCommand(ScriptCommand):
        def run(self):
            speech.speak("Consultando tiempo...")


    @manager.bind("CommandClose", ("cerrar", "finalizar", "terminar", "apagar"))
    class VoiceCommandClose(ScriptCommand):
        def run(self):
            speech.speak("Apagando LED del dispositivo")

            if not send_to_arduino("0"):
                speech.speak("Lo lamento, pero parece que el dispositivo no se encuentra conectado")


    @manager.bind("CommandOpen", ("abrir", "iniciar", "ejecutar", 'encender'))
    class VoiceCommandOpen(ScriptCommand):
        def run(self):
            speech.speak("Encendiendo LED del dispositivo")

            if not send_to_arduino("1"):
                speech.speak("Lo lamento, pero parece que el dispositivo no se encuentra conectado")


    def main_loop():
        wish_me()

        if not iot3.config.DEBUG_MODE:
            user_welcome()

        running = True

        while running:
            try:
                listener.take_command(False)
                query = listener.last_command

                if query != "":
                    try:
                        voice_command = manager.search(query)
                        if voice_command is not None:
                            voice_command.run()
                        else:

                            random_speak(
                                ("¿Algo mas?", "¿Necesitas algo mas?", "¿Que otra cosa puedo hacer por ti?")
                            )
                    except KeyboardInterrupt:
                        random_speak(
                            ("No te entiendo, pinche vato estupido", "Habla mas claro, por favor", "No te entiendo")
                        )

            except Union[KeyboardInterrupt, SystemExit]:
                running = False

        random_speak(("¡Hasta la proximaaa!", "Adios", "Fue un gusto trabajar contigo"))


    try:
        main_loop()
    except KeyboardInterrupt:

        random_speak(
            ("¡Hasta pronto!", "¡Adios!")
        )
