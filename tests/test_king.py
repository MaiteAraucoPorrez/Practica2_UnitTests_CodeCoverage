import pytest
from pieces.king import King
from pieces.pawn import Pawn

W = True

# (id, inicio, fin, piezas en el tablero, resultado esperado, mensaje que debe imprimir ("" = ninguno))
CASES = [
    ("K1-misma-casilla",             "e4", "e4", {},              False, "King must move to a different square"),
    ("K2-una-casilla-vertical",      "e4", "e5", {},              True,  ""),
    ("K3-una-casilla-horizontal",    "e4", "f4", {},              True,  ""),
    ("K4-dos-casillas-vertical",     "e4", "e6", {},              False, "King can only move one square"),
    ("K5-dos-casillas-horizontal",   "e4", "g4", {},              False, "King can only move one square"),
    ("K6-destino-ocupado-por-amiga", "e4", "e5", {"e5": Pawn(W)}, False, "Path is blocked by another piece"),
    ("K7-una-casilla-diagonal",      "e4", "f5", {},              True,  ""),
]


@pytest.mark.parametrize(
    "start, end, pieces, expected, message",
    [pytest.param(*c[1:], id=c[0]) for c in CASES],
)
def test_king_validate_move(empty_board, capsys, start, end, pieces, expected, message):
    empty_board.update(pieces)

    result = King(W).validate_move(start, end, empty_board)

    assert result is expected
    out = capsys.readouterr().out
    if message:
        assert message in out
    else:
        assert out == ""      # un movimiento válido no imprime nada
