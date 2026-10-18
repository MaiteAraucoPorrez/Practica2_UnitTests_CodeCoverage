
import pytest

from pieces.bishop import Bishop
from pieces.pawn import Pawn

W = True

SAME_SQUARE = "Bishop must move to a different square"
INVALID_MOVE = "Bishop can only move diagonally"
BLOCKED_PATH = "Path is blocked by another piece"

CASES = [
    (
        "TC-B1-misma-casilla",
        "c1", "c1",
        {},
        False,
        SAME_SQUARE,
    ),
    (
        "TC-B2-diagonal-libre",
        "c1", "f4",
        {},
        True,
        "",
    ),
    (
        "TC-B3-movimiento-vertical-invalido",
        "c1", "c4",
        {},
        False,
        INVALID_MOVE,
    ),
    (
        "TC-B4-diagonal-bloqueada",
        "c1", "f4",
        {"d2": Pawn(W)},
        False,
        BLOCKED_PATH,
    ),
    (
        "TC-B5-diagonal-una-casilla",
        "c1", "d2",
        {},
        True,
        "",
    ),
    (
        "TC-B6-movimiento-de-caballo-invalido",
        "c1", "e2",
        {},
        False,
        INVALID_MOVE,
    ),
]


@pytest.mark.parametrize(
    "start, end, pieces, expected, message",
    [pytest.param(*c[1:], id=c[0]) for c in CASES],
)
def test_bishop_validate_move(
    empty_board, capsys, start, end, pieces, expected, message
):
    empty_board.update(pieces)
    original_board = empty_board.copy()

    bishop = Bishop(W)

    result = bishop.validate_move(start, end, empty_board)

    assert result is expected

    output = capsys.readouterr().out

    if message:
        assert message in output
    else:
        assert output == ""

    assert empty_board == original_board
