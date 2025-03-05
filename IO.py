#! /usr/bin/env python3
# IO.py
# programmed by Saito-Saito-Saito
# explained on https://Saito-Saito-Saito.github.io/chess
# last updated: 04 March 2021

from config import *

local_logger = setLogger(__name__)

def ToggleType(target, logger=local_logger):
    if type(target) is int:
        if target == EMPTY:
            return ' '
        elif target == P * BLACK:
            return '♙'
        elif target == R * BLACK:
            return '♖'
        elif target == N * BLACK:
            return '♘'
        elif target == B * BLACK:
            return '♗'
        elif target == Q * BLACK:
            return '♕'
        elif target == K * BLACK:
            return '♔'
        elif target == P * WHITE:
            return '♟'
        elif target == R * WHITE:
            return '♜'
        elif target == N * WHITE:
            return '♞'
        elif target == B * WHITE:
            return '♝'
        elif target == Q * WHITE:
            return '♛'
        elif target == K * WHITE:
            return '♚'
        else:
            logger.error('UNEXPECTED INPUT VALUE of A PIECE into IO.ToggleType')
            return False
    elif type(target) is str:
        if target.isdecimal():
            return int(target)
        elif ord('a') <= ord(target) <= ord('h'):
            return ord(target) - ord('a') + 1
        elif target == 'P':
            return P
        elif target == 'R':
            return R
        elif target == 'N':
            return N
        elif target == 'B':
            return B
        elif target == 'Q':
            return Q
        elif target == 'K':
            return K
        else:
            logger.error('UNEXPECTED INPUT into IO.ToggleType')
            return False
    else:
        logger.error('UNEXPECTED INPUT TYPE into IO.ToggleType')
        return False

def instruction():
    print('''
    棋譜の書き方には何通りかありますが、ここでは FIDE (The International Chess Federalation) 公認の standard algebraic notation と呼ばれる記法を使用します。
    簡単に言えば、次のように書きます。
    ・動かす駒をアルファベット大文字で表す。ポーンは省略。
        P(Pawn), R(Rook), N(Knight), B(Bishop), Q(Queen), K(King)
    ・移動元の位置を省略可。必要ならアルファベット小文字と数字で表す。
        a-h(筋), 1-8(段)
    ・移動先をアルファベット小文字と数字で表す。
        a-h(筋), 1-8(段)
    ・取った場合は "x" を入れる。
    ・チェックした場合は "+" を、チェックメイトした場合は "#" を末尾に付ける。
    ・ポーンが最終段に到達した場合、プロモーション先を "=アルファベット大文字" で表す。
    ・キャスリングは "O-O" (キングサイド) か "O-O-O" (クイーンサイド)。
    ・ゲーム終了は "1-0" (白勝ち)、"0-1" (黒勝ち)、"1/2-1/2" (引き分け)。
    
    例：
    e4 (ポーンを e4 に進める)
    Nf3 (ナイトを f3 に動かす)
    exd5 (e のポーンが d5 を取る)
    Bb5+ (ビショップを b5 に動かし、チェック)
    Qxe7# (クイーンが e7 を取り、チェックメイト)
    e8=Q (ポーンが e8 に達し、クイーンにプロモーション)
    O-O (キングサイドキャスリング)
    1-0 (白の勝利)
    ''')
    input()

if __name__ == "__main__":
    try:
        print(ToggleType(input('enter a toffled str: ')))
    except:
        print('INVALID INPUT')
    try:
        print(ToggleType(int(input('Enter a toggled int: '))))
    except:
        print('INVALID INPUT')
    input('ENTER TO INSTRUCT')
    instruction()