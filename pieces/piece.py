class Piece():
    is_space = False

    def __init__(self):
        self.value = 0

    def validate_is_space(self, position, board):
        square = board[position]
        return square is None or square.is_space

    def get_path(self, start_position, end_position):
        file_step = 0
        rank_step = 0

        if start_position[0] == end_position[0]:
            file_step = 0
        elif ord(end_position[0]) > ord(start_position[0]):
            file_step = 1
        else:
            file_step = -1

        if start_position[1] == end_position[1]:
            rank_step = 0
        elif int(end_position[1]) > int(start_position[1]):
            rank_step = 1
        else:
            rank_step = -1

        steps = []
        current_file = ord(start_position[0]) + file_step
        current_rank = int(start_position[1]) + rank_step

        while True:
            steps.append(f"{chr(current_file)}{current_rank}")
            if chr(current_file) == end_position[0] and str(current_rank) == end_position[1]:
                break
            current_file += file_step
            current_rank += rank_step

        return steps
