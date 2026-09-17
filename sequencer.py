#
# sequencer.py
#

import heapq
import time
from heapq import heappop
from typing import Dict, Any

import numpy
import sounddevice
from matplotlib.pyplot import axis

from daughters import Daughter
from noteevent import NoteEvent


class Sequencer:
    """
    Séquenceur audio temps‑réel basé sur un callback SoundDevice.

    Ce séquenceur :
    - ouvre un flux audio en sortie (RawOutputStream)
    - appelle `_callback()` à chaque bloc de `BLOCKSIZE` frames
    - maintient un compteur d'échantillons `_pos_samples`
    - mélange les buffers des différentes `Daughter` (voies audio)
    - convertit le résultat en int32 pour la sortie audio

    Le séquenceur ne gère pas ici la logique musicale : il se contente
    d'appeler les daughters pour récupérer leurs frames et les envoyer
    au device audio.
    """

    # Sample rate fixe (44100 Hz)
    SR = 44100

    # Taille d'un bloc audio envoyé au callback
    BLOCKSIZE = 2048

    def __init__(self, daughters: list[Daughter], device=None):
        """
        Constructeur du séquenceur.

        :param daughters: Liste d'instances de Daughter.
                          Chaque Daughter représente une source audio
                          capable de fournir des frames successives.
        :param device: Nom ou index du device audio à utiliser.
                       None → device par défaut.

        Le flux audio est créé immédiatement, mais pas démarré.
        """

        # Flux audio brut (int32) avec callback
        self._stream = sounddevice.RawOutputStream(
            samplerate=self.SR,
            blocksize=self.BLOCKSIZE,
            device=device,
            channels=1,
            dtype='int32',
            callback=self._callback
        )

        self._daughters = daughters

        # Position courante en échantillons depuis le début du run()
        self._pos_samples = None

        self._events = []
        # self._event_nb = 0

    def add_note_event(self, daughter: Daughter, ts: int, params: Dict[str, Any] | None = None):

        channel = self._daughters.index(daughter)

        # Vérification : pas deux événements simultanés sur la même voie
        for ev in self._events:
            if ev.channel == channel and ev.ts == ts:
                raise ValueError(f"Deux événements simultanés sur {daughter} au timestamp {ts}")

        # Si aucun param → demander à la daughter ses paramètres par défaut.
        if params is None:
            params = daughter.make_params()

        ev = NoteEvent(
            ts=ts,
            # order=self._event_nb,   # pour éviter les doublons d'ordre
            channel=channel,
            daughter=daughter,
            params=params
        )
        # self._event_nb += 1

        heapq.heappush(self._events, ev)

    def _callback(self, outdata, frames, time, status):
        """
        Callback audio appelé par SoundDevice.

        - Déclenche les NoteEvent dont le timestamp tombe dans ce bloc.
        - Appelle get_first() avec les bons paramètres.
        - Appelle get_next() pour les daughters déjà en cours de lecture.
        - Mixe les voies.
        - Convertit en int32 pour la sortie.

        ⚠️ Le callback doit être ultra rapide.
        """
        try:
            nb_channels = len(self._daughters)

            # Un buffer par voie
            buffers = [None] * nb_channels

            # Déclenchement des événements dont le ts tombe dans ce bloc
            while self._events and (self._pos_samples <= self._events[0].ts < self._pos_samples + frames):
                ev = heapq.heappop(self._events)

                start = ev.ts - self._pos_samples
                stop = frames

                # get_first() démarre la lecture du sample avec les bons paramètres
                first_chunk = ev.daughter.get_first(
                    samplerate=self.SR,
                    frames=stop - start,
                    **ev.params
                )

                buffers[ev.channel] = numpy.concatenate((
                    numpy.zeros(start, dtype='float32'),
                    first_chunk
                ))

            # Pour les daughters sans événement → get_next()
            silence = numpy.zeros(frames, dtype='float32')

            for i in range(nb_channels):
                if buffers[i] is None:
                    nxt = self._daughters[i].get_next(self.SR, frames)
                    buffers[i] = nxt if nxt is not None else silence

            # Mixage des voies
            mixed = numpy.sum(buffers, axis=0)

            # Normalisation / clipping
            mixed = numpy.clip(mixed / nb_channels, -1.0, 1.0)

            # Conversion float32 → int32
            mixed = (mixed * (2 ** 31 - 1)).astype('int32')

            # Copie dans le buffer de sortie
            outdata[:] = mixed.tobytes()

            # Avancement du compteur
            self._pos_samples += frames

        except Exception as e:
            print("Callback error:", e)
            raise e

    def run(self):
        """
        Démarre le séquenceur et boucle tant que tous les événements n'ont pas été consommés.

        - Initialise le compteur d'échantillons
        - Démarre le flux audio
        - Boucle avec un sleep pour éviter de saturer le CPU
        - Affiche régulièrement la position en samples

        ⚠️ Cette méthode est bloquante.
        """
        self._pos_samples = 0
        self._stream.start()

        while self._events:
            time.sleep(0.5)
            print(self._pos_samples)

        self._stream.stop()
