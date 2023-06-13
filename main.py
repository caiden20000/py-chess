from enum import Enum

# Chess board is from a1 to h8
# Inner coords replace letter with number: 11 to 88

WIDTH = 8
HEIGHT = 8
# Represents an empty space on the board
EMPTY_SPACE = "0"

# Board is dict
board = {}

class PieceColor(Enum):
    """Enum to represent a chess piece color."""
    BLACK = "b"
    WHITE = "w"

class PieceType(Enum):
    """Enum to represent a chess piece type."""
    PAWN = "p"
    ROOK = "r"
    KNIGHT = "n"
    BISHOP = "b"
    QUEEN = "q"
    KING = "k"

class Piece:
    """Class to represent a chess piece."""
    def __init__(self, piece_type: PieceType, color: PieceColor):
        self.type = piece_type
        self.color = color



def init_board(width, height):
    """Initialize the board as empty."""
    global board
    board = {}
    for x in range(1, width+1):
        for y in range(1, height+1):
            insert_piece(None, x, y)

def get_piece(x, y) -> Piece | None:
    """Returns the piece at a given coordinate"""
    return board[x*10 + y]

def insert_piece(piece: Piece | None, x, y):
    """Insert a piece at the given coordinates."""
    board[x*10 + y] = piece

