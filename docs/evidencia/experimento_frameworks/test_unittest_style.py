import unittest
from helpers import Pawn, empty

class TestPawn(unittest.TestCase):
    def setUp(self):
        self.board = empty()
        self.pawn = Pawn(True)

    def test_primer_movimiento_dos_pasos(self):
        self.assertTrue(self.pawn.validate_move("e2", "e4", self.board))

    def test_error_intencional(self):
        self.assertEqual(self.pawn.validate_move("e2", "e4", self.board), False)

if __name__ == "__main__":
    unittest.main()
