import pytest

from pieces.bishop import Bishop
from pieces.king import King
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.space import Space

W, B = True, False

# Defectos encontrados al probar el juego. Cada prueba afirma el comportamiento CORRECTO según las
# reglas del ajedrez y está marcada xfail(strict=True): hoy "falla" (el defecto existe), la suite
# pasa, y si alguien arregla el defecto la prueba pasa a XPASS y strict=True la convierte en error
# para obligar a quitar el xfail.
#
# BUG-02 (peón, is_en_passentable) está en tests/test_pawn.py, junto con las pruebas de Pawn.


# BUG-01 · el rey, la reina, la torre y el alfil no pueden capturar
@pytest.mark.xfail(strict=True, reason="BUG-01: get_path incluye la casilla destino y validate_is_space la rechaza si hay una pieza: no se puede capturar")
@pytest.mark.parametrize(
    "pieza, inicio, fin",
    [
        pytest.param(King(W),   "e4", "e5", id="BUG-01-rey"),
        pytest.param(Queen(W),  "d4", "d7", id="BUG-01-reina"),
        pytest.param(Rook(W),   "a1", "a4", id="BUG-01-torre"),
        pytest.param(Bishop(W), "c1", "f4", id="BUG-01-alfil"),
    ],
)
def test_bug01_pieza_deberia_poder_capturar_una_pieza_enemiga(empty_board, pieza, inicio, fin):
    empty_board[fin] = Pawn(B)                       # pieza enemiga en el destino

    assert pieza.validate_move(inicio, fin, empty_board) is True


# BUG-03 · el mensaje al elegir una casilla vacía depende del color de la casilla
@pytest.mark.xfail(strict=True, reason="BUG-03: validate_piece compara is_white antes de revisar si la casilla es un Space")
def test_bug03_casilla_vacia_siempre_dice_no_piece_selected(new_board, capsys):
    new_board.board["e4"] = Space(B)                 # casilla vacía "negra" en turno de blanco

    assert new_board.validate_piece(True, "e4") is False
    assert "No piece selected" in capsys.readouterr().out
