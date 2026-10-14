from unittest.mock import MagicMock, call, patch

import pytest

from game import Game

PREGUNTA = "Do you want to restart? (y/n)"


@pytest.fixture
def game():
    """Game listo para probar new_game sin arrancar una partida de verdad.

    Setup: Game() llama a new_game() dentro de su constructor (un bucle con input()),
    así que new_game se reemplaza solo mientras se construye. Después se cambia el
    tablero real por un MagicMock para aislar a Game de Board.
    """
    with patch.object(Game, "new_game"):
        g = Game()
    g.board = MagicMock()
    return g


def board_acepta_todo(game, rey_vivo=True):
    """El MagicMock del tablero da por buena la jugada (formato, pieza y movimiento)."""
    game.board.validate_turn_input.return_value = True
    game.board.validate_piece.return_value = True
    game.board.validate_piece_move.return_value = True
    game.board.check_king_exist.return_value = rey_vivo


def run_new_game(game, turns, answers):
    """Ejecuta new_game con jugadas simuladas (player_turn) y respuestas simuladas (input)."""
    with patch.object(game, "player_turn", side_effect=turns) as player_turn, \
         patch("builtins.input", side_effect=answers) as fake_input:
        game.new_game()
    return player_turn, fake_input


def test_ng1_new_game_gana_blanco(game, capsys):
    player_turn, fake_input = run_new_game(game, turns=[True], answers=["n"])

    out = capsys.readouterr().out
    assert "White wins the game!!" in out
    assert "Black wins" not in out
    player_turn.assert_called_once_with(True)
    fake_input.assert_called_once_with(PREGUNTA)
    game.board.draw_board.assert_called_once()


def test_ng2_new_game_gana_negro(game, capsys):
    player_turn, _ = run_new_game(game, turns=[False, True], answers=["n"])

    out = capsys.readouterr().out
    assert "Black wins the game!!" in out
    assert "White wins" not in out
    assert player_turn.call_args_list == [call(True), call(False)]


def test_ng3_new_game_respuesta_invalida_vuelve_a_preguntar(game, capsys):
    _, fake_input = run_new_game(game, turns=[True], answers=["x", "n"])

    assert fake_input.call_count == 2
    assert "Invalid input please try again." in capsys.readouterr().out


def test_ng4_new_game_reinicio_juega_dos_partidas(game, capsys):
    player_turn, _ = run_new_game(game, turns=[True, True], answers=["y", "n"])

    assert player_turn.call_count == 2
    assert capsys.readouterr().out.count("New Game Started") == 2
    assert game.board.draw_board.call_count == 2


def test_ng5_new_game_respuesta_en_mayuscula_termina(game, capsys):
    player_turn, fake_input = run_new_game(game, turns=[True], answers=["N"])

    assert player_turn.call_count == 1
    assert fake_input.call_count == 1
    assert "Invalid input" not in capsys.readouterr().out


def test_ng6_new_game_ronda_completa_sin_ganador_y_otra_ronda(game, capsys):
    player_turn, _ = run_new_game(game, turns=[False, False, True], answers=["n"])

    assert player_turn.call_args_list == [call(True), call(False), call(True)]
    out = capsys.readouterr().out
    assert "White wins the game!!" in out
    assert "Black wins" not in out


# =====================  Tarjeta 27 · Game.player_turn (con mocks)  =====================

def test_t1_player_turn_blanco_jugada_valida(game):
    board_acepta_todo(game)

    with patch("builtins.input", return_value="E2E4") as fake_input:
        resultado = game.player_turn(True)

    assert resultado is False                      # el rey sigue vivo: la partida continúa
    fake_input.assert_called_once_with("Enter a Move for White:")
    game.board.validate_turn_input.assert_called_once_with("e2e4")    # el texto se pasó a minúsculas
    game.board.validate_piece.assert_called_once_with(True, "e2")
    game.board.validate_piece_move.assert_called_once_with("e2", "e4")
    game.board.move_piece.assert_called_once_with(True, "e2", "e4")


def test_t2_player_turn_negro_cambia_el_mensaje(game):
    board_acepta_todo(game)

    with patch("builtins.input", return_value="e7e5") as fake_input:
        game.player_turn(False)

    fake_input.assert_called_once_with("Enter a Move for Black:")
    game.board.validate_piece.assert_called_once_with(False, "e7")
    game.board.move_piece.assert_called_once_with(False, "e7", "e5")


def test_t3_player_turn_formato_invalido_vuelve_a_pedir(game):
    board_acepta_todo(game)
    game.board.validate_turn_input.side_effect = [False, True]

    with patch("builtins.input", side_effect=["zz", "e2e4"]) as fake_input:
        game.player_turn(True)

    assert fake_input.call_count == 2
    assert game.board.validate_turn_input.call_args_list == [call("zz"), call("e2e4")]
    game.board.validate_piece.assert_called_once()          # el intento inválido no llegó a validar la pieza
    game.board.move_piece.assert_called_once_with(True, "e2", "e4")


def test_t4_player_turn_pieza_invalida_vuelve_a_pedir(game):
    board_acepta_todo(game)
    game.board.validate_piece.side_effect = [False, True]

    with patch("builtins.input", side_effect=["e7e5", "e2e4"]) as fake_input:
        game.player_turn(True)

    assert fake_input.call_count == 2
    game.board.validate_piece_move.assert_called_once_with("e2", "e4")   # solo se validó el movimiento del 2.º intento
    game.board.move_piece.assert_called_once_with(True, "e2", "e4")


def test_t5_player_turn_movimiento_invalido_vuelve_a_pedir(game):
    board_acepta_todo(game)
    game.board.validate_piece_move.side_effect = [False, True]

    with patch("builtins.input", side_effect=["e2e5", "e2e4"]) as fake_input:
        game.player_turn(True)

    assert fake_input.call_count == 2
    assert game.board.validate_piece_move.call_args_list == [call("e2", "e5"), call("e2", "e4")]
    game.board.move_piece.assert_called_once_with(True, "e2", "e4")


def test_t6_player_turn_captura_del_rey_termina_la_partida(game):
    board_acepta_todo(game, rey_vivo=False)

    with patch("builtins.input", return_value="e2e4"):
        resultado = game.player_turn(True)

    assert resultado is True                       # check_king_exist() es False → game over
