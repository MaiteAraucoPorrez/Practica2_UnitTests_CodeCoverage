import pytest
from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.space import Space


def make_pawn(is_white=True, first_move=True):
    pawn = Pawn(is_white)
    pawn.is_first_move = first_move
    return pawn


# (id, peón blanco?, primer movimiento?, inicio, fin, piezas en el tablero, resultado esperado)
CASES = [
    ("P01-captura-diagonal-blanco",   True,  True,  "e4", "f5", {"f5": Rook(False)}, True),
    ("P02-captura-diagonal-negro",    False, True,  "e5", "d4", {"d4": Rook(True)},  True),
    ("P03-diagonal-casilla-vacia",    True,  True,  "e4", "f5", {},                  False),
    ("P04-diagonal-hacia-Space",      True,  True,  "e4", "f5", {"f5": Space(True)}, False),
    ("P05-diagonal-pieza-amiga",      True,  True,  "e4", "f5", {"f5": Rook(True)},  False),
    ("P06-salto-de-caballo",          True,  True,  "e2", "f4", {},                  False),
    ("P07-primer-mov-1-paso",         True,  True,  "e2", "e3", {},                  True),
    ("P08-primer-mov-2-pasos",        True,  True,  "e2", "e4", {},                  True),
    ("P09-primer-mov-3-pasos",        True,  True,  "e2", "e5", {},                  False),
    ("P10-no-primer-mov-1-paso",      True,  False, "e3", "e4", {},                  True),
    ("P11-no-primer-mov-2-pasos",     True,  False, "e3", "e5", {},                  False),
    ("P12-2-pasos-1ra-casilla-bloq",  True,  True,  "e2", "e4", {"e3": Rook(False)}, False),
    ("P13-1-paso-destino-ocupado",    True,  True,  "e2", "e3", {"e3": Rook(False)}, False),
    ("P14-desplazamiento-lateral-2",  True,  True,  "e2", "g3", {},                  False),
    ("P15-2-pasos-2da-casilla-bloq",  True,  True,  "e2", "e4", {"e4": Rook(False)}, False),
    ("P16-no-primer-mov-1-bloqueado", True,  False, "e3", "e4", {"e4": Rook(False)}, False),
    ("P17-movimiento-hacia-atras",    True,  True,  "e2", "e1", {},                  False),
]


@pytest.mark.parametrize(
    "is_white, first_move, start, end, pieces, expected",
    [pytest.param(*c[1:], id=c[0]) for c in CASES],
)
def test_pawn_validate_move(empty_board, is_white, first_move, start, end, pieces, expected):
    empty_board.update(pieces)
    pawn = make_pawn(is_white, first_move)

    assert pawn.validate_move(start, end, empty_board) is expected


def test_pawn_first_move_2_steps_marks_en_passentable(empty_board):
    pawn = make_pawn(first_move=True)
    pawn.validate_move("e2", "e4", empty_board)
    assert pawn.is_en_passentable is True
    assert pawn.is_first_move is False


@pytest.mark.xfail(strict=True, reason="BUG-02: marca is_en_passentable=True aunque el movimiento sea rechazado por camino bloqueado")
def test_pawn_blocked_two_step_must_not_mark_en_passentable(empty_board):
    empty_board["e3"] = Rook(False)
    pawn = make_pawn(first_move=True)
    assert pawn.validate_move("e2", "e4", empty_board) is False
    assert pawn.is_en_passentable is False
