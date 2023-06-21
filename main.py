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

class Coords:
    MIN_WIDTH = 0
    MAX_WIDTH = 7
    MIN_HEIGHT = 0
    MAX_HEIGHT = 7
    LETTERS = "abcdefgh"
    NUMBERS = "12345678"
    def __init__(self, x: int = 0, y: int = 0, string: str = ""):
        if string == "":
            self.x = x
            self.y = y
            self.out_of_bounds(raise_err = True)
        else:
            self.set_by_string(string)
    @staticmethod
    def validate_str(coords: str, raise_err: bool = False) -> bool:
        """Returns true if coord string is valid. EG. e1 is valid, w9 is not."""
        if len(coords) != 2 or coords[0] not in Coords.LETTERS or coords[1] not in Coords.NUMBERS:
            if raise_err:
                raise ValueError("The given coordinates are not valid! Given: " + coords)
            return False
        return True
    def out_of_bounds(self, raise_err: bool = False) -> bool:
        oob = self.x < self.MIN_WIDTH \
            or self.x > self.MAX_WIDTH \
            or self.y < self.MIN_HEIGHT \
            or self.y > self.MAX_HEIGHT
        if oob and raise_err:
            raise ValueError(f"Coordinates out of bounds! Given: ({self.x}, {self.y})")
        return oob
    def get_string(self) -> str:
        return Coords.LETTERS[self.x] + Coords.NUMBERS[self.y]
    def set_by_string(self, string):
        self.validate_str(string, raise_err = True)
        self.x = Coords.NUMBERS.index(string[0])
        self.y = Coords.LETTERS.index(string[1])
    def to_board_key(self):
        return str(self.x*10 + self.y)

# TODO: Add Coords object to piece
# TODO: Change board from containing strings to containing pieces

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
            insert_piece(None, Coords(x, y))

def get_piece(coords: Coords) -> Piece | None:
    """Returns the piece at a given coordinate. Returns None if no piece or out of bounds."""
    if coords.out_of_bounds():
        return None
    return board[coords.to_board_key()]

def insert_piece(piece: Piece | None, coords: Coords) -> bool:
    """Insert a piece at the given coordinates. Returns true if successful."""
    if coords.out_of_bounds():
        return False
    board[coords.to_board_key()] = piece
    return True

def stringify_board(show_coords: bool = False) -> str:
    """Returns the string representation of the board. For UI usage."""
    row_sep = "+---"*WIDTH + "+\n"
    result = row_sep
    for y in range(HEIGHT):
        result += "|"
        for x in range(WIDTH):
            piece = get_piece(Coords(x, y))
            if piece is None:
                result += "   "
            else:
                result += get_piece(Coords(x, y)).stringify()
            result += "|"
        result += "\n" + row_sep
    return result

def standard_board_setup():
    """Sets up the standard chess game initial state."""
    # Reminder: (0, 0) is a1
    for x in range(WIDTH):
        insert_piece(Piece(PieceType.PAWN, PieceColor.WHITE), Coords(x, 1))
        insert_piece(Piece(PieceType.PAWN, PieceColor.BLACK), Coords(x, 6))
    # White side
    insert_piece(Piece(PieceType.ROOK, PieceColor.WHITE), Coords(0, 0))
    insert_piece(Piece(PieceType.KNIGHT, PieceColor.WHITE), Coords(1, 0))
    insert_piece(Piece(PieceType.BISHOP, PieceColor.WHITE), Coords(2, 0))
    insert_piece(Piece(PieceType.QUEEN, PieceColor.WHITE), Coords(3, 0))
    insert_piece(Piece(PieceType.KING, PieceColor.WHITE), Coords(4, 0))
    insert_piece(Piece(PieceType.BISHOP, PieceColor.WHITE), Coords(5, 0))
    insert_piece(Piece(PieceType.KNIGHT, PieceColor.WHITE), Coords(6, 0))
    insert_piece(Piece(PieceType.ROOK, PieceColor.WHITE), Coords(7, 0))
    # Black side
    insert_piece(Piece(PieceType.ROOK, PieceColor.BLACK), Coords(0, 7))
    insert_piece(Piece(PieceType.KNIGHT, PieceColor.BLACK), Coords(1, 7))
    insert_piece(Piece(PieceType.BISHOP, PieceColor.BLACK), Coords(2, 7))
    insert_piece(Piece(PieceType.QUEEN, PieceColor.BLACK), Coords(3, 7))
    insert_piece(Piece(PieceType.KING, PieceColor.BLACK), Coords(4, 7))
    insert_piece(Piece(PieceType.BISHOP, PieceColor.BLACK), Coords(5, 7))
    insert_piece(Piece(PieceType.KNIGHT, PieceColor.BLACK), Coords(6, 7))
    insert_piece(Piece(PieceType.ROOK, PieceColor.BLACK), Coords(7, 7))

# Accepts input in xy-xy format. (source-destination)
def parse_move(move: str) -> list[Coords]:
    """Parses moves in 'xy-xy' format. Returns [(x,y), (x,y)]."""
    if len(move) is not 5:
        raise ValueError("Incorrect string length for move. Given: " + move)
    coords = move.split("-")
    if len(coords) != 2:
        raise ValueError("Incorrectly delimited! Given: " + move)
    if not Coords.validate_str(coords[0]):
        raise ValueError("First coordinate formatting error. Given: " + coords[0])
    if not Coords.validate_str(coords[1]):
        raise ValueError("Second coordinate formatting error. Given: " + coords[1])
    # String parsing done, convert coords for internal use
    return [Coords(string = coords[0]), Coords(string = coords[1])]

def is_move_legal(move: str) -> bool:
    """Central logic for whether a requested move is played or not."""
    coords = parse_move(move)

init_board()
standard_board_setup()
print(stringify_board())

while True:
    eto = input()
    print(eto)