#
# main.py
#

from daughters import Daughter, kick, tom, hi_hat
from sequencer import Sequencer

if __name__ == '__main__':

    seq = Sequencer([hi_hat, tom, kick])

    for i in range(0, seq.SR * 50, seq.SR * 4):
        cpl = 0
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 0*seq.SR/4)) # 1
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 1*seq.SR/4)) # &
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 2*seq.SR/4)) # 2
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 3*seq.SR/4)) # &
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 4*seq.SR/4)) # 3
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 5*seq.SR/4)) # &
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 6*seq.SR/4)) # 4
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 7*seq.SR/4)) # &

        seq.add_note_event(tom, round(i + cpl*seq.SR*2 + 2*seq.SR/4))
        seq.add_note_event(tom, round(i + cpl*seq.SR*2 + 4*seq.SR/4), tom.make_params(gain=20))
        seq.add_note_event(tom, round(i + cpl*seq.SR*2 + 6*seq.SR/4))

        seq.add_note_event(kick, round(i + cpl*seq.SR*2 + 0*seq.SR/4))
        seq.add_note_event(kick, round(i + cpl*seq.SR*2 + 3*seq.SR/4))
        seq.add_note_event(kick, round(i + cpl*seq.SR*2 + 5*seq.SR/4))

        cpl = 1
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 0 * seq.SR / 4))  # 1
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 1 * seq.SR / 4))  # &
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 2 * seq.SR / 4))  # 2
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 3 * seq.SR / 4))  # &
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 4 * seq.SR / 4))  # 3
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 5 * seq.SR / 4))  # &
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 6 * seq.SR / 4))  # 4
        seq.add_note_event(hi_hat, round(i + cpl*seq.SR*2 + 7 * seq.SR / 4), hi_hat.make_params(gain=140))  # & (accent)

        seq.add_note_event(tom, round(i + cpl*seq.SR*2 + 2 * seq.SR / 4))  # 2
        seq.add_note_event(tom, round(i + cpl*seq.SR*2 + 4 * seq.SR / 4), tom.make_params(gain=20))  # 3 accent
        seq.add_note_event(tom, round(i + cpl*seq.SR*2 + 6 * seq.SR / 4))  # 4

        # Petit break sur les deux dernières croches
        seq.add_note_event(tom, round(i + cpl*seq.SR*2 + 7 * seq.SR / 4), tom.make_params(gain=30))
        seq.add_note_event(tom, round(i + cpl*seq.SR*2 + 8 * seq.SR / 4), tom.make_params(gain=40))

        seq.add_note_event(kick, round(i + cpl*seq.SR*2 + 0 * seq.SR / 4))  # 1
        seq.add_note_event(kick, round(i + cpl*seq.SR*2 + 2 * seq.SR / 4))  # 2 (nouveau)
        seq.add_note_event(kick, round(i + cpl*seq.SR*2 + 3 * seq.SR / 4))  # 2&
        seq.add_note_event(kick, round(i + cpl*seq.SR*2 + 5 * seq.SR / 4))  # 3&
        seq.add_note_event(kick, round(i + cpl*seq.SR*2 + 7 * seq.SR / 4))  # 4&

    try:
        seq.run()
    except KeyboardInterrupt:
        print("Exiting due to user interrupt...")
        exit(0)
