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

def validate_coords_string(coord: str) -> bool:
    """Returns true if coord string is valid. EG. e1 is valid, w9 is not."""
    if len(coord) != 2: return False
    letter = "abcdefgh"
    number = "12345678"
    if coord[0] not in letter: return False
    if coord[1] not in number: return False
    return True

def coords_stringify(x: int, y: int) -> str:
    """Returns a human readable coordinate, a1 to h8."""
    conv = "abcdefgh"
    if out_of_bounds(x, y):
        raise ValueError(f"Coordinates out of bounds! Given: ({x}, {y})")
    return conv[x] + str(y+1)

def coords_string_to_tuple(coord: str) -> tuple:
    """Converts human readable coordinates (a1, g3, ...) to x, y tuple."""
    if not validate_coords_string(coord):
        raise ValueError("The given coordinates are not valid! Given: " + coord)
    conv = "abcdefgh"
    return (conv.index(coord[0]), int(coord[1]))

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
    """Sets up the standard chess game initial state."""
    # Reminder: (0, 0) is a1
    for x in range(WIDTH):
        insert_piece(Piece(PieceType.PAWN, PieceColor.WHITE), x, 1)
        insert_piece(Piece(PieceType.PAWN, PieceColor.BLACK), x, 6)
    # White side
    insert_piece(Piece(PieceType.ROOK, PieceColor.WHITE), 0, 0)
    insert_piece(Piece(PieceType.KNIGHT, PieceColor.WHITE), 1, 0)
    insert_piece(Piece(PieceType.BISHOP, PieceColor.WHITE), 2, 0)
    insert_piece(Piece(PieceType.QUEEN, PieceColor.WHITE), 3, 0)
    insert_piece(Piece(PieceType.KING, PieceColor.WHITE), 4, 0)
    insert_piece(Piece(PieceType.BISHOP, PieceColor.WHITE), 5, 0)
    insert_piece(Piece(PieceType.KNIGHT, PieceColor.WHITE), 6, 0)
    insert_piece(Piece(PieceType.ROOK, PieceColor.WHITE), 7, 0)
    # Black side
    insert_piece(Piece(PieceType.ROOK, PieceColor.BLACK), 0, 7)
    insert_piece(Piece(PieceType.KNIGHT, PieceColor.BLACK), 1, 7)
    insert_piece(Piece(PieceType.BISHOP, PieceColor.BLACK), 2, 7)
    insert_piece(Piece(PieceType.QUEEN, PieceColor.BLACK), 3, 7)
    insert_piece(Piece(PieceType.KING, PieceColor.BLACK), 4, 7)
    insert_piece(Piece(PieceType.BISHOP, PieceColor.BLACK), 5, 7)
    insert_piece(Piece(PieceType.KNIGHT, PieceColor.BLACK), 6, 7)
    insert_piece(Piece(PieceType.ROOK, PieceColor.BLACK), 7, 7)

# Accepts input in xy-xy format. (source-destination)
def parse_move(move: str) -> list[tuple]:
    """Parses moves in 'xy-xy' format. Returns [(x,y), (x,y)]."""
    if len(move) is not 5:
        raise ValueError("Incorrect string length for move. Given: " + move)
    coords = move.split("-")
    if len(coords) != 2:
        raise ValueError("Incorrectly delimited! Given: " + move)
    if not validate_coords_string(coords[0]):
        raise ValueError("First coordinate formatting error. Given: " + coords[0])
    if not validate_coords_string(coords[1]):
        raise ValueError("Second coordinate formatting error. Given: " + coords[1])
    # String parsing done, convert coords for internal use
    return [coords_string_to_tuple(coords[0]), coords_string_to_tuple(coords[1])]

def is_move_legal(move: str) -> bool:
    coords = parse_move(move)

init_board()
standard_board_setup()
print(stringify_board())

while True:
    eto = input()
    print(eto)