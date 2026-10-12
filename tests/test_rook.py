import pytest
from pieces.rook import Rook
from pieces.pawn import Pawn

W = True

# (id, inicio, fin, piezas en el tablero, resultado esperado, mensaje que debe imprimir ("" = ninguno))
CASES = [
    ("R1-misma-casilla",        "a1", "a1", {},              False, "Rook must move to a different square"),
    ("R2-vertical-libre",       "a1", "a4", {},              True,  ""),
    ("R3-horizontal-libre",     "a1", "d1", {},              True,  ""),
    ("R4-diagonal-invalida",    "a1", "c3", {},              False, "Rook can only move in a straight line"),
    ("R5-vertical-bloqueada",   "a1", "a4", {"a3": Pawn(W)}, False, "Path is blocked by another piece"),
    ("R6-una-casilla",          "a1", "a2", {},              True,  ""),
]


@pytest.mark.parametrize(
    "start, end, pieces, expected, message",
    [pytest.param(*c[1:], id=c[0]) for c in CASES],
)
def test_rook_validate_move(empty_board, capsys, start, end, pieces, expected, message):
    empty_board.update(pieces)

    result = Rook(W).validate_move(start, end, empty_board)

    assert result is expected
    out = capsys.readouterr().out
    if message:
        assert message in out
    else:
        assert out == ""      # un movimiento válido no imprime nada
