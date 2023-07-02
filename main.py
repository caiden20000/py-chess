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


def piece_color_to_str(piece_color: PieceColor) -> str:
    """Get a user-friendly string from the PieceColor enum."""
    if piece_color == PieceColor.BLACK:
        return "Black"
    if piece_color == PieceColor.WHITE:
        return "White"
    return "UNKNOWN"


def piece_type_to_str(piece_type: PieceType) -> str:
    """Get a user-friendly string from the PieceType enum."""
    if piece_type == PieceType.PAWN:
        return "Pawn"
    if piece_type == PieceType.ROOK:
        return "Rook"
    if piece_type == PieceType.KNIGHT:
        return "Knight"
    if piece_type == PieceType.BISHOP:
        return "Bishop"
    if piece_type == PieceType.QUEEN:
        return "Queen"
    if piece_type == PieceType.KING:
        return "King"
    return "UNKNOWN"


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
            self.out_of_bounds(raise_err=True)
        else:
            self.set_by_string(string)

    @staticmethod
    def validate_str(coords: str, raise_err: bool = False) -> bool:
        """Returns true if coord string is valid. EG. e1 is valid, w9 is not."""
        if len(coords) != 2 or coords[0] not in Coords.LETTERS or coords[1] not in Coords.NUMBERS:
            if raise_err:
                raise ValueError(
                    "The given coordinates are not valid! Given: " + coords)
            return False
        return True

    def out_of_bounds(self, raise_err: bool = False) -> bool:
        oob = self.x < self.MIN_WIDTH \
            or self.x > self.MAX_WIDTH \
            or self.y < self.MIN_HEIGHT \
            or self.y > self.MAX_HEIGHT
        if oob and raise_err:
            raise ValueError(
                f"Coordinates out of bounds! Given: ({self.x}, {self.y})")
        return oob

    def get_string(self) -> str:
        return Coords.LETTERS[self.x] + Coords.NUMBERS[self.y]

    def set_by_string(self, string):
        self.validate_str(string, raise_err=True)
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
        self.has_moved = False

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
        if piece.has_moved is False:
            piece.has_moved = True
        self.set_piece(piece)

    def move(self, old_coords: Coords, new_coords: Coords) -> bool:
        piece = self.get_piece(old_coords)
        if piece is None:
            return False
        self.move_piece(piece, new_coords)
        return True

    def stringify(self, show_coords: bool = False):
        # letters_coords = ' '*4 + ''.join([l + " "*3 for l in 'abcdefgh'])
        # letters_coords = ' '*4 + '   '.join('abcdefgh')
        letters_coords = "    a   b   c   d   e   f   g   h  "
        row_sep = "+---"*WIDTH + "+\n"
        result = ""
        if show_coords:
            result += letters_coords + "\n  "
        result += row_sep
        for y in range(HEIGHT):
            if show_coords:
                result += str(8-y) + " "
            result += "|"
            for x in range(WIDTH):
                piece = self.get_piece(Coords(x, 7-y))
                if piece is None:
                    result += "   "
                else:
                    result += self.get_piece(Coords(x, 7-y)).stringify()
                result += "|"
            if show_coords:
                result += " " + str(8-y)
            result += "\n"
            if show_coords:
                result += "  "
            result += row_sep
        if show_coords:
            result += letters_coords + "\n"
        return result

    def standard_board_setup(self):
        for x in range(WIDTH):
            self.set_piece(
                Piece(PieceType.PAWN, PieceColor.WHITE, Coords(x, 1)))
            self.set_piece(
                Piece(PieceType.PAWN, PieceColor.BLACK, Coords(x, 6)))
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
        raise ValueError(
            "Incorrect string length for move. Given: " + move_str)
    coords = move_str.split("-")
    if len(coords) != 2:
        raise ValueError("Incorrectly delimited! Given: " + move_str)
    if not Coords.validate_str(coords[0]):
        raise ValueError(
            "First coordinate formatting error. Given: " + coords[0])
    if not Coords.validate_str(coords[1]):
        raise ValueError(
            "Second coordinate formatting error. Given: " + coords[1])
    # String parsing done, convert coords for internal use
    return (Coords(string=coords[0]), Coords(string=coords[1]))


def out_of_bounds(x: int, y: int) -> bool:
    """Returns true if the given coordinate elements are out of bounds."""
    return 0 > x or WIDTH <= x or 0 > y or HEIGHT <= y


def piece_exists_at(board: Board, coords: Coords) -> bool:
    """Returns true if any piece at the given coordinates."""
    return board.get_piece(coords) is not None


def _linear_iteration(board: Board, 
                      old_coords: Coords, 
                      dx: int, dy: int, 
                      limit: int = 50) -> dict[list[Coords]]:
    legal: list[Coords] = []
    possible_capture: list[Coords] = []
    x, y = old_coords.x, old_coords.y
    counter = 0
    while True:
        # infinite loop detector
        if counter == limit:
            break
        x += dx
        y += dy
        if x == old_coords.x and y == old_coords.y:
            continue
        if out_of_bounds(x, y):
            break
        if piece_exists_at(board, Coords(x, y)):
            possible_capture.append(Coords(x, y))
            break
        else:
            legal.append(Coords(x, y))
        counter += 1
    return {"legal": legal, "possible_capture": possible_capture}

# How do we represent legal moves?
# Loop add moves in a direction until we encounter a piece.
# Add all empty spaces found to "legal" list, add all pieces to "possible_capture" list.
#   For special pieces like the pawn, exceptions are made.
# Add all spaces that contain enemy pieces from the "possible_capture" list to the "legal" list.
# Return the legal list.


def get_all_legal_moves(board: Board, old_coords: Coords) -> list[Coords]:
    """Returns a list of every legal move the piece at old_coords can make."""
    legal: list[Coords] = []
    possible_capture: list[Coords] = []
    piece = board.get_piece(old_coords)

    # TODO: Pawn legal moves
    if piece.type == PieceType.PAWN:
        if piece.color == PieceColor.WHITE:
            # +y
            forwards = _linear_iteration(board, old_coords, 0, 1,
                                         limit = 1 if piece.has_moved else 2)
            legal += forwards["legal"]
            diagonals = [(-1, 1), (1, 1)]
            for diagonal in diagonals:
                attack = _linear_iteration(board, old_coords, *diagonal, limit = 1)
                possible_capture += attack["possible_capture"]
        if piece.color == PieceColor.BLACK:
            # -y
            forwards = _linear_iteration(board, old_coords, 0, -1,
                                         limit = 1 if piece.has_moved else 2)
            legal += forwards["legal"]
            diagonals = [(-1, -1), (1, -1)]
            for diagonal in diagonals:
                attack = _linear_iteration(board, old_coords, *diagonal, limit = 1)
                possible_capture += attack["possible_capture"]

    # TODO: Rook legal moves
    if piece.type == PieceType.ROOK:
        # Leftwards, Rightwards, Upwards, Downwards
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for direction in directions:
            wards = _linear_iteration(board, old_coords, *direction)
            legal += wards["legal"]
            possible_capture += wards["possible_capture"]

    # TODO: Knight legal moves
    if piece.type == PieceType.KNIGHT:
        # Y'know, knight moves.
        # Limited to 1 space away
        directions = [(1, 2), (2, 1), (2, -1), (1, -2), 
                      (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        for direction in directions:
            wards = _linear_iteration(board, old_coords, *direction, limit = 1)
            legal += wards["legal"]
            possible_capture += wards["possible_capture"]

    # TODO: Bishop legal moves
    if piece.type == PieceType.BISHOP:
        # SW, NW, NE, SE
        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        for direction in directions:
            wards = _linear_iteration(board, old_coords, *direction)
            legal += wards["legal"]
            possible_capture += wards["possible_capture"]

    # TODO: Queen legal moves
    if piece.type == PieceType.QUEEN:
        # Leftwards, Rightwards, Upwards, Downwards, SW, NW, NE, SE
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1),
                      (-1, -1), (-1, 1), (1, 1), (1, -1)]
        for direction in directions:
            wards = _linear_iteration(board, old_coords, *direction)
            legal += wards["legal"]
            possible_capture += wards["possible_capture"]

    # TODO: King legal moves
    if piece.type == PieceType.KING:
        # Leftwards, Rightwards, Upwards, Downwards, SW, NW, NE, SE
        # Limited to 1 space away
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1),
                      (-1, -1), (-1, 1), (1, 1), (1, -1)]
        for direction in directions:
            wards = _linear_iteration(board, old_coords, *direction, limit = 1)
            legal += wards["legal"]
            possible_capture += wards["possible_capture"]

    # Add legal captures to legal list
    for coords in possible_capture:
        if board.get_piece(coords).color != piece.color:
            legal.append(coords)
    return legal


def is_move_legal(board: Board, old_coords: Coords, new_coords: Coords) -> bool:
    """Returns true if new_coords is in the list of all legal moves for the piece at old_coords."""
    return new_coords in get_all_legal_moves(board, old_coords)


def capture(captured_piece: Piece):
    """Called when a piece is captured. Responsible only for points distribution and notification."""
    capturer = "BLACK" if captured_piece.color == PieceColor.WHITE else "WHITE"
    print(f"{capturer} captured a {piece_type_to_str(captured_piece.type)}!\n")
    # TODO: Some points logic here


def move(board: Board, move_str: str):
    """Executes a move based on a valid move string."""
    coords = parse_move(move_str)
    if is_move_legal(board, *coords):
        captured_piece = board.get_piece(coords[1])
        if captured_piece is not None:
            # Capture
            capture(captured_piece)
        board.move(*coords)


def game():
    """Main game loop."""
    board = Board()
    board.standard_board_setup()
    print(board.stringify(True))

    exit_loop = False
    while exit_loop is False:
        user_input = input()
        try:
            move(board, user_input)
        except KeyError:
            print("Input error, try again:\n")
        else:
            print("\n\n" + board.stringify(True) + "\n")
