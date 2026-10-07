from pieces.piece import Piece

class Bishop(Piece):
    def __init__(self, is_white):
        self.value = 3
        self.is_white = is_white

    def validate_move(self, start_position, end_position, board):
        file_distance = abs(ord(end_position[0]) - ord(start_position[0]))
        rank_distance = abs(int(end_position[1]) - int(start_position[1]))

        if file_distance == 0 and rank_distance == 0:
            print("Bishop must move to a different square")
            return False

        if file_distance != rank_distance:
            print("Bishop can only move diagonally")
            return False

        for step in self.get_path(start_position, end_position):
            if not self.validate_is_space(step, board):
                print("Path is blocked by another piece")
                return False

        return True

    def draw_piece(self):
        if self.is_white:
            return("♝")
        else:
            return("♗")