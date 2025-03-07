#! /usr/bin/env python3
# fundam.py
# programmed by Saito-Saito-Saito
# explained on https://Saito-Saito-Saito.github.io/chess
# last updated: 15 August 2020

import config

# positive or negative (returning 1, -1, or 0)
def PosNeg(subject):
    if subject > 0:
        return 1
    elif subject < 0:
        return -1
    else:
        return 0

# whether the index is in the board (bool)
def InSize(subject):
    if 0 <= subject < config.SIZE:
        return True
    else:
        return False

if __name__=="__main__":
    try:
        print(PosNeg(int(input('Enter a posnegee '))))
    except:
        print('INVALID INPUT')
    try:
        print(InSize(int(input('Enter an InSizee '))))
    except:
        print('INVALID INPUT')