# src/playmode.py
import pygame
import sys
import os
import logging
import random  # ボット用に追加

from config import *
import board
import IO
import fundam

# ログ設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Pygameの初期化
pygame.init()
pygame.mixer.init()  # サウンド用のミキサー初期化

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
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 149, 237)
GRADIENT_TOP = (70, 130, 180)
GRADIENT_BOTTOM = (30, 60, 114)

# 駒の画像をロードし、スケーリング
try:
    piece_images = {
        WHITE * PAWN: pygame.transform.scale(pygame.image.load('assets/pieces/wp.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
        WHITE * ROOK: pygame.transform.scale(pygame.image.load('assets/pieces/wr.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
        WHITE * KNIGHT: pygame.transform.scale(pygame.image.load('assets/pieces/wn.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
        WHITE * BISHOP: pygame.transform.scale(pygame.image.load('assets/pieces/wb.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
        WHITE * QUEEN: pygame.transform.scale(pygame.image.load('assets/pieces/wq.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
        WHITE * KING: pygame.transform.scale(pygame.image.load('assets/pieces/wk.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
        BLACK * PAWN: pygame.transform.scale(pygame.image.load('assets/pieces/bp.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
        BLACK * ROOK: pygame.transform.scale(pygame.image.load('assets/pieces/br.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
        BLACK * KNIGHT: pygame.transform.scale(pygame.image.load('assets/pieces/bn.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
        BLACK * BISHOP: pygame.transform.scale(pygame.image.load('assets/pieces/bb.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
        BLACK * QUEEN: pygame.transform.scale(pygame.image.load('assets/pieces/bq.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
        BLACK * KING: pygame.transform.scale(pygame.image.load('assets/pieces/bk.png').convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE)),
    }
except FileNotFoundError as e:
    logger.error(f"Failed to load piece images: {e}")
    print("Error: Could not load piece images. Please ensure the 'assets/pieces/' directory exists and contains all required images.")
    sys.exit(1)

# サウンドの読み込み
try:
    move_sound = pygame.mixer.Sound('assets/sounds/move_sound.mp3')
    win_sound = pygame.mixer.Sound('assets/sounds/win_sound.mp3')
    win_sound.set_volume(0.8)  # 勝利時のサウンド音量を0.8に設定
except FileNotFoundError as e:
    logger.warning(f"Failed to load sound files: {e}. Sound effects will be disabled.")
    move_sound = None
    win_sound = None

# カスタムフォントの読み込み
try:
    font_path = os.path.join("../Roboto-Regular.ttf")  # ルートディレクトリにあるフォント
    title_font = pygame.font.Font(font_path, 48)
    button_font = pygame.font.Font(font_path, 36)
    small_font = pygame.font.Font(font_path, 24)
except FileNotFoundError:
    logger.warning("Roboto-Regular.ttf not found. Falling back to default font.")
    title_font = pygame.font.SysFont(None, 48)
    button_font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)

def draw_gradient_background(surface, top_color, bottom_color):
    height = surface.get_height()
    gradient = pygame.Surface((1, height), pygame.SRCALPHA)
    for y in range(height):
        r = top_color[0] + (bottom_color[0] - top_color[0]) * y / height
        g = top_color[1] + (bottom_color[1] - top_color[1]) * y / height
        b = top_color[2] + (bottom_color[2] - top_color[2]) * y / height
        gradient.set_at((0, y), (int(r), int(g), int(b)))
    surface.blit(pygame.transform.scale(gradient, surface.get_size()), (0, 0))

def draw_button(surface, text, font, x, y, width, height, color, hover_color, mouse_pos):
    button_rect = pygame.Rect(x, y, width, height)
    is_hovered = button_rect.collidepoint(mouse_pos)
    button_color = hover_color if is_hovered else color
    
    shadow_surface = pygame.Surface((width + 4, height + 4), pygame.SRCALPHA)
    shadow_surface.fill((0, 0, 0, 50))
    surface.blit(shadow_surface, (x + 2, y + 2))
    
    pygame.draw.rect(surface, button_color, button_rect, 0, 5)
    pygame.draw.rect(surface, (255, 255, 255), button_rect, 2, 5)
    
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)
    
    return button_rect

# メニュー画面
def main_menu():
    clock = pygame.time.Clock()
    button_width = 300
    button_height = 50
    button_spacing = 20
    total_height = (button_height + button_spacing) * 4 - button_spacing
    start_y = (WINDOW_HEIGHT - total_height) // 2
    
    while True:
        draw_gradient_background(screen, GRADIENT_TOP, GRADIENT_BOTTOM)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # ボタンの描画
        online_button = draw_button(
            screen,
            "オンライン対戦",
            button_font,
            (WINDOW_WIDTH - button_width) // 2,
            start_y,
            button_width,
            button_height,
            BUTTON_COLOR,
            BUTTON_HOVER_COLOR,
            mouse_pos
        )
        bot_button = draw_button(
            screen,
            "ボット対戦",
            button_font,
            (WINDOW_WIDTH - button_width) // 2,
            start_y + (button_height + button_spacing),
            button_width,
            button_height,
            BUTTON_COLOR,
            BUTTON_HOVER_COLOR,
            mouse_pos
        )
        friend_button = draw_button(
            screen,
            "フレンド対戦",
            button_font,
            (WINDOW_WIDTH - button_width) // 2,
            start_y + 2 * (button_height + button_spacing),
            button_width,
            button_height,
            BUTTON_COLOR,
            BUTTON_HOVER_COLOR,
            mouse_pos
        )
        tournament_button = draw_button(
            screen,
            "大会",
            button_font,
            (WINDOW_WIDTH - button_width) // 2,
            start_y + 3 * (button_height + button_spacing),
            button_width,
            button_height,
            BUTTON_COLOR,
            BUTTON_HOVER_COLOR,
            mouse_pos
        )
        settings_button = draw_button(
            screen,
            "設定",
            button_font,
            WINDOW_WIDTH - 210,
            WINDOW_HEIGHT - 90,
            200,
            50,
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
                if bot_button.collidepoint(event.pos):
                    botmode_gui()  # ボット対戦を開始
                # 他のボタンは未実装（クリックしても何も起こらない）

        clock.tick(60)

def draw_board(main_board, selected_square=None):
    for row in range(SIZE):
        for col in range(SIZE):
            color = WHITE_COLOR if (row + col) % 2 == 0 else BLACK_COLOR
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE + 100, SQUARE_SIZE, SQUARE_SIZE))
            piece = main_board.board[col][row]
            if piece != EMPTY:
                screen.blit(piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE + 100))
    
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
    
    for i, piece in enumerate(white_captured):
        abs_piece = abs(piece)
        displayed_piece = WHITE * abs_piece if piece < 0 else BLACK * abs_piece
        screen.blit(piece_images[displayed_piece], (i * SQUARE_SIZE, 10))
    
    for i, piece in enumerate(black_captured):
        abs_piece = abs(piece)
        displayed_piece = BLACK * abs_piece if piece > 0 else WHITE * abs_piece
        screen.blit(piece_images[displayed_piece], (i * SQUARE_SIZE, WINDOW_HEIGHT - SQUARE_SIZE - 10))
    
    if selected_square and selected_square[0] == "captured":
        player, idx = selected_square[1], selected_square[2]
        highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        highlight.fill(HIGHLIGHT_COLOR)
        if player == WHITE:
            screen.blit(highlight, (idx * SQUARE_SIZE, 10))
        else:
            screen.blit(highlight, (idx * SQUARE_SIZE, WINDOW_HEIGHT - SQUARE_SIZE - 10))

def get_promotion_choice(main_board, selected_square, clock):
    choices = ['Q', 'R', 'N', 'B']
    buttons = []
    button_width = 150
    button_height = 50
    button_spacing = 10
    total_height = (button_height + button_spacing) * len(choices) - button_spacing
    start_y = (WINDOW_HEIGHT - total_height) // 2
    
    while True:
        screen.fill((255, 255, 255))
        draw_board(main_board, selected_square if isinstance(selected_square, tuple) and len(selected_square) == 2 else None)
        draw_captured_pieces(main_board)
        turn_text = small_font.render(f"Turn: {'White' if main_board.player == WHITE else 'Black'}", True, (0, 0, 0))
        screen.blit(turn_text, (10, WINDOW_HEIGHT - 40))
        
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        title_text = title_font.render("Choose Promotion", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, start_y - 60))
        screen.blit(title_text, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
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

def confirm_resign(main_board, clock):
    choices = ['Yes', 'No']
    buttons = []
    button_width = 150
    button_height = 50
    button_spacing = 10
    total_height = (button_height + button_spacing) * len(choices) - button_spacing
    start_y = (WINDOW_HEIGHT - total_height) // 2
    
    while True:
        screen.fill((255, 255, 255))
        draw_board(main_board)
        draw_captured_pieces(main_board)
        turn_text = small_font.render(f"Turn: {'White' if main_board.player == WHITE else 'Black'}", True, (0, 0, 0))
        screen.blit(turn_text, (10, WINDOW_HEIGHT - 40))
        
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        title_text = title_font.render("Resign?", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, start_y - 60))
        screen.blit(title_text, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        buttons.clear()
        for i, choice in enumerate(choices):
            y = start_y + i * (button_height + button_spacing)
            button_rect = draw_button(
                screen,
                choice,
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
                        return choice == 'Yes'
        
        clock.tick(60)

def draw_game_over(main_board, clock, resign=False):
    result = main_board.is_game_over()
    message = ""
    if result == WHITE:
        message = "White Wins!"
    elif result == BLACK:
        message = "Black Wins!"
    elif result == EMPTY:
        message = "Draw by Stalemate!"
    elif resign:
        winner = -main_board.player  # 投了したプレイヤーの相手が勝者
        message = f"{'White' if winner == WHITE else 'Black'} Wins by Resignation!"

    if not message:
        return

    # 勝利時にサウンドを再生
    if win_sound:
        win_sound.play()

    alpha = 0
    fade_speed = 5
    button_width = 200
    button_height = 50
    exit_button = None
    
    while True:
        draw_gradient_background(screen, GRADIENT_TOP, GRADIENT_BOTTOM)
        
        text_surface = title_font.render(message, True, TEXT_COLOR)
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        screen.blit(text_surface, text_rect)
        
        if alpha < 255:
            alpha += fade_speed
            alpha = min(alpha, 255)
        
        mouse_pos = pygame.mouse.get_pos()
        
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

# ボットの手をランダムに選択する関数
def get_bot_move(main_board):
    legal_moves = []
    # ボード上の駒を移動する場合
    for fr_col in range(SIZE):
        for fr_row in range(SIZE):
            piece = main_board.board[fr_col][fr_row]
            if piece != EMPTY and fundam.PosNeg(piece) == main_board.player:
                for to_col in range(SIZE):
                    for to_row in range(SIZE):
                        if main_board.can_move(fr_col, fr_row, to_col, to_row):
                            legal_moves.append((fr_col, fr_row, to_col, to_row))
    
    # 持ち駒を配置する場合
    captured = main_board.captured_pieces[main_board.player]
    for idx, piece in enumerate(captured):
        for col in range(SIZE):
            for row in range(SIZE):
                if main_board.can_drop(piece, col, row):
                    legal_moves.append(("captured", idx, col, row))
    
    if legal_moves:
        return random.choice(legal_moves)
    return None

def botmode_gui():
    main_board = board.Board()
    selected_square = None
    clock = pygame.time.Clock()
    move_made = False
    
    # 棋譜ファイルの初期化
    record = open(MAINRECADDRESS, 'w')
    record.close()
    record = open(SUBRECADDRESS, 'w')
    record.close()

    while True:
        # プレイヤーのターン（白）
        if main_board.player == WHITE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col = x // SQUARE_SIZE
                    row = (y - 100) // SQUARE_SIZE
                    
                    # 持ち駒エリアのクリック
                    if y < 100:  # 白の持ち駒エリア
                        piece_idx = x // SQUARE_SIZE
                        if selected_square and (selected_square[0] == "captured" or selected_square[2] == "drop_target"):
                            if piece_idx >= len(main_board.captured_pieces[WHITE]):
                                logger.debug("Cancelled captured piece selection by clicking empty space (White)")
                                selected_square = None
                                continue
                            elif piece_idx < len(main_board.captured_pieces[WHITE]) and main_board.player == WHITE:
                                selected_square = ("captured", WHITE, piece_idx)
                                logger.debug(f"Selected captured piece: White, index {piece_idx}")
                                continue
                        if piece_idx < len(main_board.captured_pieces[WHITE]) and main_board.player == WHITE:
                            selected_square = ("captured", WHITE, piece_idx)
                            logger.debug(f"Selected captured piece: White, index {piece_idx}")
                            continue
                    elif y > BOARD_SIZE + 100:  # 黒の持ち駒エリア（プレイヤーは操作しない）
                        continue
                    
                    # ボード内のクリック
                    if 0 <= row < SIZE and 0 <= col < SIZE:
                        if selected_square is None:
                            if main_board.board[col][row] != EMPTY and fundam.PosNeg(main_board.board[col][row]) == main_board.player:
                                selected_square = (col, row)
                                logger.debug(f"Selected square: ({col}, {row})")
                        else:
                            if selected_square[0] == "captured":
                                player, idx = selected_square[1], selected_square[2]
                                piece = main_board.captured_pieces[player][idx]
                                if selected_square[1] == main_board.player:
                                    selected_square = (col, row, "drop_target", player, idx, piece)
                                    logger.debug(f"Selected drop target: ({col}, {row})")
                                if main_board.board[col][row] != EMPTY and fundam.PosNeg(main_board.board[col][row]) == main_board.player:
                                    selected_square = (col, row)
                                    logger.debug(f"Cancelled captured piece selection and selected square: ({col}, {row})")
                            elif len(selected_square) == 6 and selected_square[2] == "drop_target":
                                target_col, target_row, _, player, idx, piece = selected_square
                                if (col, row) == (target_col, target_row):
                                    logger.debug(f"Attempting drop: piece={piece} at ({col}, {row})")
                                    if main_board.drop_piece(piece, col, row):
                                        logger.debug("Drop successful")
                                        if move_sound:
                                            move_sound.play()
                                        selected_square = None
                                        move_made = True
                                    else:
                                        logger.debug("Drop failed")
                                        selected_square = (target_col, target_row, "drop_target", player, idx, piece)
                                else:
                                    selected_square = (col, row, "drop_target", player, idx, piece)
                                    logger.debug(f"Selected new drop target: ({col}, {row})")
                                if main_board.board[col][row] != EMPTY and fundam.PosNeg(main_board.board[col][row]) == main_board.player:
                                    selected_square = (col, row)
                                    logger.debug(f"Cancelled drop target selection and selected square: ({col}, {row})")
                            else:
                                fr_col, fr_row = selected_square
                                logger.debug(f"Attempting move: from ({fr_col}, {fr_row}) to ({col}, {row})")
                                piece = main_board.board[fr_col][fr_row]
                                if abs(piece) == PAWN and (row == 0 or row == 7):
                                    promotion = get_promotion_choice(main_board, selected_square, clock)
                                    if main_board.move(fr_col, fr_row, col, row, {'Q': Q, 'R': R, 'N': N, 'B': B}[promotion]):
                                        logger.debug(f"Move successful with promotion to {promotion}")
                                        if move_sound:
                                            move_sound.play()
                                        selected_square = None
                                        move_made = True
                                    else:
                                        logger.debug("Move failed")
                                        selected_square = None
                                else:
                                    if main_board.move(fr_col, fr_row, col, row):
                                        logger.debug("Move successful")
                                        if move_sound:
                                            move_sound.play()
                                        selected_square = None
                                        move_made = True
                                    else:
                                        logger.debug("Move failed")
                                        selected_square = None
                    
                    # 投了ボタンのクリック処理
                    resign_button = pygame.Rect(WINDOW_WIDTH - 210, WINDOW_HEIGHT - 90, 200, 50)
                    if resign_button.collidepoint(event.pos):
                        logger.info(f"{main_board.player == WHITE and 'White' or 'Black'} initiated resign confirmation")
                        if confirm_resign(main_board, clock):
                            logger.info(f"{main_board.player == WHITE and 'White' or 'Black'} resigned!")
                            main_board.s = "1-0" if main_board.player == BLACK else "0-1"
                            main_board.record(MAINRECADDRESS)
                            draw_game_over(main_board, clock, resign=True)
                            return  # メニューに戻る
        
        # ボットのターン（黒）
        else:
            bot_move = get_bot_move(main_board)
            if bot_move:
                if bot_move[0] == "captured":
                    _, idx, col, row = bot_move
                    piece = main_board.captured_pieces[main_board.player][idx]
                    logger.debug(f"Bot attempts drop: piece={piece} at ({col}, {row})")
                    if main_board.drop_piece(piece, col, row):
                        logger.debug("Bot drop successful")
                        if move_sound:
                            move_sound.play()
                        move_made = True
                else:
                    fr_col, fr_row, to_col, to_row = bot_move
                    logger.debug(f"Bot attempts move: from ({fr_col}, {fr_row}) to ({to_col}, {to_row})")
                    piece = main_board.board[fr_col][fr_row]
                    if abs(piece) == PAWN and (to_row == 0 or to_row == 7):
                        # ボットはランダムにプロモーションを選択
                        promotion = random.choice(['Q', 'R', 'N', 'B'])
                        if main_board.move(fr_col, fr_row, to_col, to_row, {'Q': Q, 'R': R, 'N': N, 'B': B}[promotion]):
                            logger.debug(f"Bot move successful with promotion to {promotion}")
                            if move_sound:
                                move_sound.play()
                            move_made = True
                    else:
                        if main_board.move(fr_col, fr_row, to_col, to_row):
                            logger.debug("Bot move successful")
                            if move_sound:
                                move_sound.play()
                            move_made = True

        if move_made:
            game_over = main_board.is_game_over()
            if game_over is not None:
                draw_game_over(main_board, clock)
                return  # メニューに戻る
            move_made = False

        screen.fill((255, 255, 255))
        draw_board(main_board, selected_square if isinstance(selected_square, tuple) and len(selected_square) in [2, 6] else None)
        draw_captured_pieces(main_board)
        
        turn_text = small_font.render(f"Turn: {'White' if main_board.player == WHITE else 'Black'}", True, (0, 0, 0))
        screen.blit(turn_text, (10, WINDOW_HEIGHT - 40))
        
        mouse_pos = pygame.mouse.get_pos()
        resign_button = draw_button(
            screen,
            "Resign",
            button_font,
            WINDOW_WIDTH - 210,
            WINDOW_HEIGHT - 90,
            200,
            50,
            BUTTON_COLOR,
            BUTTON_HOVER_COLOR,
            mouse_pos
        )
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()  # メニュー画面から開始