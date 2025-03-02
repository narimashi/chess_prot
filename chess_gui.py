import pygame
import sys

# 定数設定
SCREEN_SIZE = 640
GRID_SIZE = 8
SQUARE_SIZE = SCREEN_SIZE // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT_COLOR = (0, 0, 0)

# Pygame 初期化
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('持ち駒ルールのあるチェス')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

# 駒のテキスト表現 (白: 大文字, 黒: 小文字)
PIECES = {
    "P": "P", "N": "N", "B": "B", "R": "R", "Q": "Q", "K": "K",
    "p": "p", "n": "n", "b": "b", "r": "r", "q": "q", "k": "k"
}

# 仮の駒配置 (標準の初期配置)
board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]

selected_piece = None
selected_pos = None

# ボード描画関数
def draw_board(screen, board, selected_pos=None):
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = GREEN if (row + col) % 2 == 0 else WHITE
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)
            if selected_pos == (row, col):
                pygame.draw.rect(screen, RED, rect, 3)
            piece = board[row][col]
            if piece:
                text = font.render(piece, True, FONT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

# マウスクリック処理
def handle_mouse_click(pos, board):
    global selected_piece, selected_pos
    x, y = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
    if selected_piece is None:
        # 駒を選択
        selected_piece = board[y][x]
        selected_pos = (y, x) if selected_piece else None
    else:
        # 駒を移動 (駒がない場所にも移動可能)
        if selected_pos:
            board[selected_pos[0]][selected_pos[1]] = None
            board[y][x] = selected_piece
        selected_piece = None
        selected_pos = None

# メインループ
def main():
    global selected_pos
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(pygame.mouse.get_pos(), board)

        draw_board(screen, board, selected_pos)
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
