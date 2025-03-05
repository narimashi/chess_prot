#! /usr/bin/env python3
# readmode.py
# programmed by Saito-Saito-Saito
# explained on https://Saito-Saito-Saito.github.io/chess
# last updated: 15 August 2020


import sys

from config import *
import board

local_logger = setLogger(__name__)


def readmode(turnmode=False, reverse=False, logger=None):
    # logger setup
    logger = logger or local_logger
    
    # initializing the board
    main_board = board.Board()
    main_board.print()
    print('ENTER TO START')
    input()
    
    while True:
        # displaying turn number and player
        if main_board.player == WHITE:
            print('\n{}\tWHITE'.format(main_board.turn), end='\t')
            new_board = main_board.tracefile(main_board.turn, BLACK, False)
        elif main_board.player == BLACK:
            print('\n{}\tBLACK'.format(main_board.turn), end='\t')
            new_board = main_board.tracefile(main_board.turn + 1, WHITE, False)
        else:
            logger.error('UNEXPECTED VALUE of PLAYER in readmode')
            print('SYSTEM ERROR')
            sys.exit('SYSTEM ERROR')

        if type(new_board) is int:
            if new_board == EMPTY:
                print('1/2-1/2\n\nDRAW')
                return
            elif new_board == WHITE:
                print('1-0\n\nWHITE WINS')
                return
            elif new_board == BLACK:
                print('0-1\n\nBLACK WINS')
                return
            else:
                logger.error('UNEXPECTED VALUE of new_board in readmode')
                print('SYSTEM ERROR')
                sys.exit('SYSTEM ERROR')
        # moving a piece
        else:
            main_board = new_board
            print(main_board.s)
            main_board.print(turnmode=turnmode, reverse=reverse)

        # exit code
        print('ENTER TO NEXT / X TO QUIT ', end='')
        if input() in ['X', 'x']:
            print('QUITTED')
            return


if __name__=="__main__":
    readmode()