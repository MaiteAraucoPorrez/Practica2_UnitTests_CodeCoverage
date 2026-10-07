from board import Board

class Game():
    def __init__(self):
        self.board = Board()
        self.new_game()

    def new_game(self):
        print("Hello from chesspython!")
        print("If you want to start a new game type. Restart.")
        print("Type in the piece you want to move and then type the space you want to move it to.")
        print("Example: \"D4D5\"")
        
        restart = True

        while restart:
            print("New Game Started")
            self.board.draw_board()

            game_over = False

            while not game_over:
                white_turn = True
                game_over = self.player_turn(white_turn)
                if (game_over):
                    print("White wins the game!!")
                    continue
                white_turn = False
                game_over = self.player_turn(white_turn)
                if (game_over):
                    print("Black wins the game!!")
                    continue

            valid_input = False            
            while not valid_input:
                line = input(f"Do you want to restart? (y/n)").lower()
                if line == "n":
                    restart = False
                    valid_input = True
                elif line == "y":
                    restart = True
                    valid_input = True
                else:
                    print("Invalid input please try again.")

    def player_turn(self, white_turn):
        player = ""
        if white_turn:
            player = "White"
        else:
            player = "Black"
        
        while True:
            line = input(f"Enter a Move for {player}:").lower()
            is_valid_turn_input = self.board.validate_turn_input(line)
            if not is_valid_turn_input:
                continue

            start_position = line[:2]
            end_position = line[-2:]
        
            is_valid_piece = self.board.validate_piece(white_turn, start_position)
            if not is_valid_piece:
                continue

            is_valid_piece_move = self.board.validate_piece_move(start_position, end_position)
            if not is_valid_piece_move:
                continue
                
            self.board.move_piece(white_turn, start_position, end_position)

            return not self.board.check_king_exist()

