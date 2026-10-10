import pytest
from helpers import Pawn, empty

@pytest.fixture
def board():
    return empty()

def test_primer_movimiento_dos_pasos(board):
    assert Pawn(True).validate_move("e2", "e4", board) is True

def test_error_intencional(board):
    resultado = Pawn(True).validate_move("e2", "e4", board)
    assert resultado == False   # esperamos False a propósito
