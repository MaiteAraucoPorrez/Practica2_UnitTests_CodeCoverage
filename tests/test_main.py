from unittest.mock import patch
import main


def test_main_creates_game():
    with patch.object(main, "Game") as fake_game:
        main.main()
    fake_game.assert_called_once_with()
