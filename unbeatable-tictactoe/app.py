import streamlit as st
from source.board import Board
from source.player import HumanPlayer, AIPlayer


st.set_page_config(page_title="Unbeatable Tic-Tac-Toe", layout="centered")

st.title(" Unbeatable Tic-Tac-Toe")


if "board" not in st.session_state:
    st.session_state.board = Board()
    st.session_state.human_marker = "X"
    st.session_state.ai_marker = "O"
    st.session_state.human_player = HumanPlayer("X")
    st.session_state.ai_player = AIPlayer("O")
    st.session_state.current_player = st.session_state.human_player
    st.session_state.game_over = False
    st.session_state.winner = None

with st.sidebar:
    st.header("Game Settings")
    choice = st.radio("Choose your marker:", ["X", "O"], index=0)
    
    if st.button("Restart / New Game"):
        st.session_state.board = Board()
        st.session_state.human_marker = choice
        st.session_state.ai_marker = "O" if choice == "X" else "X"
        st.session_state.human_player = HumanPlayer(st.session_state.human_marker)
        st.session_state.ai_player = AIPlayer(st.session_state.ai_marker)
   
        st.session_state.current_player = (
            st.session_state.ai_player if st.session_state.ai_marker == "X" 
            else st.session_state.human_player
        )
        st.session_state.game_over = False
        st.session_state.winner = None
        st.rerun()


if not st.session_state.game_over and st.session_state.current_player == st.session_state.ai_player:
    ai_move = st.session_state.ai_player.get_move(st.session_state.board)
    st.session_state.board.make_move(ai_move, st.session_state.ai_player.marker)
    
    if st.session_state.board.check_winner(st.session_state.ai_player.marker):
        st.session_state.game_over = True
        st.session_state.winner = "AI"
    elif st.session_state.board.is_full():
        st.session_state.game_over = True
        st.session_state.winner = "Draw"
    else:
        st.session_state.current_player = st.session_state.human_player
    st.rerun()


if st.session_state.game_over:
    if st.session_state.winner == "AI":
        st.error("AI wins!")
    elif st.session_state.winner == "Human":
        st.success("You Win!")
    else:
        st.warning("Draw!")
else:
    st.info(f"Current Turn: **{'You (' + st.session_state.human_marker + ')' if st.session_state.current_player == st.session_state.human_player else 'AI (' + st.session_state.ai_marker + ')'}**")

board_state = st.session_state.board.board

for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        cell_value = board_state[idx]

        button_label = cell_value if cell_value != ' ' else f"  "
        

        is_disabled = (cell_value != ' ') or st.session_state.game_over or (st.session_state.current_player != st.session_state.human_player)
        
        if cols[col].button(button_label, key=f"cell_{idx}", use_container_width=True, disabled=is_disabled):
       
            st.session_state.board.make_move(idx, st.session_state.human_player.marker)
            
         
            if st.session_state.board.check_winner(st.session_state.human_player.marker):
                st.session_state.game_over = True
                st.session_state.winner = "Human"
            elif st.session_state.board.is_full():
                st.session_state.game_over = True
                st.session_state.winner = "Draw"
            else:
             
                st.session_state.current_player = st.session_state.ai_player
                
            
                ai_move = st.session_state.ai_player.get_move(st.session_state.board)
                st.session_state.board.make_move(ai_move, st.session_state.ai_player.marker)
                
            
                if st.session_state.board.check_winner(st.session_state.ai_player.marker):
                    st.session_state.game_over = True
                    st.session_state.winner = "AI"
                elif st.session_state.board.is_full():
                    st.session_state.game_over = True
                    st.session_state.winner = "Draw"
                else:
                    st.session_state.current_player = st.session_state.human_player
            
            st.rerun()