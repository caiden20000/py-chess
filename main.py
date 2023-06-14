from enum import Enum

# Chess board is from a1 to h8
# Inner coords replace letter with number: 00 to 77

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
    def stringify(self) -> str:
        """Returns a string representation of the piece. Should be str of length 3."""
        return self.color.value + self.type.value.upper() + self.color.value



def init_board(width: int = 8, height: int = 8):
    """Initialize the board as empty."""
    global board
    board = {}
    for x in range(width):
        for y in range(height):
            insert_piece(None, x, y)

def _board_key(x: int, y: int) -> str:
    return str(x*10 + y)

def get_piece(x: int, y: int) -> Piece | None:
    """Returns the piece at a given coordinate. Returns None if no piece or out of bounds."""
    if out_of_bounds(x, y):
        return None
    return board[_board_key(x, y)]

def insert_piece(piece: Piece | None, x: int, y: int) -> bool:
    """Insert a piece at the given coordinates. Returns true if successful."""
    if out_of_bounds(x, y):
        return False
    board[_board_key(x, y)] = piece
    return True

def out_of_bounds(x: int, y: int) -> bool:
    """Returns True if x, y is outside the board"""
    return 0 > x or x >= WIDTH or 0 > y or y >= HEIGHT

def stringify_board(show_coords: bool = False) -> str:
    """Returns the string representation of the board. For UI usage."""
    row_sep = "+---"*WIDTH + "+\n"
    result = row_sep
    for y in range(HEIGHT):
        result += "|"
        for x in range(WIDTH):
            piece = get_piece(x, y)
            if piece is None:
                result += "   "
            else:
                result += get_piece(x, y).stringify()
            result += "|"
        result += "\n" + row_sep
    return result

def standard_board_setup():
    pass

init_board()
print(stringify_board())
