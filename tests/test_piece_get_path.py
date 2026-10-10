import pytest
from pieces.pawn import Pawn
from pieces.space import Space


@pytest.mark.parametrize(
    "start, end, expected",
    [
        ("a1", "a4", ["a2", "a3", "a4"]),          # vertical hacia arriba
        ("a4", "a1", ["a3", "a2", "a1"]),          # vertical hacia abajo
        ("a1", "d1", ["b1", "c1", "d1"]),          # horizontal a la derecha
        ("d1", "a1", ["c1", "b1", "a1"]),          # horizontal a la izquierda
        ("a1", "c3", ["b2", "c3"]),                # diagonal arriba-derecha
        ("c3", "a1", ["b2", "a1"]),                # diagonal abajo-izquierda
        ("d1", "a4", ["c2", "b3", "a4"]),          # diagonal arriba-izquierda
        ("a4", "d1", ["b3", "c2", "d1"]),          # diagonal abajo-derecha
        ("a1", "a2", ["a2"]),                      # un solo paso (1 iteración)
        ("a1", "a1", ["a1"]),                      # misma casilla (caso borde)
    ],
)
def test_get_path(start, end, expected):
    piece = Pawn(True)   # get_path vive en Piece; cualquier subclase sirve

    assert piece.get_path(start, end) == expected


@pytest.mark.parametrize("square, expected", [(None, True), (Space(True), True), (Pawn(False), False)])
def test_validate_is_space(empty_board, square, expected):
    empty_board["e4"] = square
    assert Pawn(True).validate_is_space("e4", empty_board) is expected
