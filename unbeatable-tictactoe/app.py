import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

tic_tac_toe_component = components.declare_component(
    "tic_tac_toe_board", path=str(Path(__file__).parent / "frontend")
)
from source.board import Board
from source.player import HumanPlayer, AIPlayer


st.set_page_config(page_title="Classic Unbeatable Tic-Tac-Toe", page_icon="❌", layout="centered")


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

    /* The board is rendered by the custom HTML component. */

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


if "board" not in st.session_state or "human_score" not in st.session_state or "game_id" not in st.session_state:
    st.session_state.game_id = 0
    st.session_state.game_id = 0
    st.session_state.board = Board()
    st.session_state.human_marker = "X"
    st.session_state.ai_marker = "O"
    st.session_state.human_player = HumanPlayer("X")
    st.session_state.ai_player = AIPlayer("O")
    st.session_state.current_player = st.session_state.human_player
    st.session_state.game_over = False
    st.session_state.winner = None

    st.session_state.human_score = 0
    st.session_state.ai_score = 0
    st.session_state.draw_score = 0


with st.sidebar:
    st.header("⚙️ Game Settings")
    choice_emoji = st.radio("Choose your marker:", ["❌", "⭕"], index=0)
    choice = "X" if choice_emoji == "❌" else "O"
    
    if st.button("🔄 Reset Scores & Board", use_container_width=True):
        st.session_state.game_id += 1
        st.session_state.human_score = 0
        st.session_state.ai_score = 0
        st.session_state.draw_score = 0
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
        
    st.markdown("---")
    st.markdown("### 🤖 About AI")
    st.markdown("Powered by the **Minimax Algorithm**. Can you outsmart an unbeatable opponent?")


st.markdown('<p class="game-title">Tic-Tac-Toe</p>', unsafe_allow_html=True)
st.markdown('<p class="game-subtitle">Classic Strategy • Human vs. Unbeatable AI</p>', unsafe_allow_html=True)


sc1, sc2, sc3 = st.columns(3)
with sc1:
    st.markdown(f'<div class="score-card">You ({get_emoji(st.session_state.human_marker)})<br>🏆 {st.session_state.human_score}</div>', unsafe_allow_html=True)
with sc2:
    st.markdown(f'<div class="score-card">Draws<br>🤝 {st.session_state.draw_score}</div>', unsafe_allow_html=True)
with sc3:
    st.markdown(f'<div class="score-card">AI ({get_emoji(st.session_state.ai_marker)})<br>🤖 {st.session_state.ai_score}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


if not st.session_state.game_over and st.session_state.current_player == st.session_state.ai_player:
    with st.spinner("🤖 AI is calculating the best move..."):
        ai_move = st.session_state.ai_player.get_move(st.session_state.board)
        st.session_state.board.make_move(ai_move, st.session_state.ai_player.marker)
        
        if st.session_state.board.check_winner(st.session_state.ai_player.marker):
            st.session_state.game_over = True
            st.session_state.winner = "AI"
            st.session_state.ai_score += 1
        elif st.session_state.board.is_full():
            st.session_state.game_over = True
            st.session_state.winner = "Draw"
            st.session_state.draw_score += 1
        else:
            st.session_state.current_player = st.session_state.human_player
        st.rerun()


if st.session_state.game_over:
    if st.session_state.winner == "AI":
        st.error("🤖 **AI Wins!** The minimax algorithm reigns supreme.")
    elif st.session_state.winner == "Human":
        st.success("🎉 **Incredible! You Beat the AI!** (Legendary move!)")
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
    # Force the custom board component to reset its old click state
        st.session_state.game_id += 1

        st.session_state.board = Board()
        st.session_state.human_player = HumanPlayer(
            st.session_state.human_marker
        )
        st.session_state.ai_player = AIPlayer(
            st.session_state.ai_marker
        )

        st.session_state.current_player = (
            st.session_state.ai_player
            if st.session_state.ai_marker == "X"
            else st.session_state.human_player
        )

        st.session_state.game_over = False
        st.session_state.winner = None

        st.rerun()
else:
    turn_text = "Your Turn" if st.session_state.current_player == st.session_state.human_player else "AI's Turn"
    current_emoji = get_emoji(st.session_state.current_player.marker)
    st.info(f"👉 **Status:** {turn_text} (`{current_emoji}`)")

st.markdown("<br>", unsafe_allow_html=True)


board_state = st.session_state.board.board

# Render a custom HTML/CSS board. The component returns the index (0-8)
# of the clicked cell; Python continues to manage all game logic.
board_click = tic_tac_toe_component(
    board=[("" if cell == " " else cell) for cell in board_state],
    human_marker=st.session_state.human_marker,
    ai_marker=st.session_state.ai_marker,
    disabled=(
        st.session_state.game_over
        or st.session_state.current_player != st.session_state.human_player
    ),
    key=f"tic_tac_toe_board_{st.session_state.game_id}",
    default=None,
)

if board_click is not None:
    idx = int(board_click)

    # Guard against stale or invalid clicks.
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
            st.session_state.draw_score += 1

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
                st.session_state.draw_score += 1

            else:
                st.session_state.current_player = st.session_state.human_player

        st.rerun()
