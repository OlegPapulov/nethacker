import os, sys
sys.setrecursionlimit(100000)
import numpy as np
from nle.nethack import nethack

game = nethack.Nethack()
game.set_options("wiz-hum-cha-mal")
obs = game.reset()
for i in range(30):
    if game.program_state.moveloop:
        break
    obs = game.step(nethack.ASCII_SPACE)
    if game.program_state.quit:
        break
print("moveloop:", game.program_state.moveloop, "iters", i)
tty = obs["tty_chars"]
for r in range(24):
    line = tty[r*80:(r+1)*80]
    print("|" + "".join(chr(c) if 32 <= c < 127 else " " for c in line) + "|")
game.close()
