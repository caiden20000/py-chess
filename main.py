from enum import Enum
import random
import sys

# TODO: En Passant
# TODO: Castling
# TODO: Checkmate (That's dumb. Just take the King. TAKE IT. It's DUM-

# Chess board is from a1 to h8
# Inner coords replace letter with number: 00 to 77
WIDTH = 8
HEIGHT = 8

CHECK_DETECTION = True
CHECKMATE_DETECTION = False
BOT = False
UNICODE_PIECES = False


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

def swap_color(color: PieceColor):
    return PieceColor.BLACK if color == PieceColor.WHITE else PieceColor.WHITE

def piece_color_to_str(piece_color: PieceColor) -> str:
    """Get a user-friendly string from the PieceColor enum."""
    result = "UNKNOWN"
    if piece_color == PieceColor.BLACK:
        result = "Black"
    if piece_color == PieceColor.WHITE:
        result = "White"
    return result


def piece_type_to_str(piece_type: PieceType) -> str:
    """Get a user-friendly string from the PieceType enum."""
    result = "UNKNOWN"
    if piece_type == PieceType.PAWN:
        result = "Pawn"
    if piece_type == PieceType.ROOK:
        result = "Rook"
    if piece_type == PieceType.KNIGHT:
        result = "Knight"
    if piece_type == PieceType.BISHOP:
        result = "Bishop"
    if piece_type == PieceType.QUEEN:
        result = "Queen"
    if piece_type == PieceType.KING:
        result = "King"
    return result


class Coords:
    """Object to represent a position on a chess board."""
    LETTERS = "abcdefgh"
    NUMBERS = "12345678"
    MIN_WIDTH = 0
    MAX_WIDTH = 7
    MIN_HEIGHT = 0
    MAX_HEIGHT = 7

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def get_string(self) -> str:
        """Returns a human readable string that represents the coordinates."""
        return Coords.LETTERS[self.x] + Coords.NUMBERS[self.y]

    def to_board_key(self):
        """Returns a unique string to use as a key for the board dict."""
        return self.get_string()


def coords_from_string(string: str) -> Coords | None:
    """Returns a coords object from the given string. Returns None if invalid."""
    letters = Coords.LETTERS
    numbers = Coords.NUMBERS
    if len(string) != 2 or string[0] not in letters or string[1] not in numbers:
        return None
    return Coords(letters.index(string[0]), numbers.index(string[1]))


def coords_from_ints(x: int, y: int) -> Coords | None:
    """Returns a coords object from the given ints. Returns None if out of bounds."""
    oob = x < 0 or x > Coords.MAX_WIDTH or y < 0 or y > Coords.MAX_HEIGHT
    if oob:
        return None
    return Coords(x, y)


class Piece:
    """Class to represent a chess piece."""

    def __init__(self, piece_type: PieceType, color: PieceColor):
        self.type = piece_type
        self.color = color
        self.has_moved = False

    def get_string(self) -> str:
        """Returns a string representation of the piece. Should be str of length 3."""
        if UNICODE_PIECES:
            return self.unicode_version()
        return self.color.value + self.type.value.upper() + self.color.value

    def unicode_version(self) -> str:
        """Returns the unicode representation of the chess piece."""
        result = " "
        if self.color == PieceColor.BLACK and self.type == PieceType.PAWN:
            result += "♟"
        if self.color == PieceColor.BLACK and self.type == PieceType.ROOK:
            result += "♜"
        if self.color == PieceColor.BLACK and self.type == PieceType.KNIGHT:
            result += "♞"
        if self.color == PieceColor.BLACK and self.type == PieceType.BISHOP:
            result += "♝"
        if self.color == PieceColor.BLACK and self.type == PieceType.QUEEN:
            result += "♛"
        if self.color == PieceColor.BLACK and self.type == PieceType.KING:
            result += "♚"
        if self.color == PieceColor.WHITE and self.type == PieceType.PAWN:
            result += "♙"
        if self.color == PieceColor.WHITE and self.type == PieceType.ROOK:
            result += "♖"
        if self.color == PieceColor.WHITE and self.type == PieceType.KNIGHT:
            result += "♘"
        if self.color == PieceColor.WHITE and self.type == PieceType.BISHOP:
            result += "♗"
        if self.color == PieceColor.WHITE and self.type == PieceType.QUEEN:
            result += "♕"
        if self.color == PieceColor.WHITE and self.type == PieceType.KING:
            result += "♔"
        return result + " "


class Board:
    """Class to represent a chess board."""

    def __init__(self):
        self.pieces: dict[Piece | None] = {}

    def clear(self):
        """Reset the board."""
        self.pieces: dict[Piece | None] = {}

    def get_piece(self, coords: Coords) -> Piece | None:
        """Returns the piece at a given coords. Returns None if no piece exists."""
        try:
            return self.pieces[coords.to_board_key()]
        except KeyError:
            return None

    def set_piece(self, piece: Piece, coords: Coords):
        """Sets a piece at a given coords."""
        self.pieces[coords.to_board_key()] = piece

    def remove_piece(self, coords: Coords):
        """Erases any piece at the given coords."""
        self.pieces[coords.to_board_key()] = None

    def move(self, old_coords: Coords, new_coords: Coords) -> bool:
        """Moves a piece from old_coords to new_coords. Returns True if successful."""
        piece = self.get_piece(old_coords)
        if piece is None:
            err_no_piece(old_coords)
            return False
        if piece.has_moved is False:
            piece.has_moved = True
        self.remove_piece(old_coords)
        self.set_piece(piece, new_coords)
        return True

    def get_string(self, show_coords: bool = False, highlight_list: list[Coords] | None = None):
        """
        Returns the board in ASCII "art" fashion.
        show_coords bool controls whether or not the 'a b c d ...' (& numbers) are shown.
        highlight_list is a list of coordines to replace with a block string.
        """
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
                if highlight_list is not None and \
                        _is_coords_in_list(Coords(x, 7-y), highlight_list):
                    if piece is None:
                        result += "▒▒▒"
                    else:
                        result += f"▓{piece.get_string()[1]}▓"
                else:
                    if piece is None:
                        result += "   "
                    else:
                        result += piece.get_string()
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
        """Sets up the board with all new pieces, in correct chess positions."""
        self.clear()
        # Pawns
        for x in range(WIDTH):
            self.set_piece(
                Piece(PieceType.PAWN, PieceColor.WHITE), Coords(x, 1))
            self.set_piece(
                Piece(PieceType.PAWN, PieceColor.BLACK), Coords(x, 6))
        # White side
        self.set_piece(Piece(PieceType.ROOK, PieceColor.WHITE), Coords(0, 0))
        self.set_piece(Piece(PieceType.KNIGHT, PieceColor.WHITE), Coords(1, 0))
        self.set_piece(Piece(PieceType.BISHOP, PieceColor.WHITE), Coords(2, 0))
        self.set_piece(Piece(PieceType.QUEEN, PieceColor.WHITE), Coords(3, 0))
        self.set_piece(Piece(PieceType.KING, PieceColor.WHITE), Coords(4, 0))
        self.set_piece(Piece(PieceType.BISHOP, PieceColor.WHITE), Coords(5, 0))
        self.set_piece(Piece(PieceType.KNIGHT, PieceColor.WHITE), Coords(6, 0))
        self.set_piece(Piece(PieceType.ROOK, PieceColor.WHITE), Coords(7, 0))
        # Black side
        self.set_piece(Piece(PieceType.ROOK, PieceColor.BLACK), Coords(0, 7))
        self.set_piece(Piece(PieceType.KNIGHT, PieceColor.BLACK), Coords(1, 7))
        self.set_piece(Piece(PieceType.BISHOP, PieceColor.BLACK), Coords(2, 7))
        self.set_piece(Piece(PieceType.QUEEN, PieceColor.BLACK), Coords(3, 7))
        self.set_piece(Piece(PieceType.KING, PieceColor.BLACK), Coords(4, 7))
        self.set_piece(Piece(PieceType.BISHOP, PieceColor.BLACK), Coords(5, 7))
        self.set_piece(Piece(PieceType.KNIGHT, PieceColor.BLACK), Coords(6, 7))
        self.set_piece(Piece(PieceType.ROOK, PieceColor.BLACK), Coords(7, 7))


def parse_move(move_str: str, delimiter: str = " to ") -> tuple[Coords] | None:
    """Parses moves in 'xy to xy' format. Returns tuple pair of Coords. Returns None if err."""
    if len(move_str) != len("xx" + delimiter + "yy"):
        return None
    coords = move_str.split(delimiter)
    if len(coords) != 2:
        return None
    first_coords = coords_from_string(coords[0])
    second_coords = coords_from_string(coords[1])
    if first_coords is None or second_coords is None:
        return None
    # String parsing done, convert coords for internal use
    return (first_coords, second_coords)


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
    """Useful iteration tool for legal move generation."""
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

def would_move_check(board: Board, old: Coords, new: Coords):
    """Simulates a move and returns True if the player is in check afterwards."""
    temp_piece = board.get_piece(new)
    moving_piece = board.get_piece(old)
    color = moving_piece.color
    result = False
    board.move(old, new)
    if is_in_check(board, color):
        result = True
    board.move(new, old)
    board.set_piece(temp_piece, new)
    return result

# TODO: Improve the CHECK detection with optimization
# if already in check:
#   only simulate moves that enter attacking squares
#   or capture enemy pieces
# if not in check:
#   only simulate moves from pieces that are ALREADY attacked.
#   (Assuming the only way to self-check is to unblock an attack)
def prune_check_moves(board: Board, old: Coords, legal: list[Coords], invert: bool = False) -> list[Coords]:
    """Removes all moves that would leave you in CHECK."""
    final: list[Coords] = []
    for coords in legal:
        if would_move_check(board, old, coords):
            if invert:
                final.append(coords)
            continue
        if not invert:
            final.append(coords)
    return final

def get_all_legal_moves(board: Board, old_coords: Coords, check_check: bool = True) -> list[Coords]:
    """Returns a list of every legal move the piece at old_coords can make."""
    legal: list[Coords] = []
    possible_capture: list[Coords] = []
    piece = board.get_piece(old_coords)

    # Pawn legal moves
    if piece.type == PieceType.PAWN:
        if piece.color == PieceColor.WHITE:
            # +y
            forwards = _linear_iteration(board, old_coords, 0, 1,
                                         limit=1 if piece.has_moved else 2)
            legal += forwards["legal"]
            diagonals = [(-1, 1), (1, 1)]
            for diagonal in diagonals:
                attack = _linear_iteration(
                    board, old_coords, *diagonal, limit=1)
                possible_capture += attack["possible_capture"]
        if piece.color == PieceColor.BLACK:
            # -y
            forwards = _linear_iteration(board, old_coords, 0, -1,
                                         limit=1 if piece.has_moved else 2)
            legal += forwards["legal"]
            diagonals = [(-1, -1), (1, -1)]
            for diagonal in diagonals:
                attack = _linear_iteration(
                    board, old_coords, *diagonal, limit=1)
                possible_capture += attack["possible_capture"]

    # Rook legal moves
    if piece.type == PieceType.ROOK:
        # Leftwards, Rightwards, Upwards, Downwards
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for direction in directions:
            wards = _linear_iteration(board, old_coords, *direction)
            legal += wards["legal"]
            possible_capture += wards["possible_capture"]

    # Knight legal moves
    if piece.type == PieceType.KNIGHT:
        # Y'know, knight moves.
        # Limited to 1 space away
        directions = [(1, 2), (2, 1), (2, -1), (1, -2),
                      (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        for direction in directions:
            wards = _linear_iteration(board, old_coords, *direction, limit=1)
            legal += wards["legal"]
            possible_capture += wards["possible_capture"]

    # Bishop legal moves
    if piece.type == PieceType.BISHOP:
        # SW, NW, NE, SE
        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        for direction in directions:
            wards = _linear_iteration(board, old_coords, *direction)
            legal += wards["legal"]
            possible_capture += wards["possible_capture"]

    # Queen legal moves
    if piece.type == PieceType.QUEEN:
        # Leftwards, Rightwards, Upwards, Downwards, SW, NW, NE, SE
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1),
                      (-1, -1), (-1, 1), (1, 1), (1, -1)]
        for direction in directions:
            wards = _linear_iteration(board, old_coords, *direction)
            legal += wards["legal"]
            possible_capture += wards["possible_capture"]

    # King legal moves
    if piece.type == PieceType.KING:
        # Leftwards, Rightwards, Upwards, Downwards, SW, NW, NE, SE
        # Limited to 1 space away
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1),
                      (-1, -1), (-1, 1), (1, 1), (1, -1)]
        for direction in directions:
            wards = _linear_iteration(board, old_coords, *direction, limit=1)
            legal += wards["legal"]
            possible_capture += wards["possible_capture"]

    # Add legal captures to legal list
    for coords in possible_capture:
        if board.get_piece(coords).color != piece.color:
            legal.append(coords)
    # Remove moves that put the player in CHECK
    if check_check:
        final = prune_check_moves(board, old_coords, legal)
        return final
    return legal


def _is_coords_in_list(coords: Coords, li: list[Coords]) -> bool:
    for c in li:
        if coords.x == c.x and coords.y == c.y:
            return True
    return False


def is_move_legal(board: Board, old_coords: Coords, new_coords: Coords) -> bool:
    """Returns true if new_coords is in the list of all legal moves for the piece at old_coords."""
    all_legal_moves = get_all_legal_moves(board, old_coords)
    return _is_coords_in_list(new_coords, all_legal_moves)


def capture(captured_piece: Piece):
    """Called when a piece is captured. Responsible only for points distribution and notification."""
    capturer = "BLACK" if captured_piece.color == PieceColor.WHITE else "WHITE"
    print(f"!!! {capturer} captured a {piece_type_to_str(captured_piece.type)}!")
    # TODO: Some points logic here


def list_legal_moves(board: Board, coords: Coords) -> str:
    """Returns a formatted list of every legal move for the piece at the given coords."""
    all_moves = get_all_legal_moves(board, coords)
    result_str = ""
    for c in all_moves:
        if result_str != "":
            result_str += ", "
        result_str += c.get_string()
    return result_str


def visualize_legal_moves(board: Board, coords: Coords) -> str:
    """Prints the legal moves on top of the board."""
    all_moves = get_all_legal_moves(board, coords)
    board_str = board.get_string(True, all_moves)
    return board_str


def move(board: Board, move_str: str, turn: PieceColor) -> bool:
    """Executes a move based on a valid move string."""
    coords = parse_move(move_str)
    if coords is None:
        err_bad_coords()
        return False
    piece = board.get_piece(coords[0])
    if piece is None:
        err_no_piece(coords[0])
        return False
    if piece.color != turn:
        err_wrong_turn(turn)
        return False
    if is_move_legal(board, *coords):
        captured_piece = board.get_piece(coords[1])
        board.move(*coords)
        # Reverse move if now in CHECK (or still in CHECK)
        if CHECK_DETECTION and is_in_check(board, turn):
            board.move(coords[1], coords[0])
            board.set_piece(captured_piece, coords[1])
            err_in_check()
            return False
        if captured_piece is not None:
            capture(captured_piece)
        return True
    elif would_move_check(board, *coords):
        err_in_check()
        return False
    else:
        err_illegal()
        return False


def err_no_piece(coords: Coords):
    """Err msg for "no piece" errors"""
    print("There is no piece at " + coords.get_string() + "!")


def err_illegal():
    """Err msg for "illegal move" errors"""
    print("You cannot move there! Try listing the legal moves for that piece.")


def err_bad_coords():
    """Err msg for "bad coords" errors"""
    print("The coordinates are incorrectly formatted!")


def err_wrong_turn(turn: PieceColor):
    """Err msg for "wrong turn" errors"""
    print(
        f"That piece doesn't belong to you! It's {piece_color_to_str(turn)}'s turn!")

def err_in_check():
    """Err msg for "in check" errors"""
    print("You cannot move there, that puts your king in CHECK!")

def print_turn(turn: PieceColor):
    """Prints out a string indicating who's turn it is."""
    result = f"=========== {piece_color_to_str(turn)}'s Turn! ==========="
    print(result)


def print_instructional_text():
    """Prints out a generic string listing options."""
    result = ""
    result += "| Type 'xx to yy' to move a piece.\n"
    result += "| Type 'xx' to see all available moves.\n"
    result += "| Type 'board' to reprint the board.\n"
    result += "| Type 'quit' to exit the program.\n"
    print(result)


def print_legal_moves(board: Board, coords: Coords):
    """Prints out a legal move list, as well as a visual diagram."""
    piece = board.get_piece(coords)
    # If there is no piece at the given coordinates, the request is invalid
    if piece is None:
        err_no_piece(coords)
        return
    # There is a piece at the coordinates, give the information for that piece:
    print("\n" + visualize_legal_moves(board, coords))
    print(
        f"| The legal moves for the {piece_type_to_str(piece.type)} at {coords.get_string()} are: ")
    print("| " + list_legal_moves(board, coords) + "\n")


def print_board(board: Board, turn: PieceColor):
    """Print the current board state and who's turn it is."""
    print("\n" + board.get_string(True) + "")
    print_turn(turn)


def handle_input(board: Board, turn: PieceColor, user_input: str) -> bool:
    """Returns True if a move was committed without error."""
    try:
        # If the string is of the form "xx to yy", it is a move
        if len(user_input) == len("xx to yy"):
            if not move(board, user_input, turn):
                return False
            return True

        # If the string is of the form "xx" then it is a legal move query
        elif len(user_input) == len("xx"):
            coords = coords_from_string(user_input)
            if coords is None:
                err_bad_coords()
                return False
            print_legal_moves(board, coords)
            return False

        # If the string is in this list of exiting strings, quit the program
        elif user_input in ["quit", "exit", "stop"]:
            print("| Quitting program...")
            sys.exit()

        elif user_input == "board":
            print_board(board, turn)
            return False

        # The string matched none of the previous checks, bad input
        else:
            print("!!! Unrecognized input, try again:\n")
            print_instructional_text()

    # Any error raised is a sign of a failure
    except (KeyError, ValueError) as ex:
        print(ex)
        print("!!! Input error, try again:\n")
        print_instructional_text()
        return False

# Apparently a pinned piece CAN still check your king.
def get_all_legal_moves_for_player(board: Board, turn: PieceColor, check_check: bool = False):
    """Returns list of tuple pairs of coordinates representing every possible move for a player."""
    # Moves are Coords tuple pairs, eg (a4, b5)
    all_moves: list[tuple[Coords]] = []
    # Copy to avoid dict change during iteration err
    pieces = board.pieces.copy()
    for coords in pieces:
        old_coords = coords_from_string(coords)
        piece = board.get_piece(old_coords)
        if piece is None or piece.color != turn:
            continue
        legal = get_all_legal_moves(board, old_coords, check_check)
        for new_coords in legal:
            all_moves.append((old_coords, new_coords))
    return all_moves

# Relies on get_all_legal_moves(), which currently doesn't account for CHECKs
def get_all_legal_inputs_for_player(board: Board, turn: PieceColor):
    """Returns list of every legal string input for a player."""
    all_moves = get_all_legal_moves_for_player(board, turn, check_check=True)
    all_inputs: list[str] = []
    for moves in all_moves:
        input_str = f"{moves[0].get_string()} to {moves[1].get_string()}"
        all_inputs.append(input_str)
    # for coords in board.pieces:
    #     old_coords = coords_from_string(coords)
    #     piece = board.get_piece(old_coords)
    #     if piece is None or piece.color != turn:
    #         continue
    #     legal = get_all_legal_moves(board, old_coords, check_check=True)
    #     for new_coords in legal:
    #         input_str = f"{coords} to {new_coords.get_string()}"
    #         all_inputs.append(input_str)
    return all_inputs

# This function can probably be optimized heavily
def is_in_check(board: Board, color: PieceColor) -> bool:
    """Checks every move to see if king is attacked."""
    checker = swap_color(color)
    all_moves = get_all_legal_moves_for_player(board, checker)
    for moves in all_moves:
        coords = moves[1]
        piece = board.get_piece(coords)
        if piece is None:
            continue
        if piece.color == color and piece.type == PieceType.KING:
            return True
    return False

def is_in_checkmate(board: Board, color: PieceColor) -> bool:
    """Returns true if the given player is in checkmate."""
    if not is_in_check(board, color):
        return False
    all_moves = get_all_legal_moves_for_player(board, color, check_check=True)
    if len(all_moves) == 0:
        return True
    return False

def print_win(color: PieceColor):
    """Declares the winner!"""
    print("==== The game is won! ====")
    print(f"{piece_color_to_str(color)} has checkmated {piece_color_to_str(swap_color(color))}!")
    print("_______ GOOD GAME ________")

def game():
    """Main game loop."""
    board = Board()
    board.standard_board_setup()
    print(board.get_string(True))

    turn = PieceColor.WHITE
    exit_loop = False
    print_turn(turn)
    print_instructional_text()
    while exit_loop is False:
        user_input = ""
        if BOT and turn == PieceColor.BLACK:
            possible_inputs = get_all_legal_inputs_for_player(board, turn)
            user_input = random.choice(possible_inputs)
            print("> " + user_input)
        else:
            # User input prefix
            print("> ", end="")
            # Read input until newline
            user_input = input()
        print("")
        input_result = handle_input(board, turn, user_input)
        if input_result is True:
            if is_in_checkmate(board, swap_color(turn)):
                print("\n" + board.get_string(True) + "")
                print_win(turn)
                exit_loop = True
                break
            turn = swap_color(turn)
            print_board(board, turn)
            print_instructional_text()
        else:
            # Move was unsuccessful
            print_instructional_text()

# Fool's mate
# f2 to f3
# e7 to e5
# g2 to g4
# d8 to h4

game()
