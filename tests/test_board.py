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


# =====================  Tarjeta 25 · construir y dibujar el tablero  =====================

def test_bm1_build_board_crea_64_casillas_vacias(new_board):
    casillas = new_board.build_board()

    assert len(casillas) == 64
    assert set(casillas) == {f"{f}{r}" for f in FILES for r in "12345678"}
    assert all(valor is None for valor in casillas.values())


def test_bm2_init_pieces_posicion_inicial(new_board):
    orden = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    for archivo, clase in zip(FILES, orden):
        blanca, negra = new_board.board[f"{archivo}1"], new_board.board[f"{archivo}8"]
        assert type(blanca) is clase and blanca.is_white is True
        assert type(negra) is clase and negra.is_white is False
    for archivo in FILES:
        assert type(new_board.board[f"{archivo}2"]) is Pawn and new_board.board[f"{archivo}2"].is_white
        assert type(new_board.board[f"{archivo}7"]) is Pawn and not new_board.board[f"{archivo}7"].is_white


def test_bm3_init_pieces_llena_las_filas_3_a_6_con_space(new_board):
    medio = [new_board.board[f"{f}{r}"] for f in FILES for r in "3456"]

    assert len(medio) == 32
    assert all(isinstance(casilla, Space) for casilla in medio)     # ninguna quedó en None
    assert sum(1 for casilla in medio if casilla.is_white) == 16
    assert sum(1 for casilla in medio if not casilla.is_white) == 16


def test_bm7_draw_board_imprime_9_lineas(new_board, capsys):
    new_board.draw_board()

    lineas = capsys.readouterr().out.splitlines()
    assert len(lineas) == 9
    assert lineas[0] == "1♜♞♝♛♚♝♞♜"
    assert lineas[1] == "2♟♟♟♟♟♟♟♟"
    assert lineas[7] == "8♖♘♗♕♔♗♘♖"
    assert lineas[8] == " abcdefgh"


def test_bm8_draw_board_dibuja_guion_bajo_en_casilla_none(new_board, capsys):
    new_board.board["e4"] = None

    new_board.draw_board()

    fila_4 = capsys.readouterr().out.splitlines()[3]
    assert fila_4.startswith("4")
    assert fila_4.count("_") == 1


@pytest.mark.parametrize(
    "pieza, blanca, negra",
    [
        pytest.param(King,   "♚", "♔", id="King"),
        pytest.param(Queen,  "♛", "♕", id="Queen"),
        pytest.param(Rook,   "♜", "♖", id="Rook"),
        pytest.param(Bishop, "♝", "♗", id="Bishop"),
        pytest.param(Knight, "♞", "♘", id="Knight"),
        pytest.param(Pawn,   "♟", "♙", id="Pawn"),
        pytest.param(Space,  "■", "□", id="Space"),
    ],
)
def test_bm9_draw_piece_simbolo_distinto_por_color(pieza, blanca, negra):
    assert pieza(True).draw_piece() == blanca
    assert pieza(False).draw_piece() == negra
