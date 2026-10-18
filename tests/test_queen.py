
import pytest

from pieces.queen import Queen
from pieces.pawn import Pawn

W, B = True, False

SAME_SQUARE = "Queen must move to a different square"
INVALID_MOVE = "Queen can only move in a straight line or diagonally"
BLOCKED_PATH = "Path is blocked by another piece"

# (id, inicio, fin, piezas en tablero, resultado esperado, mensaje)
CASES = [
    (
        "TC-Q1-misma-casilla",
        "d4", "d4",
        {},
        False,
        SAME_SQUARE,
    ),
    (
        "TC-Q2-vertical-libre",
        "d4", "d7",
        {},
        True,
        "",
    ),
    (
        "TC-Q3-horizontal-libre",
        "d4", "g4",
        {},
        True,
        "",
    ),
    (
        "TC-Q4-diagonal-libre",
        "d4", "g7",
        {},
        True,
        "",
    ),
    (
        "TC-Q5-movimiento-invalido",
        "d4", "e6",
        {},
        False,
        INVALID_MOVE,
    ),
    (
        "TC-Q6-bloqueo-vertical-primera-casilla",
        "d4", "d7",
        {"d5": Pawn(W)},
        False,
        BLOCKED_PATH,
    ),
    (
        "TC-Q7-bloqueo-vertical-segunda-casilla",
        "d4", "d7",
        {"d6": Pawn(W)},
        False,
        BLOCKED_PATH,
    ),
    (
        "TC-Q8-bloqueo-diagonal-enemigo",
        "d4", "g7",
        {"e5": Pawn(B)},
        False,
        BLOCKED_PATH,
    ),
    (
        "TC-Q9-bloqueo-horizontal-amigo",
        "d4", "g4",
        {"e4": Pawn(W)},
        False,
        BLOCKED_PATH,
    ),
]


@pytest.mark.parametrize(
    "start, end, pieces, expected, message",
    [pytest.param(*c[1:], id=c[0]) for c in CASES],
)
def test_queen_validate_move(
    empty_board, capsys, start, end, pieces, expected, message
):
    # Arrange: preparar el tablero
    empty_board.update(pieces)
    original_board = empty_board.copy()

    queen = Queen(W)

    # Act: ejecutar el metodo a probar
    result = queen.validate_move(start, end, empty_board)

    # Assert: comprobar el resultado
    assert result is expected

    # Comprobar el mensaje mostrado
    output = capsys.readouterr().out

    if message:
        assert message in output
    else:
        assert output == ""

    # Verificar que el movimiento no modifico el tablero
    assert empty_board == original_board
