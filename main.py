import datetime
import math
import pathlib
import time

import numpy
import sounddevice
import soundfile
import matplotlib.pyplot as plt
from numpy.random.mtrand import exponential


class Daughter:
    """

    """

    def __init__(self):
        """
        Daughter's constructor.
        """
        self._pos = -1
        self._buffer: numpy.ndarray

    def get_first(self, samplerate: int, frames: int) -> numpy.ndarray:
        """
        return the first frames from the buffer, and start daughter's 'play' status.

        :param samplerate:
        :param frames:
        :return:
        """
        # Si on dépasse la fin → compléter avec silence
        if frames > len(self._buffer):
            chunk = self._buffer[0:]
            pad = numpy.zeros(frames - len(self._buffer), dtype=numpy.float32)
            self._pos = None
            return numpy.concatenate((chunk, pad))

        # Sinon → lecture normale
        self._pos = frames
        return self._buffer[0:frames]


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

        # Si on dépasse la fin → compléter avec silence
        if end > len(self._buffer):
            chunk = self._buffer[start:]
            pad = numpy.zeros(end - len(self._buffer), dtype=numpy.float32)
            self._pos = None
            return numpy.concatenate((chunk, pad))

        # Sinon → lecture normale
        self._pos = end
        return self._buffer[start:end]


class Sequencer:
    """

    """
    SR = 44100
    BLOCKSIZE = 2048

    def __init__(self, daughters=None, device=None):
        """
        Sequencer's constructor.

        :param daughters: List of daughters
        :param device: Device to use ou None for default
        """
        self._daughters = [] if daughters is None else daughters
        self._stream = sounddevice.RawOutputStream(samplerate=self.SR, blocksize=self.BLOCKSIZE, device=device, channels=1, dtype='int32', callback=self._callback)
        self._pos_samples = None

    def _callback(self, outdata, frames, time, status):
        """
        This callback will be called every 'frames' frames needed to be outed.

        :param outdata: Out data (array)
        :param frames: Number of frames do be provided
        :param time:
        :param status:
        """
        try:
            buffer = numpy.zeros(frames, dtype='float32')

            cpt = len(self._daughters)
            if cpt > 0:
                buffer /= cpt
                buffer.clip(-1.0, 1.0)
                buffer *= (2 ** 31 - 1)
                buffer=buffer.astype('int32')
                outdata[:] = buffer.tobytes()

            self._pos_samples += frames

        except Exception as e:
            print(e)
            # raise sounddevice.CallbackAbort(e)

    def run(self):
        self._pos_samples = 0
        self._stream.start()
        while True:
            time.sleep(0.5)
            print(self._pos_samples)

        self._stream.stop()






# def sine(freq, duration, sr=SR, amp=0.5):
#     t = np.arange(int(sr * duration)) / sr
#     return (amp * np.sin(2 * np.pi * freq * t)).astype('float32')

# def white_noise(duration, sr=SR, amp=0.3):
#     return (amp * np.random.uniform(-1.0, 1.0, int(sr * duration))).astype('float32')

if __name__ == '__main__':

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

    seq = Sequencer([kick, tom])
    try:
        seq.run()
    except KeyboardInterrupt:
        print("Exiting due to user interrupt...")
        exit(0)



    # s = sine(220, 1, sr=SR, amp=1)

    # with soundfile.SoundFile(pathlib.Path('[99Sounds] 99 Drum Samples/[99Sounds] 99 Drum Samples/Samples/kick-deep.wav')) as f:
    #     audio = f.read()
    #
    #
    #
    #     sounddevice.play(audio)
    #     time.sleep(0.1)
    #     sounddevice.play(audio, blocking=True)
    #     time.sleep(0.1)
    #     sounddevice.play(audio, blocking=True)
    #     sounddevice.play(audio, blocking=True)
    #
    #     duration = len(audio) / SR
    #     time = np.linspace(0, duration, int(SR * duration), endpoint=False)
    #     plt.plot(time, audio)
    #     plt.title("Double frappe de batterie synthétique")
    #     plt.xlabel("Temps (s)")
    #     plt.xlim(0, 1)  # définit l'échelle verticale de -50 à +50
    #     plt.ylabel("Amplitude")
    #     plt.ylim(-1.1, 1.1)  # définit l'échelle verticale de -50 à +50
    #     plt.show()