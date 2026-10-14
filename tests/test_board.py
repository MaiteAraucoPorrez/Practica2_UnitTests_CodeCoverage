import pytest

from board import Board
from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.space import Space

FILES = "abcdefgh"


# =====================  Tarjeta 23 · Board.validate_turn_input  =====================

# (id, texto que escribe el jugador, ¿es válido?)
TURN_INPUTS = [
    ("V1-valida",                    "a1a2",  True),
    ("V2-largo-3",                   "a1a",   False),
    ("V2b-largo-5",                  "a1a22", False),
    ("V3-archivo-origen-invalido",   "z1a2",  False),
    ("V4-fila-origen-invalida",      "a9a2",  False),
    ("V5-archivo-destino-invalido",  "a1z2",  False),
    ("V6-fila-destino-invalida",     "a1a9",  False),
    ("V7-mayusculas",                "A1A2",  False),
]


@pytest.mark.parametrize("line, valid", [pytest.param(*c[1:], id=c[0]) for c in TURN_INPUTS])
def test_validate_turn_input(new_board, capsys, line, valid):
    result = new_board.validate_turn_input(line)

    assert result is valid
    out = capsys.readouterr().out
    assert (out == "") is valid        # válida: no imprime nada; inválida: imprime la ayuda


def test_v8_validate_turn_input_imprime_la_ayuda(new_board, capsys):
    assert new_board.validate_turn_input("xx") is False

    out = capsys.readouterr().out
    assert "Invalid turn input" in out
    assert "Valid Files abcdefgh" in out
    assert "Valid Ranks 12345678" in out
