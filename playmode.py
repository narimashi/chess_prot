#! /usr/bin/env python3
# playmode.py
# programmed by Saito-Saito-Saito, modified by Grok 3 (xAI)
# last updated: March 04, 2025

import sys

from config import *
import board
import IO

local_logger = setLogger(__name__)

def playmode(turnmode=True, logger=None):
    logger = logger or local_logger
    
    record = open(MAINRECADDRESS, 'w')
    record.close()
    record = open(SUBRECADDRESS, 'w')
    record.close()

    main_board = board.Board()
    main_board.print(turnmode=turnmode)

    while True:
        if main_board.king_place(main_board.player) == False:
            winner = -main_board.player
            break
        if main_board.checkmatejudge(main_board.player):
            print('CHECKMATE')
            winner = -main_board.player
            break
        if main_board.stalematejudge(main_board.player):
            print('STALEMATE')
            winner = EMPTY
            break

        if main_board.player == WHITE:
            print('WHITE (X to resign / H to help / Z to back) >>> ', end='')
        elif main_board.player == BLACK:
            print('BLACK (X to resign / H to help / Z to back) >>> ', end='')

        main_board.s = input().replace(' ', '').replace('o', 'O')
        logger.debug(f"Player input: {main_board.s}")

        if main_board.s in ['H', 'h']:
            IO.instruction()
            main_board.print(turnmode=turnmode, reverse=False)
            main_board.s = ''
            continue
        if main_board.s in ['X', 'x']:
            winner = -main_board.player
            break
        if main_board.s in ['Z', 'z']:
            if main_board.player == WHITE:
                print('Do you agree, BLACK (y/n)? >>> ', end='')
            elif main_board.player == BLACK:
                print('Do you agree, WHITE (y/n)? >>> ', end='')
            if input() not in ['y', 'Y', 'Yes', 'YES', 'yes']:
                main_board.s = ''
                continue
            new_board = main_board.tracefile(main_board.turn - 1, main_board.player, isrecwrite=True)
            if new_board == main_board:
                logger.warning('IMPOSSIBLE TO BACK')
                print('SORRY, NOW WE CANNOT BACK THE BOARD')
            else:
                main_board = new_board
                main_board.print(turnmode=turnmode)
            main_board.s = ''
            continue

        motion = main_board.s_analyze()
        if type(motion) is int:
            if motion == EMPTY:
                if main_board.player == WHITE:
                    print('Do you agree, BLACK (y/n)? >>>', end=' ')
                elif main_board.player == BLACK:
                    print('Do you agree, WHITE (y/n)? >>>', end=' ')
                if input() in ['y', 'Y']:
                    winner = EMPTY
                    break
                else:
                    main_board.print(turnmode=turnmode, reverse=False)
                    main_board.s = ''
                    continue
            elif motion == WHITE == -main_board.player:
                winner = WHITE
                break
            elif motion == BLACK == -main_board.player:
                winner = BLACK
                break
            else:
                print('INVALID INPUT')
                main_board.s = ''
                continue
        if motion == False:
            print('INVALID INPUT/MOTION')
            main_board.s = ''
            continue

        if motion[0] is None and motion[1] is None:  # 持ち駒を打つ場合
            piece_type = IO.ToggleType(main_board.s[0])
            to_file = motion[2]
            to_rank = motion[3]
            logger.debug(f"Attempting drop with piece_type={piece_type}, to_file={to_file}, to_rank={to_rank}")
            drop_result = main_board.drop_piece(piece_type, to_file, to_rank)
            if drop_result:
                logger.debug(f"Drop succeeded at {chr(ord('a') + to_file)}{to_rank + 1}")
                main_board.record(MAINRECADDRESS)
                if main_board.player == BLACK:
                    main_board.turn += 1
                main_board.player *= -1
                main_board.print(turnmode=turnmode)
            else:
                print('INVALID DROP')
                main_board.s = ''
                continue
        else:  # 通常の移動
            if not main_board.move(*motion):
                print('INVALID MOTION')
                main_board.s = ''
                continue
            main_board.record(MAINRECADDRESS)
            if main_board.player == BLACK:
                main_board.turn += 1
            main_board.player *= -1
            main_board.print(turnmode=turnmode)

        main_board.s = ''

    print('\nGAME SET')
    if winner == EMPTY:
        print('1/2 - 1/2\tDRAW')
        main_board.s = '1/2-1/2 '
        main_board.record(MAINRECADDRESS)
    elif winner == WHITE:
        print('1 - 0\tWHITE WINS')
        main_board.s = '1-0 '
        main_board.record(MAINRECADDRESS)
    elif winner == BLACK:
        print('0 - 1\tBLACK WINS')
        main_board.s = '0-1 '
        main_board.record(MAINRECADDRESS)

    if input('\nDo you want the record (y/n)? >>> ') in ['y', 'Y', 'yes', 'YES', 'Yes']:
        record = open(MAINRECADDRESS, 'r')
        print('\n------------------------------------')
        print(record.read())
        print('------------------------------------')
        record.close()

    print('\nGAME OVER\n')

if __name__ == "__main__":
    playmode()