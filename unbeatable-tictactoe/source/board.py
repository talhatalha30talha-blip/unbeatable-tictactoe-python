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