import contextlib
import pyaudio


@contextlib.contextmanager
def open_pyaudio():
    _p = pyaudio.PyAudio()

    yield _p

    _p.terminate()


@contextlib.contextmanager
def open_stream(p, **kwargs):
    stream = p.open(**kwargs)

    yield stream

    stream.stop_stream()
    stream.close()


def find_working_microphone():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    with open_pyaudio() as p:
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)

            if device_info['maxInputChannels'] > 0:
                try:
                    with open_stream(p, input_device_index=i, format=FORMAT, channels=CHANNELS, rate=RATE, input=True):
                        pass

                    return i
                except OSError:
                    continue

    return None


class MicrophoneNoFound(Exception):
    ...
