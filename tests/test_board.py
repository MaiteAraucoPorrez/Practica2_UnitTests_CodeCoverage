
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


# ===================== Tarjeta 23 · Board.validate_turn_input =====================

# (id, texto que escribe el jugador, ¿es válido?)
TURN_INPUTS = [
    ("V1-valida", "a1a2", True),
    ("V2-largo-3", "a1a", False),
    ("V2b-largo-5", "a1a22", False),
    ("V3-archivo-origen-invalido", "z1a2", False),
    ("V4-fila-origen-invalida", "a9a2", False),
    ("V5-archivo-destino-invalido", "a1z2", False),
    ("V6-fila-destino-invalida", "a1a9", False),
    ("V7-mayusculas", "A1A2", False),
]


@pytest.mark.parametrize(
    "line, valid",
    [pytest.param(*c[1:], id=c[0]) for c in TURN_INPUTS],
)
def test_validate_turn_input(new_board, capsys, line, valid):
    result = new_board.validate_turn_input(line)

    assert result is valid
    out = capsys.readouterr().out
    assert (out == "") is valid


def test_v8_validate_turn_input_imprime_la_ayuda(new_board, capsys):
    assert new_board.validate_turn_input("xx") is False

    out = capsys.readouterr().out
    assert "Invalid turn input" in out
    assert "Valid Files abcdefgh" in out
    assert "Valid Ranks 12345678" in out


# ===================== Tarjeta 25 · construir y dibujar el tablero =====================

def test_bm1_build_board_crea_64_casillas_vacias(new_board):
    casillas = new_board.build_board()

    assert len(casillas) == 64
    assert set(casillas) == {f"{f}{r}" for f in FILES for r in "12345678"}
    assert all(valor is None for valor in casillas.values())


def test_bm2_init_pieces_posicion_inicial(new_board):
    orden = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

    for archivo, clase in zip(FILES, orden):
        blanca = new_board.board[f"{archivo}1"]
        negra = new_board.board[f"{archivo}8"]

        assert type(blanca) is clase and blanca.is_white is True
        assert type(negra) is clase and negra.is_white is False

    for archivo in FILES:
        assert type(new_board.board[f"{archivo}2"]) is Pawn and new_board.board[f"{archivo}2"].is_white
        assert type(new_board.board[f"{archivo}7"]) is Pawn and not new_board.board[f"{archivo}7"].is_white


def test_bm3_init_pieces_llena_las_filas_3_a_6_con_space(new_board):
    medio = [
        new_board.board[f"{f}{r}"]
        for f in FILES
        for r in "3456"
    ]

    assert len(medio) == 32
    assert all(isinstance(casilla, Space) for casilla in medio)
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
        pytest.param(King, "♚", "♔", id="King"),
        pytest.param(Queen, "♛", "♕", id="Queen"),
        pytest.param(Rook, "♜", "♖", id="Rook"),
        pytest.param(Bishop, "♝", "♗", id="Bishop"),
        pytest.param(Knight, "♞", "♘", id="Knight"),
        pytest.param(Pawn, "♟", "♙", id="Pawn"),
        pytest.param(Space, "■", "□", id="Space"),
    ],
)
def test_bm9_draw_piece_simbolo_distinto_por_color(pieza, blanca, negra):
    assert pieza(True).draw_piece() == blanca
    assert pieza(False).draw_piece() == negra


# ===================== HU · Board.validate_piece =====================

# (id, turno blanco, posición, color del Space o None,
#  resultado esperado, mensaje esperado)
PIECE_CASES = [
    (
        "TC-BP1-blanco-selecciona-propia",
        True,
        "e2",
        None,
        True,
        "",
    ),
    (
        "TC-BP2-blanco-selecciona-enemiga",
        True,
        "e7",
        None,
        False,
        "Please select a White piece",
    ),
    (
        "TC-BP3-negro-selecciona-propia",
        False,
        "e7",
        None,
        True,
        "",
    ),
    (
        "TC-BP4-negro-selecciona-enemiga",
        False,
        "e2",
        None,
        False,
        "Please select a Black piece",
    ),
    (
        "TC-BP5-space-blanco",
        True,
        "e4",
        True,
        False,
        "No piece selected",
    ),
]


@pytest.mark.parametrize(
    "white_turn, position, space_color, expected, message",
    [pytest.param(*c[1:], id=c[0]) for c in PIECE_CASES],
)
def test_board_validate_piece(
    new_board, capsys, white_turn, position,
    space_color, expected, message
):
    # Arrange
    if space_color is not None:
        new_board.board[position] = Space(space_color)

    # Act
    result = new_board.validate_piece(white_turn, position)

    # Assert
    assert result is expected

    output = capsys.readouterr().out

    if message:
        assert message in output
    else:
        assert output == ""


# ===================== TC-BP6 · BUG-03 =====================

@pytest.mark.xfail(
    strict=True,
    reason=(
        "BUG-03: validate_piece comprueba el color "
        "antes de verificar si la casilla es Space"
    ),
)
def test_bp6_space_negro_deberia_decir_no_piece_selected(new_board, capsys):
    # Arrange: turno blanco y casilla vacía negra
    new_board.board["e4"] = Space(False)

    # Act
    result = new_board.validate_piece(True, "e4")

    # Assert: comportamiento correcto esperado
    assert result is False

    output = capsys.readouterr().out

    # Actualmente esta comprobación falla por BUG-03
    assert "No piece selected" in output


# ===================== TC-BM4 · Board.validate_piece_move =====================

def test_bm4_validate_piece_move(new_board):
    # Movimiento válido: peón blanco de e2 a e4
    result_valid = new_board.validate_piece_move("e2", "e4")
    assert result_valid is True

    # Movimiento inválido: torre de a1 a a3,
    # ya que el peón de a2 bloquea el camino
    result_invalid = new_board.validate_piece_move("a1", "a3")
    assert result_invalid is False


# ===================== KeyError · Posición inexistente =====================

def test_validate_piece_posicion_inexistente(new_board):
    with pytest.raises(KeyError):
        new_board.validate_piece(True, "z9")


# ===================== TC-BM5 · Movimiento normal =====================

def test_bm5_move_piece_actualiza_tablero(new_board, capsys):
    # Arrange: guardar la referencia al peón original
    peon_blanco = new_board.board["e2"]

    assert isinstance(peon_blanco, Pawn)
    assert new_board.check_king_exist() is True

    # Act: mover el peón de e2 a e4
    new_board.move_piece(True, "e2", "e4")

    # Assert 1: el peón llegó a e4
    assert new_board.board["e4"] is peon_blanco

    # Assert 2: e2 quedó como una casilla vacía
    assert isinstance(new_board.board["e2"], Space)
    assert new_board.board["e2"].is_white is True

    # Assert 3: el tablero fue impreso
    output = capsys.readouterr().out
    lineas = output.splitlines()

    assert len(lineas) == 9
    assert lineas[3].startswith("4")

    # Assert 4: ningún rey fue capturado
    assert new_board.check_king_exist() is True


# ===================== TC-BM6 · Captura del rey =====================

def test_bm6_move_piece_detecta_captura_rey(new_board, capsys):
    # Arrange: colocar un rey negro en e4
    rey_negro = King(False)
    new_board.board["e4"] = rey_negro

    peon_blanco = new_board.board["e2"]

    assert isinstance(peon_blanco, Pawn)
    assert new_board.check_king_exist() is True

    # Act: mover el peón hacia la casilla del rey
    # Se prueba move_piece directamente, no la legalidad del movimiento
    new_board.move_piece(True, "e2", "e4")

    # Assert 1: el peón ocupa la casilla del rey capturado
    assert new_board.board["e4"] is peon_blanco

    # Assert 2: el origen queda vacío
    assert isinstance(new_board.board["e2"], Space)

    # Assert 3: el programa detectó la captura del rey
    assert new_board.check_king_exist() is False

    # Assert 4: el tablero se imprimió
    output = capsys.readouterr().out
    assert len(output.splitlines()) == 9
