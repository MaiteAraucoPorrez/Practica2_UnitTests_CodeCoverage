import pytest
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.space import Space

W, B = True, False
L_SHAPE = "Knight must move in an L-shape"
FRIENDLY = "Knight cannot land on a friendly piece"

# (id, inicio, fin, piezas en el tablero, resultado esperado, mensaje que debe imprimir ("" = ninguno))
CASES = [
    ("N1-L-1-columna-2-filas",      "b1", "c3", {},                                              True,  ""),
    ("N2-L-2-columnas-1-fila",      "b1", "d2", {},                                              True,  ""),
    ("N3-diagonal-2-2",             "b1", "d3", {},                                              False, L_SHAPE),
    ("N4-diagonal-1-1",             "b1", "c2", {},                                              False, L_SHAPE),
    ("N5-destino-con-pieza-amiga",  "b1", "c3", {"c3": Pawn(W)},                                 False, FRIENDLY),
    ("N6-captura-pieza-enemiga",    "b1", "c3", {"c3": Pawn(B)},                                 True,  ""),
    ("N7-salta-piezas",             "b1", "c3", {"b2": Pawn(W), "c2": Pawn(W), "a1": Pawn(W)},   True,  ""),
    ("N8-3-columnas-1-fila",        "b1", "e2", {},                                              False, L_SHAPE),
]


@pytest.mark.parametrize(
    "start, end, pieces, expected, message",
    [pytest.param(*c[1:], id=c[0]) for c in CASES],
)
def test_knight_validate_move(empty_board, capsys, start, end, pieces, expected, message):
    empty_board.update(pieces)

    result = Knight(W).validate_move(start, end, empty_board)

    assert result is expected
    out = capsys.readouterr().out
    if message:
        assert message in out
    else:
        assert out == ""      # un movimiento válido no imprime nada


@pytest.mark.parametrize(
    "square, expected",
    [(None, True), (Space(W), True), (Pawn(B), True), (Pawn(W), False)],
    ids=["D1-casilla-vacia-None", "D2-casilla-Space", "D3-pieza-enemiga", "D4-pieza-amiga"],
)
def test_knight_validate_destination(empty_board, square, expected):
    empty_board["c3"] = square

    assert Knight(W).validate_destination("c3", empty_board) is expected
