class Player:
    def __init__(self, marker):
       #this init method will add attribute to the player class, when the player will be created, he will be given the makrker at the time of creation
       self.marker=marker
    def get_move(self, board):
        #this method will get move from the player
        raise NotImplementedError("")


class HumanPlayer(Player):
    def __init__(self, marker):
        #inheritence implement
        super().__init__(marker)
    def get_move(self, board):
        #this method is override from main player class
        while True:
            try:
                user_input=input(f"Player {self.marker}, enter your move: ")
                choice=int(user_input)
                index=choice - 1
                if board.is_valid_move(index):
                    return index
                else:
                    print(" this is already taken or it is filled. Try again.")        
            except ValueError:
                print("Invalid input! Please enter a valid number between 1 and 9.")
  
class AIPlayer(Player):
    def __init__(self, marker):
        super().__init__(marker)
        # if user select any marker, the ai will get other marker
        self.opponent_marker = 'O' if marker == 'X' else 'X'

    def get_move(self, board):
        #this method is override by main player class
        best_score = -float('inf')
        best_move = None

        for move in board.get_available_moves():
            board.make_move(move, self.marker)
            score = self.minimax(board, 0, False)
            board.undo_move(move)
            if score > best_score:
                best_score = score
                best_move = move        
        return best_move

    def minimax(self, board, depth, is_maximizing):
        #if the ai win at 1st attempt, score 10 is given, if drawn, score 0 is given,, if user win score -10 is given
        if board.check_winner(self.marker):
            return 10 - depth 
        if board.check_winner(self.opponent_marker):
            return depth - 10 
        if board.is_full():
            return 0    
        #if Ai is max side, then logic for max side   
        if is_maximizing:
            max_eval = -float('inf')
            for move in board.get_available_moves():
                board.make_move(move, self.marker)
                eval = self.minimax(board, depth + 1, False)
                board.undo_move(move)
                max_eval = max(max_eval, eval)
            return max_eval
        #if AI is on minimum side, then logix for min side
        else:
            min_eval = float('inf')
            for move in board.get_available_moves():
                board.make_move(move, self.opponent_marker)
                eval = self.minimax(board, depth + 1, True)
                board.undo_move(move)
                min_eval = min(min_eval, eval)
            return min_eval