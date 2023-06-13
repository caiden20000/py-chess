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



def init_board(width: int, height: int):
    """Initialize the board as empty."""
    global board
    board = {}
    for x in range(1, width+1):
        for y in range(1, height+1):
            insert_piece(None, x, y)

def get_piece(x: int, y: int) -> Piece | None:
    """Returns the piece at a given coordinate. Returns None if no piece or out of bounds."""
    if out_of_bounds(x, y):
        return None
    return board[x*10 + y]

def insert_piece(piece: Piece | None, x: int, y: int) -> bool:
    """Insert a piece at the given coordinates. Returns true if successful."""
    if out_of_bounds(x, y):
        return False
    board[x*10 + y] = piece
    return True

def out_of_bounds(x: int, y: int) -> bool:
    """Returns True if x, y is outside the board"""
    return 0 > x or x >= WIDTH or 0 > y or y >= HEIGHT

def stringify_board() -> str:
    row_sep = "+--"*WIDTH + "+"
    result = ""
    result += row_sep
    for y in range(HEIGHT):
        result += "|"
        for x in range(WIDTH):
            get_piece()