import pytest
from helpers import Pawn, empty

@pytest.mark.parametrize("fin, esperado", [("e3", True), ("e4", True), ("e5", False)], ids=["1-paso", "2-pasos", "3-pasos"])
def test_peon_primer_movimiento(fin, esperado):
    assert Pawn(True).validate_move("e2", fin, empty()) is esperado
