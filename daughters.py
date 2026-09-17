#
# daughter.py
#

import pathlib
from typing import Dict, Any

import numpy
import soundfile


class Daughter:
    """

    """

    def __init__(self):
        """
        Daughter's constructor.
        """
        self._pos = None
        self._buffer: numpy.ndarray
        self._gain: float = 0

    def get_first(self, samplerate: int, frames: int, **params) -> numpy.ndarray:
        """
        return the first frames from the buffer, and start daughter's 'play' status.

        :param samplerate:  Sampling rate of the buffer.
        :param frames:  Number of frames to return.
        :param params:  Any parameters to configure the next sound.
        :return:
        """
        # print(params)
        self._gain = params.get('gain', 100) / 100.0

        chunk = self._buffer[:frames] * self._gain
        # Si on dépasse la fin → compléter avec silence
        if frames > len(self._buffer):
            pad = numpy.zeros(frames - len(self._buffer), dtype=numpy.float32)
            self._pos = None
            return numpy.concatenate((chunk, pad))
        # Sinon → lecture normale
        else:
            self._pos = frames
            return chunk


    def get_next(self, samplerate: int, frames: int) -> numpy.ndarray|None:
        """
        return next frames from the buffer. Must be called until 'None' indicating end of buffer.

        :param samplerate:
        :param frames:
        :return:
        """

        # Si on dépasse la fin du sample → silence
        if self._pos is None:
            return None

        start = self._pos
        end = start + frames

        chunk = self._buffer[start:end] * self._gain
        # Si on dépasse la fin → compléter avec silence
        if end > len(self._buffer):
            pad = numpy.zeros(end - len(self._buffer), dtype=numpy.float32)
            self._pos = None
            return numpy.concatenate((chunk, pad))
        # Sinon → lecture normale
        else:
            self._pos = end
            return chunk

    # def make_params(self, **params) -> Dict[str, Any]:
    #     """
    #     Fabrique un dict de paramètres pour un événement.
    #     Les paramètres peuvent être spécialisés selon le type d'instrument.
    #     Ex: gain, pitch, etc.
    #     """
    #     return params

    def __call__(self, **kwargs):
        """
        Si l'instance de Daughter est passée avec des paramètres, alors on retourne l'instance et ces paramètres.
        :param kwargs: Liste des paramètres.
        :return: Un tuple de l'instance et de ses paramètres.
        """
        return self, kwargs

kick = Daughter()
with soundfile.SoundFile(
    pathlib.Path('[99Sounds] 99 Drum Samples/[99Sounds] 99 Drum Samples/Samples/kick-big.wav')
) as f:
    kick._buffer = f.read()

tom = Daughter()
with soundfile.SoundFile(
    pathlib.Path('[99Sounds] 99 Drum Samples/[99Sounds] 99 Drum Samples/Samples/tom-acoustic02.wav')
) as f:
    tom._buffer = f.read()

hi_hat = Daughter()
with soundfile.SoundFile(
    pathlib.Path('[99Sounds] 99 Drum Samples/[99Sounds] 99 Drum Samples/Samples/hihat-acoustic01.wav')
) as f:
    hi_hat._buffer = f.read()

# def sine(freq, duration, sr=SR, amp=0.5):
#     t = np.arange(int(sr * duration)) / sr
#     return (amp * np.sin(2 * np.pi * freq * t)).astype('float32')

# def white_noise(duration, sr=SR, amp=0.3):
#     return (amp * np.random.uniform(-1.0, 1.0, int(sr * duration))).astype('float32')
