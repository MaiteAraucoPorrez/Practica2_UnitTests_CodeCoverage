from pieces.piece import Piece

class Pawn(Piece):
    def __init__(self, is_white):
        self.value = 1
        self.is_white = is_white
        self.is_first_move = True
        self.is_en_passentable = False

    def validate_move(self, start_position, end_position, board):
        rank_distance = int(end_position[1]) - int(start_position[1])
        file_distance = abs(ord(end_position[0]) - ord(start_position[0]))
        forward_step = 1
        
        if self.is_white:
            forward_step = 1
        else:
            forward_step = -1

        is_forward_one = rank_distance == forward_step
        is_diagonal = file_distance == 1 and is_forward_one

        # Diagonal capture
        if is_diagonal:
            target = board[end_position]
            if target is None or target.is_space:
                print("Pawn can only capture diagonally if there is an enemy piece there")
                return False
            if target.is_white == self.is_white:
                print("Pawn cannot capture a friendly piece")
                return False
            self.is_first_move = False
            return True

        # Straight move
        if file_distance != 0:
            print("Pawn can only move in its given file")
            return False

        if self.is_first_move:
            if rank_distance == (2 * forward_step):
                self.is_en_passentable = True
            if rank_distance not in (forward_step, 2 * forward_step):
                print("Pawn can only move one or two spaces forward on the first turn")
                return False
        else:
            self.is_en_passentable = False
            if rank_distance != forward_step:
                print("Pawn can only move one space forward after its first turn")
                return False

        for step in self.get_path(start_position, end_position):
            if not self.validate_is_space(step, board):
                print("Path is blocked by another piece")
                return False

        self.is_first_move = False

        #TODO: pawns can also take on en passent. Need to figure out that logic here or somewhere else aswell.

        return True    

    def draw_piece(self):
        if self.is_white:
            return("♟")
        else:
            return("♙")