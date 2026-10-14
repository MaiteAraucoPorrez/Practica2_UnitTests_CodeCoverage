import pytest

from pieces.piece import Piece
from pieces.space import Space

W = True

# (id, inicio, fin, resultado esperado)
PATH_CASES = [
    ("G1-vertical-arriba",          "a1", "a4", ["a2", "a3", "a4"]),
    ("G2-vertical-abajo",           "a4", "a1", ["a3", "a2", "a1"]),
    ("G3-horizontal-derecha",       "a1", "d1", ["b1", "c1", "d1"]),
    ("G4-horizontal-izquierda",     "d1", "a1", ["c1", "b1", "a1"]),
    ("G5-diagonal-arriba-derecha",  "a1", "c3", ["b2", "c3"]),
    ("G6-diagonal-abajo-izquierda", "c3", "a1", ["b2", "a1"]),
    ("G7-diagonal-arriba-izquierda","d1", "a4", ["c2", "b3", "a4"]),
    ("G8-diagonal-abajo-derecha",   "a4", "d1", ["b3", "c2", "d1"]),
    ("G9-una-iteracion",            "a1", "a2", ["a2"]),
    ("G10-misma-casilla",           "a1", "a1", ["a1"]),
]


@pytest.mark.parametrize(
    "start, end, expected",
    [pytest.param(*c[1:], id=c[0]) for c in PATH_CASES],
)
def test_piece_get_path(start, end, expected):
    piece = object.__new__(Piece)

    result = piece.get_path(start, end)

    assert result == expected


@pytest.mark.parametrize(
    "square, expected",
    [
        (None, True),
        (Space(W), True),
        (object.__new__(Piece), False),
    ],
    ids=[
        "S1-casilla-None",
        "S2-casilla-Space",
        "S3-casilla-pieza",
    ],
)
def test_piece_validate_is_space(square, expected):
    piece = object.__new__(Piece)
    board = {"a1": square}

    result = piece.validate_is_space("a1", board)

    assert result is expected