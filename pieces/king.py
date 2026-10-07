from pieces.piece import Piece

class King(Piece):
    def __init__(self, is_white):
        self.value = None
        self.is_white = is_white

    def validate_move(self, start_position, end_position, board):
        file_distance = abs(ord(end_position[0]) - ord(start_position[0]))
        rank_distance = abs(int(end_position[1]) - int(start_position[1]))

        if file_distance == 0 and rank_distance == 0:
            print("King must move to a different square")
            return False

        if file_distance > 1 or rank_distance > 1:
            print("King can only move one square")
            return False    

        for step in self.get_path(start_position, end_position):
            if not self.validate_is_space(step, board):
                print("Path is blocked by another piece")
                return False

        return True

    def draw_piece(self):
        if self.is_white:
            return("♚")
        else:
            return("♔")