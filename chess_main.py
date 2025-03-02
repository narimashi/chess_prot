import pygame
import chess
import sys
import os

# 初期設定
pygame.init()
screen_size = 600
square_size = screen_size // 8
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("取った駒を使えるチェス")

# 色の設定
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)

# チェスボードの初期化
board = chess.Board()

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

# 駒画像の辞書を表示（デバッグ用）
print("読み込まれた駒画像:", piece_images.keys())

# チェスボードの描画
def draw_board(screen, board):
    for row in range(8):
        for col in range(8):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

    for square, piece in board.piece_map().items():
        row, col = divmod(square, 8)
        piece_key = f"{'w' if piece.color == chess.WHITE else 'b'}{piece.symbol().lower()}"
        if piece_key in piece_images:
            screen.blit(piece_images[piece_key], (col * square_size, row * square_size))
        else:
            print(f"駒画像が見つかりません: {piece_key}")

# メインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw_board(screen, board)
    pygame.display.flip()
