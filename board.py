#! /usr/bin/env python3
# board.py
# programmed by Saito-Saito-Saito, modified by Grok 3 (xAI)
# last updated: March 05, 2025

import copy
import re
import sys

from config import *
import fundam
import IO

local_logger = setLogger(__name__)

class Board:
    def __init__(self, *, board=[], target=[OVERSIZE, OVERSIZE], castl_k=[WHITE, BLACK], castl_q=[WHITE, BLACK], player=WHITE, turn=1, s='', logger=local_logger):
        if len(board) == SIZE:
            self.board = copy.deepcopy(board)
        else:
            self.board = [
                [R, P, 0, 0, 0, 0, -P, -R],
                [N, P, 0, 0, 0, 0, -P, -N],
                [B, P, 0, 0, 0, 0, -P, -B],
                [Q, P, 0, 0, 0, 0, -P, -Q],
                [K, P, 0, 0, 0, 0, -P, -K],
                [B, P, 0, 0, 0, 0, -P, -B],
                [N, P, 0, 0, 0, 0, -P, -N],
                [R, P, 0, 0, 0, 0, -P, -R]
            ]
        self.ep_target = copy.deepcopy(target)
        self.castl_k = copy.deepcopy(castl_k)
        self.castl_q = copy.deepcopy(castl_q)
        self.turn = turn
        self.player = player
        self.s = s
        self.logger = logger
        self.captured_pieces = {WHITE: [], BLACK: []}

    def print(self, *, turnmode=True, reverse=False):
        start = [SIZE - 1, 0]
        stop = [-1, SIZE]
        step = [-1, +1]
        switch = bool(turnmode and (self.player == BLACK))
        if reverse:
            switch = not switch
            
        print('\n')
        if switch:
            print('\t    h   g   f   e   d   c   b   a')
        else:
            print('\t    a   b   c   d   e   f   g   h')
        print('\t   -------------------------------')
        for rank in range(start[switch], stop[switch], step[switch]):
            print('\t{} |'.format(rank + 1), end='')
            for file in range(start[not switch], stop[not switch], step[not switch]):
                print(' {} |'.format(IO.ToggleType(self.board[file][rank])), end='')
            print(' {}'.format(rank + 1))
            print('\t   -------------------------------')
        if switch:
            print('\t    h   g   f   e   d   c   b   a')
        else:
            print('\t    a   b   c   d   e   f   g   h')
        print(f"\nWhite's captured pieces: {[IO.ToggleType(piece) for piece in self.captured_pieces[WHITE]]}")
        print(f"Black's captured pieces: {[IO.ToggleType(piece) for piece in self.captured_pieces[BLACK]]}")
        print('\n')

    def motionjudge(self, frFILE, frRANK, toFILE, toRANK, promote=EMPTY, logger=None):
        logger = logger or self.logger
        
        if not (fundam.InSize(frFILE) and fundam.InSize(frRANK) and fundam.InSize(toFILE) and fundam.InSize(toRANK)):
            logger.debug('OUT OF THE BOARD')
            return False

        player = fundam.PosNeg(self.board[frFILE][frRANK])
        piece = abs(self.board[frFILE][frRANK])
        
        if fundam.PosNeg(self.board[toFILE][toRANK]) == player:
            logger.debug('MOVING TO OWN SQUARE')
            return False

        if piece == EMPTY:
            logger.debug('MOVING EMPTY')
            return False

        elif piece == PAWN:
            if (toRANK == 8 - 1 or toRANK == 1 - 1) and promote not in [R, N, B, Q]:
                logger.info('NECESSARY TO PROMOTE')
                return False
            if frFILE == toFILE and toRANK - frRANK == player and self.board[toFILE][toRANK] == EMPTY:
                return True
            if abs(toFILE - frFILE) == 1 and toRANK - frRANK == player and fundam.PosNeg(self.board[toFILE][toRANK]) == -player:
                return True
            if ((player == WHITE and frRANK == 2 - 1) or (player == BLACK and frRANK == 7 - 1)) and frFILE == toFILE and toRANK - frRANK == 2 * player and self.board[frFILE][frRANK + player] == self.board[toFILE][toRANK] == EMPTY:
                return True
            if abs(self.ep_target[FILE] - frFILE) == 1 and frRANK == self.ep_target[RANK] and toFILE == self.ep_target[FILE] and toRANK - self.ep_target[RANK] == player and self.board[toFILE][toRANK] == EMPTY:
                return True
            logger.debug('INVALID MOTION of PAWN')
            return False

        elif piece == ROOK:
            if frFILE != toFILE and frRANK != toRANK:
                logger.debug('INVALID MOTION of ROOK')
                return False

        elif piece == KNIGHT:
            if (abs(toFILE - frFILE) == 1 and abs(toRANK - frRANK) == 2) or (abs(toFILE - frFILE) == 2 and abs(toRANK - frRANK) == 1):
                return True
            logger.debug('INVALID MOTION of KNIGHT')
            return False

        elif piece == BISHOP:
            if abs(toFILE - frFILE) != abs(toRANK - frRANK):
                logger.debug('INVALID MOTION of BISHOP')
                return False

        elif piece == QUEEN:
            if frFILE != toFILE and frRANK != toRANK and abs(toFILE - frFILE) != abs(toRANK - frRANK):
                logger.debug('INVALID MOTION of QUEEN')
                return False

        elif piece == KING:
            if abs(toFILE - frFILE) <= 1 and abs(toRANK - frRANK) <= 1:
                logger.debug('KING NORMAL')
                return True
            if player == WHITE:
                rank = 1 - 1
            elif player == BLACK:
                rank = 8 - 1
            else:
                logger.error('UNEXPECTED PLAYER VALUE in motionjudge')
                print('SYSTEM ERROR')
                sys.exit('SYSTEM ERROR')
            if player in self.castl_q and frFILE == e - 1 and frRANK == rank and toFILE == c - 1 and toRANK == rank and self.board[b - 1][rank] == self.board[c - 1][rank] == self.board[d - 1][rank] == EMPTY:
                for ran in range(SIZE):
                    for fil in range(SIZE):
                        if fundam.PosNeg(self.board[fil][ran]) == -player and (self.motionjudge(fil, ran, e - 1, rank, Q) or self.motionjudge(fil, ran, d - 1, rank, Q) or self.motionjudge(fil, ran, c - 1, rank, Q)):
                            logger.info('CHECKED IN THE WAY')
                            return False
                logger.debug('KING Q-side')
                return True
            if player in self.castl_k and frFILE == e - 1 and frRANK == rank and toFILE == g - 1 and toRANK == rank and self.board[f - 1][rank] == self.board[g - 1][rank] == EMPTY:
                for ran in range(SIZE):
                    for fil in range(SIZE):
                        if fundam.PosNeg(self.board[fil][ran]) == -player and (self.motionjudge(fil, ran, e - 1, rank, Q) or self.motionjudge(fil, ran, d - 1, rank, Q) or self.motionjudge(fil, ran, c - 1, rank, Q)):
                            logger.info('CHECKED IN THE WAY')
                            return False
                logger.debug('KING K-side')
                return True
            logger.debug('INVALID MOTION of KING')
            return False

        else:
            logger.error('UNEXPECTED VALUE of PIECE in motionjudge')
            print('SYSTEM ERROR')
            sys.exit('SYSTEM ERROR')

        direction = [fundam.PosNeg(toFILE - frFILE), fundam.PosNeg(toRANK - frRANK)]
        focused = [frFILE + direction[FILE], frRANK + direction[RANK]]
        while focused[FILE] != toFILE or focused[RANK] != toRANK:
            if not (fundam.InSize(focused[0]) and fundam.InSize(focused[1])):
                logger.warning('')
                break
            if self.board[focused[FILE]][focused[RANK]] != EMPTY:
                logger.debug('THERE IS AN OBSTACLE in the way')
                return False
            focused[FILE] += direction[FILE]
            focused[RANK] += direction[RANK]
        return True

    # ... (他の部分は変更なし)

    def move(self, frFILE, frRANK, toFILE, toRANK, promote=EMPTY, logger=None):
        logger = logger or self.logger
        
        if self.motionjudge(frFILE, frRANK, toFILE, toRANK, promote) == False:
            return False
        
        if fundam.PosNeg(self.board[frFILE][frRANK]) != self.player:
            logger.debug('MOVING OPPONENT PIECE OR EMPTY')
            return False

        piece = abs(self.board[frFILE][frRANK])
        
        if self.board[toFILE][toRANK] != EMPTY:
            captured_piece = self.board[toFILE][toRANK]  # 符号付きで保持
            self.captured_pieces[self.player].append(captured_piece)
            logger.info(f"Captured piece {IO.ToggleType(captured_piece)} added to player's stock")

        if piece == KING and abs(toFILE - frFILE) > 1:
            if self.player == WHITE:
                rank = 1 - 1
            elif self.player == BLACK:
                rank = 8 - 1
            else:
                logger.error('UNEXPECTED VALUE of PLAYER in move')
                print('SYSTEM ERROR')
                sys.exit('SYSTEM ERROR')
            if toFILE == c - 1:
                self.board[d - 1][rank] = self.player * ROOK
                self.board[a - 1][rank] = EMPTY
            elif toFILE == g - 1:
                self.board[f - 1][rank] = self.player * ROOK
                self.board[h - 1][rank] = EMPTY
            else:
                logger.error('UNEXPECTED VALUE of toFILE in move')
                return False
        if piece == PAWN and frFILE != toFILE and self.board[toFILE][toRANK] == EMPTY:
            self.board[self.ep_target[FILE]][self.ep_target[RANK]] = EMPTY
        if piece == PAWN and (toRANK == 8 - 1 or toRANK == 1 - 1):
            self.board[frFILE][frRANK] = self.player * promote
        
        self.board[toFILE][toRANK] = self.board[frFILE][frRANK]
        self.board[frFILE][frRANK] = EMPTY
        
        if piece == PAWN and abs(toRANK - frRANK) > 1:
            self.ep_target = [toFILE, toRANK]
        else:
            self.ep_target = [OVERSIZE, OVERSIZE]
        if self.player in self.castl_q and (piece == KING or (piece == ROOK and frFILE == a - 1)):
            self.castl_q.remove(self.player)
        if self.player in self.castl_k and (piece == KING or (piece == ROOK and frFILE == h - 1)):
            self.castl_k.remove(self.player)
        
        logger.info('SUCCESSFULLY MOVED')
        # ターン更新をここで実行
        self.record(MAINRECADDRESS)
        if self.player == BLACK:
            self.turn += 1
        self.player *= -1
        return True

# ... (他の部分は変更なし)

    # ... (他の部分は変更なし)

    def drop_piece(self, piece_type, toFILE, toRANK, logger=None):
        logger = logger or self.logger

        logger.debug(f"Attempting to drop {IO.ToggleType(piece_type)} at {chr(ord('a') + toFILE)}{toRANK + 1}")
        logger.debug(f"Board[{toFILE}][{toRANK}] = {self.board[toFILE][toRANK]}")
        logger.debug(f"Captured pieces for player {self.player}: {self.captured_pieces[self.player]}")
        logger.debug(f"piece_type = {piece_type}, type(piece_type) = {type(piece_type)}")

        if self.board[toFILE][toRANK] != EMPTY:
            logger.debug('TARGET SQUARE IS OCCUPIED')
            return False

        if abs(piece_type) == PAWN and (toRANK == (SIZE - 1) if self.player == WHITE else toRANK == 0):
            logger.debug('CANNOT DROP PAWN ON LAST RANK')
            return False

        if piece_type not in self.captured_pieces[self.player]:
            logger.debug('PIECE NOT IN CAPTURED STOCK')
            return False

        self.board[toFILE][toRANK] = self.player * abs(piece_type)  # 符号をプレイヤーに合わせて変換
        self.captured_pieces[self.player].remove(piece_type)
        logger.info(f"Dropped {IO.ToggleType(piece_type)} at {chr(ord('a') + toFILE)}{toRANK + 1}")
        self.record(MAINRECADDRESS)
        if self.player == BLACK:
            self.turn += 1
        self.player *= -1
        return True

# ... (他の部分は変更なし)

    def s_analyze(self, logger=None):
        logger = logger or self.logger
        self.s = self.s.replace(' ', '').replace('!', '').replace('?', '')
        logger.debug(f"Analyzing input: {self.s}")

        if len(self.s) == 0:
            logger.debug('len(s) == 0')
            return False

        drop_match = re.match(r'^([PRNBQK])\@([a-h][1-8])$', self.s)
        if drop_match:
            piece = IO.ToggleType(drop_match.group(1))
            toFILE = IO.ToggleType(drop_match.group(2)[0]) - 1
            toRANK = IO.ToggleType(drop_match.group(2)[1]) - 1
            logger.info(f"Detected drop: {piece} to {chr(ord('a') + toFILE)}{toRANK + 1}")
            logger.debug(f"Calling drop_piece with piece={piece}, toFILE={toFILE}, toRANK={toRANK}")
            if self.drop_piece(piece, toFILE, toRANK):
                logger.debug("Drop succeeded")
                return True
            else:
                logger.debug(f"Drop failed for {self.s}")
                return False

        match = re.match(r'^[PRNBQK]?[a-h]?[1-8]?[x]?[a-h][1-8](=[RNBQ]|e.p.)?[\++#]?$', self.s)
        if match:
            line = match.group()
            logger.info('line = {}'.format(line))

            if line[0] in ['P', 'R', 'N', 'B', 'Q', 'K']:
                piece = IO.ToggleType(line[0])
                line = line.lstrip(line[0]) 
            else:
                piece = PAWN
            logger.info('PIECE == {}'.format(piece))

            if line[0].isdecimal():
                frFILE = OVERSIZE
                frRANK = IO.ToggleType(line[0]) - 1
                line = line.lstrip(line[0])
            elif ord('a') <= ord(line[0]) <= ord('h') and ord('a') <= ord(line[1]) <= ord('x'):
                frFILE = IO.ToggleType(line[0]) - 1
                frRANK = OVERSIZE
                line = line[1:]
            else:
                frFILE = OVERSIZE
                frRANK = OVERSIZE
            logger.info('FR = {}, {}'.format(frFILE, frRANK))

            if line[0] == 'x':
                CAPTURED = True
                line = line.lstrip(line[0])
            else:
                CAPTURED = False

            toFILE = IO.ToggleType(line[0]) - 1
            toRANK = IO.ToggleType(line[1]) - 1
            logger.info('TO = {}, {}'.format(toFILE, toRANK))

            if '=' in line:
                promote = IO.ToggleType(line[line.index('=') + 1])
            else:
                promote = EMPTY
            logger.info('promote = {}'.format(promote))

            candidates = []
            for fil in range(SIZE):
                if fundam.InSize(frFILE) and frFILE != fil:
                    continue
                for ran in range(SIZE):
                    if fundam.InSize(frRANK) and frRANK != ran:
                        continue
                    if self.board[fil][ran] != self.player * piece:
                        continue
                    if self.motionjudge(fil, ran, toFILE, toRANK, promote) == False:
                        continue
                    candidates.append([fil, ran])
            logger.info('candidates = {}'.format(candidates))

            for reference in range(len(candidates)):
                local_board = Board(board=self.board, target=self.ep_target, castl_k=self.castl_k, castl_q=self.castl_q, player=self.player, turn=self.turn, s=self.s)
                local_board.move(candidates[reference][FILE], candidates[reference][RANK], toFILE, toRANK, promote)
                if CAPTURED or 'e.p.' in line:
                    if fundam.PosNeg(self.board[toFILE][toRANK]) == -self.player:
                        pass
                    elif fundam.InSize(toRANK - 1) and fundam.PosNeg(self.board[toFILE][toRANK - 1]) == -self.player and fundam.PosNeg(local_board.board[toFILE][toRANK - 1]) == EMPTY:
                        pass
                    elif fundam.InSize(toRANK + 1) and fundam.PosNeg(self.board[toFILE][toRANK + 1]) == -self.player and fundam.PosNeg(local_board.board[toFILE][toRANK + 1]) == EMPTY:
                        pass
                    else:
                        logger.info('{} does not capture any piece'.format(candidates[reference]))
                        del candidates[reference]
                        reference -= 1
                        continue
                
                if line.count('+') > local_board.checkcounter(-self.player):
                    logger.info('{} is short of the number of check'.format(candidates[reference]))
                    del candidates[reference]
                    reference -= 1
                    continue

                if '#' in line and local_board.checkmatejudge(-self.player) == False:
                    logger.info('{} does not checkmate'.format(candidates[reference]))
                    del candidates[reference]
                    reference -= 1
                    continue

                if 'e.p.' in line and self.board[toFILE][toRANK] != EMPTY:
                    logger.info('{} does not en passant'.format(candidates[reference]))
                    del candidates[reference]
                    reference -= 1
                    continue

            if len(candidates) == 1:
                logger.info('NORMALLY RETURNED')
                self.move(candidates[0][FILE], candidates[0][RANK], toFILE, toRANK, promote)
                return True
            elif len(candidates) > 1:
                logger.warning('THERE IS ANOTHER MOVE')
                self.move(candidates[0][FILE], candidates[0][RANK], toFILE, toRANK, promote)
                return True
            else:
                logger.info('THERE IS NO MOVE')
                return False

        else:
            if self.s == '1/2-1/2':
                logger.info('DRAW GAME')
                return EMPTY
            elif self.s == '1-0' and self.player == BLACK:
                logger.info('WHITE WINS')
                return WHITE
            elif self.s == '0-1' and self.player == WHITE:
                logger.info('BLACK WINS')
                return BLACK
            
            if self.player == WHITE:
                rank = 1 - 1
            elif self.player == BLACK:
                rank = 8 - 1
            else:
                logger.error('UNEXPECTED PLAYER VALUE in s_analyze')
                print('SYSTEM ERROR')
                sys.exit('SYSTEM ERROR')
            if self.s in ['O-O-O', 'o-o-o', '0-0-0'] and self.board[e - 1][rank] == self.player * KING:
                logger.info('format is {}, castl is {}'.format(self.s, self.castl_q))
                self.move(e - 1, rank, c - 1, rank, EMPTY)
                return True
            elif self.s in ['O-O', 'o-o', '0-0'] and self.board[e - 1][rank] == self.player * KING:
                logger.info('format is {}, castl is {}'.format(self.s, self.castl_k))
                self.move(e - 1, rank, g - 1, rank, EMPTY)
                return True
            
            logger.debug('INVALID FORMAT')
            return False

    def king_place(self, searcher):
        for fil in range(SIZE):
            if searcher * KING in self.board[fil]:
                return [fil, self.board[fil].index(searcher * KING)]
        return EMPTY

    def checkcounter(self, checkee, logger=None):
        logger = logger or self.logger
        
        TO = self.king_place(checkee)
        try:
            toFILE = TO[FILE]
            toRANK = TO[RANK]
        except:
            logger.info('THERE IS NO KING ON THE BOARD')
            return False

        count = 0
        for frFILE in range(SIZE):
            for frRANK in range(SIZE):
                if fundam.PosNeg(self.board[frFILE][frRANK]) == -checkee and self.motionjudge(frFILE, frRANK, toFILE, toRANK, Q):
                    logger.info('CHECK: {}, {} -> {}, {}'.format(frFILE, frRANK, toFILE, toRANK))
                    count += 1
        return count

    def checkmatejudge(self, matee, logger=None):
        logger = logger or self.logger
        
        if self.checkcounter(matee) in [False, 0]:
            logger.debug('NOT CHECKED')
            return False
        
        for frFILE in range(SIZE):
            for frRANK in range(SIZE):
                if fundam.PosNeg(self.board[frFILE][frRANK]) == matee:
                    for toFILE in range(SIZE):
                        for toRANK in range(SIZE):
                            local_board = Board(board=self.board, target=self.ep_target, castl_k=self.castl_k, castl_q=self.castl_q, player=matee)
                            if local_board.move(frFILE, frRANK, toFILE, toRANK, Q) and local_board.checkcounter(matee) == 0:
                                logger.info('THERE IS {}, {} -> {}, {}'.format(frFILE,frRANK,toFILE,toRANK))
                                return False
                    logger.debug('"FR = {}, {}" was unavailable'.format(frFILE, frRANK))
        return True

    def stalematejudge(self, matee, logger=None):
        logger = logger or self.logger
        
        if self.checkcounter(matee) not in [0, False]:
            logger.debug('CHECKED')
            return False

        for frFILE in range(SIZE):
            for frRANK in range(SIZE):
                if fundam.PosNeg(self.board[frFILE][frRANK]) == matee:
                    for toFILE in range(SIZE):
                        for toRANK in range(SIZE):
                            local_board = Board(board=self.board, target=self.ep_target, castl_k=self.castl_k, castl_q=self.castl_q, player=matee)
                            if local_board.move(frFILE, frRANK, toFILE, toRANK, Q) and local_board.checkcounter(matee) == 0:
                                logger.info('THERE IS {}, {} -> {}, {}'.format(frFILE,frRANK,toFILE,toRANK))
                                return False
                    logger.debug('"FR = {}, {}" was unavailable'.format(frFILE, frRANK))
        logger.info('STALEMATE. {} cannot move'.format(self.player))
        return True

    def record(self, address, logger=None):
        logger = logger or self.logger
        
        self.s = self.s.replace(' ', '').replace('!', '').replace('?', '')

        if len(self.s) == 0:
            logger.debug('len(s) == 0')
            return False

        match = re.match(r'^[PRNBQK]?[a-h]?[1-8]?[x]?[a-h][1-8](=[RNBQ]|e.p.)?[\++#]?$', self.s)
        if match:
            s_record = match.group()
        elif self.s in ['1-0', '0-1', '1/2-1/2']:
            s_record = self.s
        elif self.s in ['O-O-O', 'O-O', 'o-o-o', 'o-o', '0-0-0', '0-0']:
            s_record = self.s.replace('o', 'O').replace('0', 'O')
        elif re.match(r'^[PRNBQK]\@[a-h][1-8]$', self.s):
            s_record = self.s
        else:
            logger.info('OUT OF FORMAT in record')
            return False
        
        f = open(address, 'a')
        if s_record == '1-0':
            f.write('1-0')
        elif s_record == '0-1':
            f.write('{}\t0-1'.format(self.turn))
        elif self.player == WHITE:
            f.write('{}\t'.format(self.turn) + s_record.ljust(12))
        elif self.player == BLACK:
            f.write(s_record.ljust(12) + '\n')
        else:
            logger.error('UNEXPECTED VALUE of PLAYER in record')
            print('SYSTEM ERROR')
            sys.exit('SYSTEM ERROR')
        
        f.close()
        return True

    def tracefile(self, destination_turn, destination_player, isrecwrite=True, logger=None):
        logger = logger or self.logger
        
        if destination_turn == 1 and destination_player == WHITE:
            local_board = Board()
            return local_board

        open(SUBRECADDRESS, 'w').close()
        f = open(MAINRECADDRESS, 'r')
        line = f.read().strip()
        f.close()
        logger.info('line is "{}"'.format(line))

        local_board = Board()
        
        for letter in line:
            if letter in [' ', '\t', '\n', ',', '.']:
                logger.info('local_s is {}'.format(local_board.s))
                motion = local_board.s_analyze()
                if motion == True:
                    local_board.record(SUBRECADDRESS)
                    if local_board.turn == destination_turn and local_board.player == destination_player:
                        logger.info('trace succeeded')
                        if isrecwrite:
                            f = open(MAINRECADDRESS, 'w')
                            g = open(SUBRECADDRESS, 'r')
                            f.write(g.read())
                            f.close()
                            g.close()
                        return local_board
                elif type(motion) is int:
                    print('GAME SET')
                    if isrecwrite:
                        f = open(MAINRECADDRESS, 'w')
                        g = open(SUBRECADDRESS, 'r')
                        f.write(g.read())
                        f.close()
                        g.close()
                    return motion
                local_board.s = ''
            else:
                local_board.s = ''.join([local_board.s, letter])
                logger.debug('local_s = {}'.format(local_board.s))

        logger.info('local_s is {}'.format(local_board.s))
        motion = local_board.s_analyze()
        if motion == True:
            local_board.record(SUBRECADDRESS)
            if local_board.turn == destination_turn and local_board.player == destination_player:
                logger.info('trace succeeded')
                if isrecwrite:
                    f = open(MAINRECADDRESS, 'w')
                    g = open(SUBRECADDRESS, 'r')
                    f.write(g.read())
                    f.close()
                    g.close()
                return local_board
        elif type(motion) is int:
            if isrecwrite:
                f = open(MAINRECADDRESS, 'w')
                g = open(SUBRECADDRESS, 'r')
                f.write(g.read())
                f.close()
                g.close()
            return motion

        logger.warning('FAILED TO BACK')
        return self

if __name__ == "__main__":
    local_board = Board()
    local_board.print()
    local_board.move(c - 1, 2 - 1, c - 1, 4 - 1)
    local_board.print(turnmode=True)
    local_board.move(c - 1, 7 - 1, c - 1, 6 - 1)
    local_board.print(turnmode=True)
    print(local_board.king_place(WHITE))
    print(local_board.king_place(BLACK))