from pieces.piece import Piece

class Queen(Piece):
    def __init__(self, is_white):
        self.value = 9
        self.is_white = is_white

    def validate_move(self, start_position, end_position, board):
        file_distance = abs(ord(end_position[0]) - ord(start_position[0]))
        rank_distance = abs(int(end_position[1]) - int(start_position[1]))

        if file_distance == 0 and rank_distance == 0:
            print("Queen must move to a different square")
            return False

        is_straight_move = start_position[0] == end_position[0] or start_position[1] == end_position[1]
        is_diagonal_move = file_distance == rank_distance

        if not (is_straight_move or is_diagonal_move):
            print("Queen can only move in a straight line or diagonally")
            return False

        for step in self.get_path(start_position, end_position):
            if not self.validate_is_space(step, board):
                print("Path is blocked by another piece")
                return False

        return True

    def draw_piece(self):
        if self.is_white:
            return("♛")
        else:
            return("♕")