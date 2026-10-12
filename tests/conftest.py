import pytest
from board import Board

FILES = "abcdefgh"
RANKS = "12345678"


@pytest.fixture
def empty_board():
    """Tablero vacío (dict de 64 casillas en None). Se crea nuevo en cada prueba.

    Setup: crea el tablero.
    Teardown (después de `yield`): comprueba que la prueba no agregó ni quitó casillas.
    """
    board = {f"{f}{r}": None for f in FILES for r in RANKS}
    yield board
    assert len(board) == 64, "Teardown: la prueba cambió las casillas del tablero"


@pytest.fixture
def new_board():
    """Board real con las piezas en posición inicial."""
    return Board()
