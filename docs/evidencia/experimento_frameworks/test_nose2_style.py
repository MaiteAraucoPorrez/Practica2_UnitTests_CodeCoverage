from helpers import Pawn, empty

def test_primer_movimiento_dos_pasos():
    assert Pawn(True).validate_move("e2", "e4", empty()) is True

def test_error_intencional():
    resultado = Pawn(True).validate_move("e2", "e4", empty())
    assert resultado == False   # esperamos False a propósito
