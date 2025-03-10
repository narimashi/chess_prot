from logging import getLogger, StreamHandler, FileHandler, DEBUG, INFO, WARNING, ERROR, CRITICAL, Formatter
import os

# ディレクトリ作成
os.makedirs('data', exist_ok=True)

# LOGGER SETTINGS
DEFAULT_LOG_ADDRESS = 'data/log.txt'
DEFAULT_FORMAT = Formatter('%(asctime)s - %(levelname)s - logger:%(name)s - %(filename)s - L%(lineno)d - %(funcName)s - %(message)s')

def setLogger(name='default', *, level=INFO, fhandler=None, shandler=None, fhandler_level=DEBUG, shandler_level=CRITICAL, filemode='w', filename=DEFAULT_LOG_ADDRESS, fhandler_format=DEFAULT_FORMAT, shandler_format=DEFAULT_FORMAT):
    logger = getLogger(name)
    logger.setLevel(level)

    fhandler = fhandler or FileHandler(filename, mode=filemode, encoding='utf-8')
    fhandler.setLevel(fhandler_level)
    fhandler.setFormatter(fhandler_format)
    logger.addHandler(fhandler)

    shandler = shandler or StreamHandler()
    shandler.setLevel(shandler_level)
    shandler.setFormatter(shandler_format)
    logger.addHandler(shandler)

    return logger

# record files
MAINRECADDRESS = 'data/mainrecord.txt'
SUBRECADDRESS = 'data/subrecord.txt'

# board size
SIZE = 8
OVERSIZE = SIZE * SIZE

# for index
FILE = 0
RANK = 1
a, b, c, d, e, f, g, h = 1, 2, 3, 4, 5, 6, 7, 8

WHITE = 1
BLACK = -1

EMPTY = 0
P = PAWN = 1
R = ROOK = 2
N = KNIGHT = 3
B = BISHOP = 4
Q = QUEEN = 5
K = KING = 6