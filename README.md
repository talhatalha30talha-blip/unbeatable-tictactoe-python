# ❌ Tic-Tac-Toe (Unbeatable AI with Minimax Algorithm) ⭕

A classic console-based Tic-Tac-Toe game built in **Python** where you can play against an **unbeatable AI opponent** powered by the **Minimax algorithm**. No matter how well you play, the best you can achieve is a draw!

---

## 🚀 Features

* **Unbeatable AI:** Utilizes the recursive Minimax decision-making algorithm to evaluate all possible future moves, ensuring the AI never loses.
* **Interactive Gameplay:** Prompts the user to choose their preferred marker (`X` or `O`) and handles turn orders seamlessly.
* **Input Validation:** Robust error handling for invalid inputs or spaces that are already taken.
* **Object-Oriented Design:** Clean and modular code structure separating the game board, base players, human logic, and AI logic.

---

## 🛠️ Code Structure

* `Board`: Manages the state of the 9-cell grid, checks for winning conditions, tracks full boards, and handles valid moves.
* `Player`: Base class for players.
* `HumanPlayer`: Handles console input and translates it to valid board indices.
* `AIPlayer`: Implements the Minimax decision engine to calculate the optimal next move.

---

## ⚙️ Prerequisites

Make sure you have **Python 3.x** installed on your machine. You can verify it by running:
```bash
python --version



🎮 How to Run the GameClone this repository or download the tictactoe.py file:Bashgit clone [https://github.com/YOUR-USERNAME/unbeatable-tictactoe-python.git](https://github.com/talhatalha30talha/unbeatable-tictactoe-python.git)
cd unbeatable-tictactoe-python
Run the script using your terminal or command prompt:Bashpython tictactoe.py
Follow the on-screen prompts to choose your marker (X or O) and enter numbers from 1 to 9 to make your moves.🧠 How the Minimax Algorithm WorksThe AI looks ahead at all potential game states recursively:If the AI wins, it receives a positive score ($10 - depth$).If the human wins, it receives a negative score ($depth - 10$).If the board is full with no winner, it results in a score of 0 (Draw).
The AI acts as the maximizing player trying to get the highest score, while anticipating that the human will play as the minimizing player trying to block it.📄 LicenseThis project is open-source and available under the MIT License.
