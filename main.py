from enum import Enum

# Chess board is from a1 to h8
# Inner coords replace letter with number: 00 to 77

WIDTH = 8
HEIGHT = 8

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
    """Object to represent a position on a chess board."""
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
        self.x = Coords.LETTERS.index(string[0])
        self.y = Coords.NUMBERS.index(string[1])
    def to_board_key(self):
        return f"{self.x}:{self.y}"

class Piece:
    """Class to represent a chess piece."""
    def __init__(self, piece_type: PieceType, color: PieceColor, coords: Coords):
        self.type = piece_type
        self.color = color
        self.coords = coords
    def stringify(self) -> str:
        """Returns a string representation of the piece. Should be str of length 3."""
        return self.color.value + self.type.value.upper() + self.color.value

class Board:
    """Class to represent a chess board."""
    def __init__(self):
        self.pieces: dict[Piece | None] = {}
    def get_piece(self, coords: Coords) -> Piece | None:
        try:
            return self.pieces[coords.to_board_key()]
        except KeyError:
            return None
    def set_piece(self, piece: Piece):
        self.pieces[piece.coords.to_board_key()] = piece
    def remove_piece(self, coords: Coords):
        self.pieces[coords] = None
    def move_piece(self, piece: Piece, new_coords: Coords):
        self.pieces[piece.coords.to_board_key()] = None
        piece.coords = new_coords
        self.set_piece(piece)
    def move(self, old_coords: Coords, new_coords: Coords) -> bool:
        piece = self.get_piece(old_coords)
        if piece is None:
            return False
        self.move_piece(piece, new_coords)
        return True
    def stringify(self, show_coords: bool = False):
        row_sep = "+---"*WIDTH + "+\n"
        result = row_sep
        for y in range(HEIGHT):
            result += "|"
            for x in range(WIDTH):
                piece = self.get_piece(Coords(x, 7-y))
                if piece is None:
                    result += "   "
                else:
                    result += self.get_piece(Coords(x, 7-y)).stringify()
                result += "|"
            result += "\n" + row_sep
        return result
    def standard_board_setup(self):
        for x in range(WIDTH):
            self.set_piece(Piece(PieceType.PAWN, PieceColor.WHITE, Coords(x, 1)))
            self.set_piece(Piece(PieceType.PAWN, PieceColor.BLACK, Coords(x, 6)))
        # White side
        self.set_piece(Piece(PieceType.ROOK, PieceColor.WHITE, Coords(0, 0)))
        self.set_piece(Piece(PieceType.KNIGHT, PieceColor.WHITE, Coords(1, 0)))
        self.set_piece(Piece(PieceType.BISHOP, PieceColor.WHITE, Coords(2, 0)))
        self.set_piece(Piece(PieceType.QUEEN, PieceColor.WHITE, Coords(3, 0)))
        self.set_piece(Piece(PieceType.KING, PieceColor.WHITE, Coords(4, 0)))
        self.set_piece(Piece(PieceType.BISHOP, PieceColor.WHITE, Coords(5, 0)))
        self.set_piece(Piece(PieceType.KNIGHT, PieceColor.WHITE, Coords(6, 0)))
        self.set_piece(Piece(PieceType.ROOK, PieceColor.WHITE, Coords(7, 0)))
        # Black side
        self.set_piece(Piece(PieceType.ROOK, PieceColor.BLACK, Coords(0, 7)))
        self.set_piece(Piece(PieceType.KNIGHT, PieceColor.BLACK, Coords(1, 7)))
        self.set_piece(Piece(PieceType.BISHOP, PieceColor.BLACK, Coords(2, 7)))
        self.set_piece(Piece(PieceType.QUEEN, PieceColor.BLACK, Coords(3, 7)))
        self.set_piece(Piece(PieceType.KING, PieceColor.BLACK, Coords(4, 7)))
        self.set_piece(Piece(PieceType.BISHOP, PieceColor.BLACK, Coords(5, 7)))
        self.set_piece(Piece(PieceType.KNIGHT, PieceColor.BLACK, Coords(6, 7)))
        self.set_piece(Piece(PieceType.ROOK, PieceColor.BLACK, Coords(7, 7)))

# Accepts input in xy-xy format. (source-destination)
def parse_move(move_str: str) -> tuple[Coords]:
    """Parses moves in 'xy-xy' format. Returns tuple pair of Coords."""
    if len(move_str) != 5:
        raise ValueError("Incorrect string length for move. Given: " + move_str)
    coords = move_str.split("-")
    if len(coords) != 2:
        raise ValueError("Incorrectly delimited! Given: " + move_str)
    if not Coords.validate_str(coords[0]):
        raise ValueError("First coordinate formatting error. Given: " + coords[0])
    if not Coords.validate_str(coords[1]):
        raise ValueError("Second coordinate formatting error. Given: " + coords[1])
    # String parsing done, convert coords for internal use
    return (Coords(string = coords[0]), Coords(string = coords[1]))

def is_move_legal(old_coords: Coords, new_coords: Coords) -> bool:
    """Central logic for whether a requested move is played or not."""
    return True

def move(board: Board, move_str: str):
    coords = parse_move(move_str)
    if is_move_legal(*coords):
        board.move(*coords)


global_board = Board()
global_board.standard_board_setup()
print(global_board.stringify())

while True:
    user_input = input()
    try:
        move(global_board, user_input)
    except KeyError:
        print("Input error, try again:\n")
    else:
        print("\n\n" + global_board.stringify() + "\n")
