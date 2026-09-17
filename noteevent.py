#
# NoteEvent.py
#

from dataclasses import dataclass
from typing import Dict, Any
from daughters import Daughter

@dataclass()
class NoteEvent:
    """
    Représente un événement musical planifié dans le temps.

    Un NoteEvent est une instruction disant :
    « À l’instant ts (en frames), déclenche la Daughter X avec les paramètres Y ».

    Champs :
    - ts : timestamp en frames (position absolue dans la timeline audio)
    - channel : index de la Daughter dans le Sequencer (routing interne)
    - daughter : instance réelle de Daughter (source audio)
    - params : dictionnaire de paramètres (gain, pitch, etc.)

    Le NoteEvent est comparable (via __lt__) pour être stocké dans une heap.
    Le tri se fait uniquement sur (ts, channel), ce qui garantit :
    - un ordre strict des événements
    - aucune comparaison de types non comparables (Daughter, params)
    - un comportement déterministe dans heapq
    """

    ts: int                      # timestamp en frames
    channel: int                 # index dans la liste du sequencer
    daughter: Daughter           # instance réelle (voie)
    params: Dict[str, Any]       # paramètres de l’événement (gain, etc.)

    def __lt__(self, other):
        """
        Définition explicite de l'ordre strict entre deux événements.

        Le tri se fait sur :
        1. ts (timestamp)
        2. channel (voie)

        Pourquoi ?
        - heapq doit pouvoir comparer les événements pour les ordonner.
        - ts suffit pour l'ordre temporel.
        - channel sert de tiebreaker si deux événements ont le même ts.
        - On NE compare PAS daughter ni params (non comparables).

        Grâce à cette méthode :
        - heapq ne plante jamais
        - l'ordre est déterministe
        """
        return (self.ts, self.channel) < (other.ts, other.channel)
