from source.board import Board
from source.player import HumanPlayer, AIPlayer

def play_game():
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