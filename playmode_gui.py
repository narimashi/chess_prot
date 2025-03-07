#! /usr/bin/env python3
# playmode_gui.py
# programmed by Saito-Saito-Saito, modified by Grok 3 (xAI)
# last updated: March 07, 2025

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
WINDOW_HEIGHT = BOARD_SIZE + 200
WINDOW_WIDTH = BOARD_SIZE
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Special Chess GUI")

# 色の定義
WHITE_COLOR = (245, 245, 220)
BLACK_COLOR = (139, 69, 19)
HIGHLIGHT_COLOR = (255, 255, 0, 100)
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0, 200)
BUTTON_COLOR = (70, 130, 180)  # スチールブルー
BUTTON_HOVER_COLOR = (100, 149, 237)  # コーンフラワーブルー
GRADIENT_TOP = (70, 130, 180)  # グラデーション上部
GRADIENT_BOTTOM = (30, 60, 114)  # グラデーション下部

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

# カスタムフォントの読み込み
try:
    font_path = os.path.join("Roboto-Regular.ttf")  # フォントファイルのパス
    title_font = pygame.font.Font(font_path, 48)  # タイトル用フォント
    button_font = pygame.font.Font(font_path, 36)  # ボタン用フォント
    small_font = pygame.font.Font(font_path, 24)  # 小さいテキスト用フォント
except FileNotFoundError:
    logger.warning("Roboto-Regular.ttf not found. Falling back to default font.")
    title_font = pygame.font.SysFont(None, 48)
    button_font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)

def draw_board(main_board, selected_square=None):
    for row in range(SIZE):
        for col in range(SIZE):
            color = WHITE_COLOR if (row + col) % 2 == 0 else BLACK_COLOR
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE + 100, SQUARE_SIZE, SQUARE_SIZE))
            piece = main_board.board[col][row]
            if piece != EMPTY:
                screen.blit(piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE + 100))
    
    # ハイライト表示
    if selected_square and isinstance(selected_square, tuple) and len(selected_square) == 2:
        col, row = selected_square
        highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        highlight.fill(HIGHLIGHT_COLOR)
        screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE + 100))
    elif selected_square and isinstance(selected_square, tuple) and len(selected_square) == 6 and selected_square[2] == "drop_target":
        col, row, _, _, _, _ = selected_square
        highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        highlight.fill(HIGHLIGHT_COLOR)
        screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE + 100))

def draw_captured_pieces(main_board, selected_square=None):
    white_captured = main_board.captured_pieces[WHITE]
    black_captured = main_board.captured_pieces[BLACK]
    
    # 白の持ち駒（上部）
    for i, piece in enumerate(white_captured):
        abs_piece = abs(piece)
        displayed_piece = WHITE * abs_piece if piece < 0 else BLACK * abs_piece
        screen.blit(piece_images[displayed_piece], (i * SQUARE_SIZE, 10))
    
    # 黒の持ち駒（下部）
    for i, piece in enumerate(black_captured):
        abs_piece = abs(piece)
        displayed_piece = BLACK * abs_piece if piece > 0 else WHITE * abs_piece
        screen.blit(piece_images[displayed_piece], (i * SQUARE_SIZE, WINDOW_HEIGHT - SQUARE_SIZE - 10))
    
    # 選択中の持ち駒をハイライト
    if selected_square and selected_square[0] == "captured":
        player, idx = selected_square[1], selected_square[2]
        highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        highlight.fill(HIGHLIGHT_COLOR)
        if player == WHITE:
            screen.blit(highlight, (idx * SQUARE_SIZE, 10))
        else:
            screen.blit(highlight, (idx * SQUARE_SIZE, WINDOW_HEIGHT - SQUARE_SIZE - 10))

def draw_gradient_background(surface, top_color, bottom_color):
    """グラデーション背景を描画"""
    height = surface.get_height()
    gradient = pygame.Surface((1, height), pygame.SRCALPHA)
    for y in range(height):
        r = top_color[0] + (bottom_color[0] - top_color[0]) * y / height
        g = top_color[1] + (bottom_color[1] - top_color[1]) * y / height
        b = top_color[2] + (bottom_color[2] - top_color[2]) * y / height
        gradient.set_at((0, y), (int(r), int(g), int(b)))
    surface.blit(pygame.transform.scale(gradient, surface.get_size()), (0, 0))

def draw_button(surface, text, font, x, y, width, height, color, hover_color, mouse_pos):
    """ボタンを描画（ホバーエフェクト付き）"""
    button_rect = pygame.Rect(x, y, width, height)
    is_hovered = button_rect.collidepoint(mouse_pos)
    button_color = hover_color if is_hovered else color
    
    # ボタンの背景（影付き）
    shadow_surface = pygame.Surface((width + 4, height + 4), pygame.SRCALPHA)
    shadow_surface.fill((0, 0, 0, 50))
    surface.blit(shadow_surface, (x + 2, y + 2))
    
    # ボタンの描画
    pygame.draw.rect(surface, button_color, button_rect, 0, 5)
    pygame.draw.rect(surface, (255, 255, 255), button_rect, 2, 5)
    
    # テキストの描画
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)
    
    return button_rect

def get_promotion_choice(main_board, selected_square, clock):
    """昇格選択ダイアログを表示（オシャレなデザイン）"""
    choices = ['Q', 'R', 'N', 'B']
    buttons = []
    button_width = 150
    button_height = 50
    button_spacing = 10
    total_height = (button_height + button_spacing) * len(choices) - button_spacing
    start_y = (WINDOW_HEIGHT - total_height) // 2
    
    while True:
        # 現在のボードを再描画
        screen.fill((255, 255, 255))
        draw_board(main_board, selected_square if isinstance(selected_square, tuple) and len(selected_square) == 2 else None)
        draw_captured_pieces(main_board)
        turn_text = small_font.render(f"Turn: {'White' if main_board.player == WHITE else 'Black'}", True, (0, 0, 0))
        screen.blit(turn_text, (10, WINDOW_HEIGHT - 40))
        
        # 半透明のオーバーレイを描画
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # タイトル描画
        title_text = title_font.render("Choose Promotion", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, start_y - 60))
        screen.blit(title_text, title_rect)
        
        # マウスの位置を取得
        mouse_pos = pygame.mouse.get_pos()
        
        # 選択肢ボタンを描画
        buttons.clear()
        for i, choice in enumerate(choices):
            y = start_y + i * (button_height + button_spacing)
            button_rect = draw_button(
                screen,
                f"Promote to {choice}",
                button_font,
                (WINDOW_WIDTH - button_width) // 2,
                y,
                button_width,
                button_height,
                BUTTON_COLOR,
                BUTTON_HOVER_COLOR,
                mouse_pos
            )
            buttons.append((button_rect, choice))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button_rect, choice in buttons:
                    if button_rect.collidepoint(event.pos):
                        return choice
        
        clock.tick(60)

def draw_game_over(main_board, clock):
    """ゲーム終了メッセージを表示（オシャレなデザイン）"""
    result = main_board.is_game_over()
    message = ""
    if result == WHITE:
        message = "White Wins!"
    elif result == BLACK:
        message = "Black Wins!"
    elif result == EMPTY:
        message = "Draw by Stalemate!"
    
    if not message:
        return

    # フェードインアニメーションのためのアルファ値
    alpha = 0
    fade_speed = 5
    button_width = 200
    button_height = 50
    exit_button = None
    
    while True:
        # グラデーション背景
        draw_gradient_background(screen, GRADIENT_TOP, GRADIENT_BOTTOM)
        
        # メッセージのフェードイン
        text_surface = title_font.render(message, True, TEXT_COLOR)
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        screen.blit(text_surface, text_rect)
        
        # アルファ値を増加
        if alpha < 255:
            alpha += fade_speed
            alpha = min(alpha, 255)
        
        # マウスの位置を取得
        mouse_pos = pygame.mouse.get_pos()
        
        # 終了ボタンの描画
        exit_button = draw_button(
            screen,
            "Exit",
            button_font,
            (WINDOW_WIDTH - button_width) // 2,
            WINDOW_HEIGHT // 2 + 50,
            button_width,
            button_height,
            BUTTON_COLOR,
            BUTTON_HOVER_COLOR,
            mouse_pos
        )
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    return
        
        clock.tick(60)

def main():
    main_board = board.Board()
    selected_square = None
    clock = pygame.time.Clock()
    move_made = False  # 移動が完了したかどうかを追跡
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // SQUARE_SIZE
                row = (y - 100) // SQUARE_SIZE
                
                # 持ち駒エリアのクリック
                if y < 100:  # 上部（白の持ち駒エリア）
                    piece_idx = x // SQUARE_SIZE
                    if selected_square and (selected_square[0] == "captured" or selected_square[2] == "drop_target"):
                        if piece_idx >= len(main_board.captured_pieces[WHITE]):
                            # 空いている部分をクリックしてキャンセル
                            logger.debug("Cancelled captured piece selection by clicking empty space (White)")
                            selected_square = None
                            continue
                        elif piece_idx < len(main_board.captured_pieces[WHITE]) and main_board.player == WHITE:
                            # 別の持ち駒を選択
                            selected_square = ("captured", WHITE, piece_idx)
                            logger.debug(f"Selected captured piece: White, index {piece_idx}")
                            continue
                    if piece_idx < len(main_board.captured_pieces[WHITE]) and main_board.player == WHITE:
                        selected_square = ("captured", WHITE, piece_idx)
                        logger.debug(f"Selected captured piece: White, index {piece_idx}")
                        continue
                elif y > BOARD_SIZE + 100:  # 下部（黒の持ち駒エリア）
                    piece_idx = x // SQUARE_SIZE
                    if selected_square and (selected_square[0] == "captured" or selected_square[2] == "drop_target"):
                        if piece_idx >= len(main_board.captured_pieces[BLACK]):
                            # 空いている部分をクリックしてキャンセル
                            logger.debug("Cancelled captured piece selection by clicking empty space (Black)")
                            selected_square = None
                            continue
                        elif piece_idx < len(main_board.captured_pieces[BLACK]) and main_board.player == BLACK:
                            # 別の持ち駒を選択
                            selected_square = ("captured", BLACK, piece_idx)
                            logger.debug(f"Selected captured piece: Black, index {piece_idx}")
                            continue
                    if piece_idx < len(main_board.captured_pieces[BLACK]) and main_board.player == BLACK:
                        selected_square = ("captured", BLACK, piece_idx)
                        logger.debug(f"Selected captured piece: Black, index {piece_idx}")
                        continue
                
                # ボード内のクリック
                if 0 <= row < SIZE and 0 <= col < SIZE:
                    if selected_square is None:
                        # 通常の駒選択
                        if main_board.board[col][row] != EMPTY and fundam.PosNeg(main_board.board[col][row]) == main_board.player:
                            selected_square = (col, row)
                            logger.debug(f"Selected square: ({col}, {row})")
                    else:
                        if selected_square[0] == "captured":
                            player, idx = selected_square[1], selected_square[2]
                            piece = main_board.captured_pieces[player][idx]
                            if selected_square[1] == main_board.player:
                                # 1回目のクリックで配置先を選択
                                selected_square = (col, row, "drop_target", player, idx, piece)
                                logger.debug(f"Selected drop target: ({col}, {row})")
                            # 盤面の自分の駒をクリックしてキャンセル
                            if main_board.board[col][row] != EMPTY and fundam.PosNeg(main_board.board[col][row]) == main_board.player:
                                selected_square = (col, row)
                                logger.debug(f"Cancelled captured piece selection and selected square: ({col}, {row})")
                        elif len(selected_square) == 6 and selected_square[2] == "drop_target":
                            # 2回目のクリックで配置
                            target_col, target_row, _, player, idx, piece = selected_square
                            if (col, row) == (target_col, target_row):
                                logger.debug(f"Attempting drop: piece={piece} at ({col}, {row})")
                                if main_board.drop_piece(piece, col, row):
                                    logger.debug("Drop successful")
                                    selected_square = None
                                    move_made = True  # 移動が完了
                                else:
                                    logger.debug("Drop failed")
                                    selected_square = (target_col, target_row, "drop_target", player, idx, piece)
                            else:
                                # 別のマスを選択
                                selected_square = (col, row, "drop_target", player, idx, piece)
                                logger.debug(f"Selected new drop target: ({col}, {row})")
                            # 盤面の自分の駒をクリックしてキャンセル
                            if main_board.board[col][row] != EMPTY and fundam.PosNeg(main_board.board[col][row]) == main_board.player:
                                selected_square = (col, row)
                                logger.debug(f"Cancelled drop target selection and selected square: ({col}, {row})")
                        else:
                            # 通常の移動
                            fr_col, fr_row = selected_square
                            logger.debug(f"Attempting move: from ({fr_col}, {fr_row}) to ({col}, {row})")
                            piece = main_board.board[fr_col][fr_row]
                            if abs(piece) == PAWN and (row == 0 or row == 7):
                                promotion = get_promotion_choice(main_board, selected_square, clock)
                                if main_board.move(fr_col, fr_row, col, row, {'Q': Q, 'R': R, 'N': N, 'B': B}[promotion]):
                                    logger.debug(f"Move successful with promotion to {promotion}")
                                    selected_square = None
                                    move_made = True  # 移動が完了
                                else:
                                    logger.debug("Move failed")
                                    selected_square = None
                            else:
                                if main_board.move(fr_col, fr_row, col, row):
                                    logger.debug("Move successful")
                                    selected_square = None
                                    move_made = True  # 移動が完了
                                else:
                                    logger.debug("Move failed")
                                    selected_square = None
        
        # 移動が完了した直後にゲーム終了判定を行う
        if move_made:
            game_over = main_board.is_game_over()
            if game_over is not None:
                draw_game_over(main_board, clock)
                pygame.quit()
                sys.exit()
            move_made = False  # リセット

        screen.fill((255, 255, 255))
        draw_board(main_board, selected_square if isinstance(selected_square, tuple) and len(selected_square) in [2, 6] else None)
        draw_captured_pieces(main_board)
        
        turn_text = small_font.render(f"Turn: {'White' if main_board.player == WHITE else 'Black'}", True, (0, 0, 0))
        screen.blit(turn_text, (10, WINDOW_HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()