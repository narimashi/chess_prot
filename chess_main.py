import pygame
import chess
import sys
import os

# 初期設定
pygame.init()
screen_size = 800  # 横幅を広げて持ち駒表示用スペースを確保
board_size = 600
square_size = board_size // 8
screen = pygame.display.set_mode((screen_size, board_size))
pygame.display.set_caption("取った駒を使えるチェス")

# 色の設定
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
HIGHLIGHT_COLOR = (100, 200, 100, 100)
SIDE_PANEL_COLOR = (50, 50, 50)

# チェスボードの初期化
board = chess.Board()
captured_pieces = {chess.WHITE: [], chess.BLACK: []}
selected_square = None
valid_moves = []
selected_piece_from_captured = None

# 画像フォルダのパス
current_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(current_dir, 'assets')

# 駒画像の読み込み
piece_images = {}
pieces = ['p', 'r', 'n', 'b', 'q', 'k']
colors = ['w', 'b']

for color in colors:
    for piece in pieces:
        filename = os.path.join(image_dir, f"{color}{piece}.png")
        try:
            image = pygame.image.load(filename)
            piece_images[color + piece] = pygame.transform.scale(image, (square_size, square_size))
        except FileNotFoundError:
            print(f"画像ファイルが見つかりません: {filename}")

# 描画関数
def draw_board(screen, board, valid_moves=[]):
    screen.fill(SIDE_PANEL_COLOR)
    
    # チェスボードの描画
    for row in range(8):
        for col in range(8):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

            if chess.square(col, row) in valid_moves:
                highlight_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                highlight_surface.fill(HIGHLIGHT_COLOR)
                screen.blit(highlight_surface, (col * square_size, row * square_size))

    for square, piece in board.piece_map().items():
        row, col = divmod(square, 8)
        piece_key = f"{'w' if piece.color == chess.WHITE else 'b'}{piece.symbol().lower()}"
        if piece_key in piece_images:
            screen.blit(piece_images[piece_key], (col * square_size, row * square_size))

    draw_captured_pieces(screen)

# 持ち駒の表示
def draw_captured_pieces(screen):
    offset_x = board_size + 20
    offset_y = 20
    for color, pieces in captured_pieces.items():
        y_offset = offset_y
        for piece in pieces:
            piece_key = f"{'w' if color == chess.WHITE else 'b'}{piece.lower()}"
            if piece_key in piece_images:
                screen.blit(piece_images[piece_key], (offset_x, y_offset))
                y_offset += square_size + 10
        offset_x += square_size + 20

# マウス位置からマスを取得
def get_square_under_mouse():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    row, col = mouse_y // square_size, mouse_x // square_size
    if 0 <= row < 8 and 0 <= col < 8:
        return chess.square(col, row)
    return None

# メインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            square = get_square_under_mouse()
            if square is not None:
                piece = board.piece_at(square)
                
                # 駒の選択
                if piece and piece.color == board.turn:
                    selected_square = square
                    valid_moves = [move.to_square for move in board.legal_moves if move.from_square == square]
                    print("選択した駒の移動可能なマス:", [chess.square_name(sq) for sq in valid_moves])
                
                # 駒の移動と持ち駒追加
                elif selected_square is not None and square in valid_moves:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        # 駒を取る場合、持ち駒に追加する
                        if board.piece_at(square):
                            captured_piece = board.piece_at(square)
                            captured_pieces[captured_piece.color].append(captured_piece.symbol().lower())
                        board.push(move)
                    selected_square = None
                    valid_moves = []

        elif event.type == pygame.KEYDOWN:
            # Zキーで取り消し (Undo)
            if event.key == pygame.K_z and len(board.move_stack) > 0:
                last_move = board.pop()
                print("1手戻しました")
            
            # Rキーでリセット
            elif event.key == pygame.K_r:
                board.reset()
                captured_pieces = {chess.WHITE: [], chess.BLACK: []}
                selected_square = None
                valid_moves = []
                selected_piece_from_captured = None
                print("ゲームをリセットしました")

    draw_board(screen, board, valid_moves)
    pygame.display.flip()
