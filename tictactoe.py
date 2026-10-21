class Board:
    def __init__(self):
        #here, we will create a board with 9 inputs in it for the 'x' or 'o'
        self.board=[' 'for i in range(9)]

    def display(self):
        #in this method, we will just print the board in the console
        print()
        print(f"  {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("------------")
        print(f"  {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("------------")
        print(f"  {self.board[6]} | {self.board[7]} | {self.board[8]} ")
        print()
    
    def is_valid_move(self, index):
        #this method will check if the move made by player is valid, i.e, the index user want to chose is between 1-9 or not and also that index is not used previously
        return 0<=index<9 and self.board[index]==' '
    
    def make_move(self, index, marker):
        #let the player to make a move    
        self.board[index]=marker


    def undo_move(self, index):
        #if a player want to undo the recent move then use this method
        self.board[index]=' '

    def is_valid_move(self, index):
        #check for the validation of the move made, i.e. if the index of move is not in range of 9 or the index is not empty i mean the index is already filled in previous moves
        return 0<=index<9 and self.board[index]==' '

    def check_winner(self, marker):
        #this method will check if there is any winner in the game at this point. if any diagonal, row, or coloumn is filled with all the same markers, then the winner will be found
        win_conditions=[(0, 1, 2), (3, 4, 5), (6, 7, 8), 
            (0, 3, 6), (1, 4, 7), (2, 5, 8), 
            (0, 4, 8), (2, 4, 6)]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == self.board[c] == marker:
                return True
        return False

    def is_full(self):
        #this method will check if there is no empty index in the board at this point. the game will be drawn if this method hits
        return ' ' not in self.board

    def get_available_moves(self):
        # this method will return all possible moves that the player can do at this specific point of the game
        availablemoves=[i for i, cell in enumerate(self.board) if cell == ' ']
        return availablemoves



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












game_board = Board()


choice = ""
while choice not in ["X", "O"]:
    choice = input("Do you want to choose 'X' or 'O'? : ").upper()
    if choice not in ["X", "O"]:
        print("Invalid choice! Please type only 'X' or 'O'.")

human_marker = choice
ai_marker = 'O' if human_marker == 'X' else 'X'

human_player = HumanPlayer(human_marker)
ai_player = AIPlayer(ai_marker)

current_player = ai_player if ai_marker == 'X' else human_player

print("\n------------------------------------------")
print("               Game is start              ")
print("------------------------------------------")

while True:
    game_board.display()
    
    if current_player == ai_player:
        move = ai_player.get_move(game_board)
    else:
        move = current_player.get_move(game_board)
    
    game_board.make_move(move, current_player.marker)
    
    if game_board.check_winner(current_player.marker):
        game_board.display()
        if current_player == ai_player:
            print("AI wins!!!")
        else:
            print("You Win!!!")
        break
    
    if game_board.is_full():
        game_board.display()
        print("Game is Draw!!!")
        break
    
  
    current_player = ai_player if current_player == human_player else human_player