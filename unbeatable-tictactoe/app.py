import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

tic_tac_toe_component = components.declare_component(
    "tic_tac_toe_board", path=str(Path(__file__).parent / "frontend")
)
from source.board import Board
from source.player import HumanPlayer, AIPlayer


st.set_page_config(page_title="Classic Tic-Tac-Toe", page_icon="❌", layout="centered")


st.markdown("""
    <style>
    /* Fix top padding so content doesn't hide behind the header toolbar */
    .block-container {
        padding-top: 4.5rem !important;
        padding-bottom: 2rem !important;
    }

    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #2b1055 50%, #7597de 100%);
        background-attachment: fixed;
    }

    [data-testid="stSidebar"] {
        background: rgba(20, 20, 35, 0.95) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stCheckbox label,
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span {
        color: #e0e0e0 !important;
    }

    /* Style Sidebar Reset Button */
    [data-testid="stSidebar"] .stButton button {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        transition: all 0.2s ease;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255, 75, 75, 0.2) !important;
        border-color: #ff4b4b !important;
        color: #ffffff !important;
    }

    .game-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(45deg, #ff4b4b, #ffffff, #4b9eff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 0px;
        margin-bottom: 0px;
        text-shadow: 0 4px 20px rgba(255, 75, 75, 0.3);
    }
    
    .game-subtitle {
        text-align: center;
        font-size: 1.15rem;
        color: #d1d5db;
        font-weight: 500;
        margin-bottom: 25px;
        letter-spacing: 0.5px;
    }

    .score-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 14px;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        font-size: 1.05rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    </style>
""", unsafe_allow_html=True)


def get_emoji(marker):
    return "❌" if marker == "X" else "⭕"



if "game_id" not in st.session_state:
    st.session_state.game_id = 0
    st.session_state.board = Board()
    st.session_state.game_over = False
    st.session_state.winner = None
    
    # Separate draw scores for AI mode vs Double Player mode
    st.session_state.ai_draw_score = 0
    st.session_state.p_draw_score = 0
    

    st.session_state.human_marker = "X"
    st.session_state.ai_marker = "O"
    st.session_state.human_player = HumanPlayer("X")
    st.session_state.ai_player = AIPlayer("O")
    st.session_state.human_score = 0
    st.session_state.ai_score = 0
    st.session_state.current_player = st.session_state.human_player

    #for double player checkbox
    st.session_state.p1_score = 0
    st.session_state.p2_score = 0
    st.session_state.player1 = HumanPlayer("X")
    st.session_state.player2 = HumanPlayer("O")


with st.sidebar:
    st.header("⚙️ Game Settings")
    
    # checkbox for double player mode
    double_player = st.checkbox("👥 Double Player Mode (2P)", value=False, key="double_player_mode")
        
    st.markdown("---")
    
    if not double_player:
        choice_emoji = st.radio("Choose your marker:", ["❌", "⭕"], index=0, key="marker_choice")
        choice = "X" if choice_emoji == "❌" else "O"
    else:
        st.markdown("### ℹ️ 2P Mode Active")
        st.markdown("• **Player 1**: ❌ (Starts first)\n• **Player 2**: ⭕")
        choice = "X"
    
    if st.button("🔄 Reset Scores & Board", use_container_width=True):
        st.session_state.game_id += 1
        st.session_state.board = Board()
        st.session_state.game_over = False
        st.session_state.winner = None
        
        if double_player:
            st.session_state.p1_score = 0
            st.session_state.p2_score = 0
            st.session_state.p_draw_score = 0
            st.session_state.player1 = HumanPlayer("X")
            st.session_state.player2 = HumanPlayer("O")
            st.session_state.current_player = st.session_state.player1
        else:
            st.session_state.human_score = 0
            st.session_state.ai_score = 0
            st.session_state.ai_draw_score = 0
            st.session_state.human_marker = choice
            st.session_state.ai_marker = "O" if choice == "X" else "X"
            st.session_state.human_player = HumanPlayer(st.session_state.human_marker)
            st.session_state.ai_player = AIPlayer(st.session_state.ai_marker)
            st.session_state.current_player = (
                st.session_state.ai_player if st.session_state.ai_marker == "X" 
                else st.session_state.human_player
            )
        st.rerun()
        
    st.markdown("---")
    if double_player:
        st.markdown("### 👥 2-Player Rules")
        st.markdown("Players take turns placing `❌` and `⭕`.")
    else:
        st.markdown("### 🤖 By Talha")
        st.markdown("Powered by the **Minimax Algorithm**. Can you beat an unbeatable opponent?")



st.markdown('<p class="game-title">Tic-Tac-Toe</p>', unsafe_allow_html=True)
subtitle_text = "Double Player Mode" if double_player else "Classic Strategy • Human vs. Unbeatable AI"
st.markdown(f'<p class="game-subtitle">{subtitle_text}</p>', unsafe_allow_html=True)



sc1, sc2, sc3 = st.columns(3)
if double_player:
    with sc1:
        st.markdown(f'<div class="score-card">Player 1 (❌)<br>🏆 {st.session_state.get("p1_score", 0)}</div>', unsafe_allow_html=True)
    with sc2:
        st.markdown(f'<div class="score-card">Draws<br>🤝 {st.session_state.get("p_draw_score", 0)}</div>', unsafe_allow_html=True)
    with sc3:
        st.markdown(f'<div class="score-card">Player 2 (⭕)<br>🏆 {st.session_state.get("p2_score", 0)}</div>', unsafe_allow_html=True)
else:
    with sc1:
        st.markdown(f'<div class="score-card">You ({get_emoji(st.session_state.human_marker)})<br>🏆 {st.session_state.human_score}</div>', unsafe_allow_html=True)
    with sc2:
        st.markdown(f'<div class="score-card">Draws<br>🤝 {st.session_state.ai_draw_score}</div>', unsafe_allow_html=True)
    with sc3:
        st.markdown(f'<div class="score-card">AI ({get_emoji(st.session_state.ai_marker)})<br>🤖 {st.session_state.ai_score}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# AI move 
if not double_player and not st.session_state.game_over and st.session_state.current_player == st.session_state.ai_player:
    with st.spinner("🤖 AI is doing his move"):
        ai_move = st.session_state.ai_player.get_move(st.session_state.board)
        st.session_state.board.make_move(ai_move, st.session_state.ai_player.marker)
        
        if st.session_state.board.check_winner(st.session_state.ai_player.marker):
            st.session_state.game_over = True
            st.session_state.winner = "AI"
            st.session_state.ai_score += 1
        elif st.session_state.board.is_full():
            st.session_state.game_over = True
            st.session_state.winner = "Draw"
            st.session_state.ai_draw_score = st.session_state.get("ai_draw_score", 0) + 1
        else:
            st.session_state.current_player = st.session_state.human_player
        st.rerun()



if st.session_state.game_over:
    if double_player:
        if st.session_state.winner == "Player 1":
            st.success("🎉 **Player 1 (❌) Won!**")
            st.balloons()
        elif st.session_state.winner == "Player 2":
            st.success("🎉 **Player 2 (⭕) Won!** ")
            st.balloons()
        else:
            st.warning("🤝 **It's a Draw!** Perfectly balanced.")
    else:
        if st.session_state.winner == "AI":
            st.error("🤖 **AI Wins!** The minimax algorithm reigns supreme.")
            st.balloons()
        elif st.session_state.winner == "Human":
            st.success("🎉 **Impossible! How do You Beat the AI!** ")
            st.balloons()
        else:
            st.warning("🤝 **It's a Draw!** Perfectly balanced.")
    
    st.markdown("""
        <style>
        div.stButton > button {
            background: linear-gradient(135deg, #ff4b4b 0%, #ff6b6b 100%) !important;
            color: white !important;
            border: none !important;
            font-weight: 600 !important;
        }
        div.stButton > button:hover {
            background: linear-gradient(135deg, #ff3333 0%, #ff5252 100%) !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("Play Again", use_container_width=True):
        st.session_state.game_id += 1
        st.session_state.board = Board()
        st.session_state.game_over = False
        st.session_state.winner = None

        if double_player:
            st.session_state.player1 = HumanPlayer("X")
            st.session_state.player2 = HumanPlayer("O")
            st.session_state.current_player = st.session_state.player1
        else:
            st.session_state.human_player = HumanPlayer(st.session_state.human_marker)
            st.session_state.ai_player = AIPlayer(st.session_state.ai_marker)
            st.session_state.current_player = (
                st.session_state.ai_player
                if st.session_state.ai_marker == "X"
                else st.session_state.human_player
            )

        st.rerun()
else:
    if double_player:
        p_name = "Player 1" if st.session_state.current_player.marker == "X" else "Player 2"
        turn_text = f"{p_name}'s Turn"
    else:
        turn_text = "Your Turn" if st.session_state.current_player == st.session_state.human_player else "AI's Turn"
    
    current_emoji = get_emoji(st.session_state.current_player.marker)
    st.info(f"👉 **Status:** {turn_text} (`{current_emoji}`)")

st.markdown("<br>", unsafe_allow_html=True)


board_state = st.session_state.board.board


if double_player:
    component_disabled = st.session_state.game_over
else:
    component_disabled = (
        st.session_state.game_over
        or st.session_state.current_player != st.session_state.human_player
    )

board_click = tic_tac_toe_component(
    board=[("" if cell == " " else cell) for cell in board_state],
    human_marker="X" if double_player else st.session_state.human_marker,
    ai_marker="O" if double_player else st.session_state.ai_marker,
    disabled=component_disabled,
    key=f"tic_tac_toe_board_{st.session_state.game_id}",
    default=None,
)

if board_click is not None:
    idx = int(board_click)

    if double_player:
        if (
            0 <= idx < 9
            and board_state[idx] == " "
            and not st.session_state.game_over
        ):
            current_p = st.session_state.current_player
            st.session_state.board.make_move(idx, current_p.marker)

            if st.session_state.board.check_winner(current_p.marker):
                st.session_state.game_over = True
                if current_p.marker == "X":
                    st.session_state.winner = "Player 1"
                    st.session_state.p1_score = st.session_state.get("p1_score", 0) + 1
                else:
                    st.session_state.winner = "Player 2"
                    st.session_state.p2_score = st.session_state.get("p2_score", 0) + 1

            elif st.session_state.board.is_full():
                st.session_state.game_over = True
                st.session_state.winner = "Draw"
                st.session_state.p_draw_score = st.session_state.get("p_draw_score", 0) + 1

            else:
                
                if st.session_state.current_player.marker == "X":
                    st.session_state.current_player = st.session_state.player2
                else:
                    st.session_state.current_player = st.session_state.player1

            st.rerun()

    else:
        if (
            0 <= idx < 9
            and board_state[idx] == " "
            and not st.session_state.game_over
            and st.session_state.current_player == st.session_state.human_player
        ):
            st.session_state.board.make_move(
                idx, st.session_state.human_player.marker
            )

            if st.session_state.board.check_winner(
                st.session_state.human_player.marker
            ):
                st.session_state.game_over = True
                st.session_state.winner = "Human"
                st.session_state.human_score += 1

            elif st.session_state.board.is_full():
                st.session_state.game_over = True
                st.session_state.winner = "Draw"
                st.session_state.ai_draw_score = st.session_state.get("ai_draw_score", 0) + 1

            else:
                st.session_state.current_player = st.session_state.ai_player

                ai_move = st.session_state.ai_player.get_move(
                    st.session_state.board
                )
                st.session_state.board.make_move(
                    ai_move, st.session_state.ai_player.marker
                )

                if st.session_state.board.check_winner(
                    st.session_state.ai_player.marker
                ):
                    st.session_state.game_over = True
                    st.session_state.winner = "AI"
                    st.session_state.ai_score += 1

                elif st.session_state.board.is_full():
                    st.session_state.game_over = True
                    st.session_state.winner = "Draw"
                    st.session_state.ai_draw_score = st.session_state.get("ai_draw_score", 0) + 1

                else:
                    st.session_state.current_player = st.session_state.human_player

            st.rerun()
