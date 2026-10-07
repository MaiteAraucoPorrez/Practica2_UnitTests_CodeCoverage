from pieces.piece import Piece

class Space(Piece):
    is_space = True

    def __init__(self, is_white):
        self.is_white = is_white 

    def draw_piece(self):
        if self.is_white:
            return("■")
        else:
            return("□")