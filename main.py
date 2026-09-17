#
# main.py
#
from smtplib import SMTPRecipientsRefused

from daughters import Daughter, kick, tom, hi_hat
from sequencer import Sequencer

if __name__ == '__main__':

    seq = Sequencer([hi_hat, tom, kick])

    frame = 0
    BPM = 120
    tps = (60/BPM) * seq.SR

    for i in range(4):

        # 1er couplet
        for s in range(8):
            seq.add_note_event(hi_hat, round(frame + s * tps / 2)) # 1, 1&, 2, 2&, 3, 3&, 4, 4&

        seq.add_note_event(tom, round(frame + 2*tps/2))   # 2
        seq.add_note_event(tom(gain=20), round(frame + 4*tps/2)) # 3
        seq.add_note_event(tom, round(frame + 6*tps/2))   # 4

        seq.add_note_event(kick, round(frame + 0*tps/2))
        seq.add_note_event(kick, round(frame + 3*tps/2))
        seq.add_note_event(kick, round(frame + 5*tps/2))
        frame += tps*4  # Mesure à 4/4

        # 2ème couplet
        for s in range(7):  # jusqu'à 4.
            seq.add_note_event(hi_hat, round(frame + s*tps/2)) # 1
        seq.add_note_event(hi_hat(gain=140), round(frame + 7 * tps/2))  # 4& (accent)

        seq.add_note_event(tom, round(frame + 2*tps/2))  # 2
        seq.add_note_event(tom(gain=20), round(frame + 4*tps/2))  # 3 accent
        seq.add_note_event(tom, round(frame + 6*tps/2))  # 4
        # Petit break sur les deux dernières croches
        seq.add_note_event(tom(gain=30), round(frame + 7*tps/2)) # 4&
        seq.add_note_event(tom(gain=40), round(frame + 8*tps/2)) # 5

        seq.add_note_event(kick, round(frame + 0*tps/2))  # 1
        seq.add_note_event(kick, round(frame + 2*tps/2))  # 2 (nouveau)
        seq.add_note_event(kick, round(frame + 3*tps/2))  # 2&
        seq.add_note_event(kick, round(frame + 5*tps/2))  # 3&
        seq.add_note_event(kick, round(frame + 7*tps/2))  # 4&
        frame += tps*4  # Mesure à 4/4

    try:
        seq.run()
    except KeyboardInterrupt:
        print("Exiting due to user interrupt...")
        exit(0)
