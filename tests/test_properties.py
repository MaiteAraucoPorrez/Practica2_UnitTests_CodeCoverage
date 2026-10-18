
import pytest
from hypothesis import given, settings, strategies as st

from pieces.piece import Piece
from pieces.king import King
from pieces.knight import Knight


FILES = "abcdefgh"
RANKS = "12345678"
SQUARES = [f"{f}{r}" for f in FILES for r in RANKS]

DIRECTIONS = [
    (0, 1), (0, -1),
    (1, 0), (-1, 0),
    (1, 1), (-1, -1),
    (-1, 1), (1, -1),
]


def square_at(file_index, rank_index):
    return f"{FILES[file_index]}{rank_index + 1}"


def coordinates(square):
    return FILES.index(square[0]), int(square[1]) - 1


def in_board(file_index, rank_index):
    return 0 <= file_index < 8 and 0 <= rank_index < 8


def empty_board():
    return {square: None for square in SQUARES}


# TC-H1: generar caminos rectos o diagonales válidos
@st.composite
def path_cases(draw):
    dx, dy = draw(st.sampled_from(DIRECTIONS))

    possible_starts = [
        (x, y)
        for x in range(8)
        for y in range(8)
        if in_board(x + dx, y + dy)
    ]

    x, y = draw(st.sampled_from(possible_starts))

    max_steps = max(
        n for n in range(1, 8)
        if in_board(x + dx * n, y + dy * n)
    )

    n = draw(st.integers(min_value=1, max_value=max_steps))

    start = square_at(x, y)
    end = square_at(x + dx * n, y + dy * n)

    return start, end, dx, dy, n


@settings(max_examples=100, deadline=None)
@given(case=path_cases())
def test_h1_get_path_property(case):
    start, end, dx, dy, n = case
    x, y = coordinates(start)

    piece = object.__new__(Piece)
    result = piece.get_path(start, end)

    expected_path = [
        square_at(x + dx * step, y + dy * step)
        for step in range(1, n + 1)
    ]

    assert len(result) == n
    assert result[0] == expected_path[0]
    assert result[-1] == end
    assert result == expected_path


# TC-H2 y TC-H3: movimientos válidos e inválidos
def is_knight_move(start, end):
    x1, y1 = coordinates(start)
    x2, y2 = coordinates(end)

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    return (dx, dy) in ((1, 2), (2, 1))


def is_king_move(start, end):
    x1, y1 = coordinates(start)
    x2, y2 = coordinates(end)

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    return max(dx, dy) == 1


KNIGHT_VALID = []
KNIGHT_INVALID = []
KING_VALID = []
KING_INVALID = []

for start in SQUARES:
    for end in SQUARES:
        pair = (start, end)

        if is_knight_move(start, end):
            KNIGHT_VALID.append(pair)
        else:
            KNIGHT_INVALID.append(pair)

        if is_king_move(start, end):
            KING_VALID.append(pair)
        else:
            KING_INVALID.append(pair)


@st.composite
def movement_cases(draw, piece_type):
    want_valid = draw(st.booleans())

    if piece_type == "knight":
        cases = KNIGHT_VALID if want_valid else KNIGHT_INVALID
    else:
        cases = KING_VALID if want_valid else KING_INVALID

    return draw(st.sampled_from(cases))


@settings(max_examples=100, deadline=None)
@given(case=movement_cases("knight"))
def test_h2_knight_property(case):
    start, end = case

    board = empty_board()
    knight = Knight(True)

    expected = is_knight_move(start, end)
    result = knight.validate_move(start, end, board)

    assert result is expected


@settings(max_examples=100, deadline=None)
@given(case=movement_cases("king"))
def test_h3_king_property(case):
    start, end = case

    board = empty_board()
    king = King(True)

    expected = is_king_move(start, end)
    result = king.validate_move(start, end, board)

    assert result is expected
