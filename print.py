#! usr/bin/env/ Python3
# print.py
# coded by Saito-Saito-Saito
# explained on https://Saito-Saito-Saito.github.io/chess
# last updated: 15 August 2020
# NOTE: This code is only for explaining, so is not neccessary to run.

from board import *

class BoardPrint(Board):
    def PrintWhiteSide(self):
        print('\n')
        print('\t    a   b   c   d   e   f   g   h')
        print('\t   -------------------------------')
        for rank in range(SIZE - 1, -1, -1):  # down to less
            print('\t{} |'.format(rank + 1), end='')
            for file in range(SIZE):
                print(' {} |'.format(IO.ToggleType(self.board[file][rank])), end='')
            print(' {}'.format(rank + 1))
            print('\t   -------------------------------')
        print('\t    a   b   c   d   e   f   g   h')
        print('\n')
    

if __name__ == "__main__":
    test_board = BoardPrint()
    test_board.print()