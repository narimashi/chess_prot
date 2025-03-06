#! /usr/bin/env python3
# playmode_gui.py
# programmed by Saito-Saito-Saito, modified by Grok 3 (xAI)
# last updated: March 06, 2025

import pygame
import sys
import os
from config import *
import board
import IO
import fundam
import logging

# ログ設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Pygameの初期化
pygame.init()

# 画面設定
SQUARE_SIZE = 64
BOARD_SIZE = SIZE * SQUARE_SIZE
WINDOW_WIDTH = BOARD_SIZE + 200
WINDOW_HEIGHT = BOARD_SIZE
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Special Chess GUI")

# 色の定義
WHITE_COLOR = (245, 245, 220)
BLACK_COLOR = (139, 69, 19)
HIGHLIGHT_COLOR = (255, 255, 0, 100)

# 駒の画像をロードし、スケーリング
piece_images = {
    WHITE * PAWN: pygame.transform.scale(pygame.image.load('pieces/wp.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
    WHITE * ROOK: pygame.transform.scale(pygame.image.load('pieces/wr.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
    WHITE * KNIGHT: pygame.transform.scale(pygame.image.load('pieces/wn.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
    WHITE * BISHOP: pygame.transform.scale(pygame.image.load('pieces/wb.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
    WHITE * QUEEN: pygame.transform.scale(pygame.image.load('pieces/wq.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
    WHITE * KING: pygame.transform.scale(pygame.image.load('pieces/wk.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
    BLACK * PAWN: pygame.transform.scale(pygame.image.load('pieces/bp.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
    BLACK * ROOK: pygame.transform.scale(pygame.image.load('pieces/br.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
    BLACK * KNIGHT: pygame.transform.scale(pygame.image.load('pieces/bn.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
    BLACK * BISHOP: pygame.transform.scale(pygame.image.load('pieces/bb.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
    BLACK * QUEEN: pygame.transform.scale(pygame.image.load('pieces/bq.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
    BLACK * KING: pygame.transform.scale(pygame.image.load('pieces/bk.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
}

# フォント設定
font = pygame.font.SysFont(None, 36)

def draw_board(main_board, selected_square=None):
    for row in range(SIZE):
        for col in range(SIZE):
            color = WHITE_COLOR if (row + col) % 2 == 0 else BLACK_COLOR
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = main_board.board[col][row]
            if piece != EMPTY:
                screen.blit(piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))
    
    if selected_square and isinstance(selected_square, tuple) and len(selected_square) == 2:
        col, row = selected_square
        highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        highlight.fill(HIGHLIGHT_COLOR)
        screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def draw_captured_pieces(main_board):
    white_captured = main_board.captured_pieces[WHITE]  # 白が取った駒（黒の駒、負の値）
    black_captured = main_board.captured_pieces[BLACK]  # 黒が取った駒（白の駒、正の値）
    
    # 白の持ち駒エリア（左側）に黒が取った白の駒を表示
    for i, piece in enumerate(black_captured):
        screen.blit(piece_images[piece], (BOARD_SIZE + 10, 10 + i * SQUARE_SIZE))
    
    # 黒の持ち駒エリア（右側）に白が取った黒の駒を表示
    for i, piece in enumerate(white_captured):
        screen.blit(piece_images[piece], (BOARD_SIZE + 80, 10 + i * SQUARE_SIZE))

def main():
    main_board = board.Board()
    selected_square = None
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
                
                # ボード外（持ち駒エリア）のクリック
                if col >= SIZE:
                    piece_idx = y // SQUARE_SIZE
                    if main_board.player == WHITE and piece_idx < len(main_board.captured_pieces[WHITE]):
                        selected_square = ("captured", WHITE, piece_idx)
                        logger.debug(f"Selected captured piece: White, index {piece_idx}")
                    elif main_board.player == BLACK and piece_idx < len(main_board.captured_pieces[BLACK]):
                        selected_square = ("captured", BLACK, piece_idx)
                        logger.debug(f"Selected captured piece: Black, index {piece_idx}")
                    continue
                
                # ボード内のクリック
                if selected_square is None:
                    if main_board.board[col][row] != EMPTY and fundam.PosNeg(main_board.board[col][row]) == main_board.player:
                        selected_square = (col, row)
                        logger.debug(f"Selected square: ({col}, {row})")
                else:
                    if selected_square[0] == "captured":  # 持ち駒を選択していた場合
                        player, idx = selected_square[1], selected_square[2]
                        piece = main_board.captured_pieces[player][idx]
                        logger.debug(f"Attempting drop: piece={piece} at ({col}, {row})")
                        if main_board.drop_piece(abs(piece), col, row):
                            logger.debug("Drop successful")
                            selected_square = None
                        else:
                            logger.debug("Drop failed")
                            selected_square = None
                    else:  # 通常の移動
                        fr_col, fr_row = selected_square
                        logger.debug(f"Attempting move: from ({fr_col}, {fr_row}) to ({col}, {row})")
                        if main_board.move(fr_col, fr_row, col, row):
                            logger.debug("Move successful")
                            selected_square = None
                        else:
                            logger.debug("Move failed")
                            selected_square = None
        
        # 画面描画
        screen.fill((255, 255, 255))
        draw_board(main_board, selected_square if isinstance(selected_square, tuple) and len(selected_square) == 2 else None)
        draw_captured_pieces(main_board)
        
        turn_text = font.render(f"Turn: {'White' if main_board.player == WHITE else 'Black'}", True, (0, 0, 0))
        screen.blit(turn_text, (BOARD_SIZE + 10, WINDOW_HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()