# 🎄 Christmas Sudoku Solver ❄️

Welcome to **Christmas Sudoku**! This is a festive version of the classic puzzle game, featuring a warm holiday theme, falling snow animation, and an intelligent auto-solver. Built with **Python** and **Pygame**.

<img width="534" height="721" alt="Screenshot 2025-12-04 at 10 02 21" src="https://github.com/user-attachments/assets/274f000f-2131-4901-a2fd-46ff6f47244b" />

## ✨ Key Features

* **Festive Atmosphere:** Holiday color palette (Red, Green, Gold) and continuous **Snowfall Animation**.
* **Two Game Modes:**
    * **Player Mode:** The game generates a random Sudoku board for you to solve.
    * **Input Mode:** Enter your own puzzle (from a newspaper or book) and let the computer solve it.
* **Visual Backtracking Solver:** Watch the computer solve the puzzle in real-time using a backtracking algorithm (with optimized frame-skipping for speed).
* **Game Utilities:**
    * Live Timer.
    * Error detection (invalid moves turn red).
    * **New Game** generator.

## 🛠️ Installation & Setup

To play the game, you need to have Python installed on your computer.

1.  **Install Python:** Download from [python.org](https://www.python.org/).
2.  **Install Pygame:** Open your Terminal or Command Prompt and run:
    ```bash
    pip install pygame
    ```

## 🚀 How to Run

1.  Ensure both `main.py` and the font file `PlaywriteNO-VariableFont_wght.ttf` are in the **same folder**.
2.  Run the script:
    ```bash
    python main.py
    ```

## 🎮 Controls

### Keyboard & Mouse
* **Left Click:** Select a cell or click buttons.
* **Number Keys (1-9):** Fill the selected cell.
* **Backspace / Delete:** Clear the selected cell.

### Buttons
* **New Game:** Generates a fresh, random board.
* **Reset:** Clears all numbers you have entered, resetting the board to its initial state.
* **Solve Now:** Triggers the AI to auto-solve the current board.
* **Mode: Player/Input:** Toggles between playing yourself or inputting a custom board.

## 🧠 The Algorithm

This project uses the **Backtracking Algorithm** to solve the Sudoku grid:
1.  Finds an empty cell.
2.  Tries numbers 1-9.
3.  Checks validity (row, column, 3x3 box).
4.  Recursively moves to the next cell.
5.  If a dead-end is reached, it backtracks to the previous cell and tries the next number.

*Note: The visualization includes a frame-skipping technique to ensure the animation is smooth and doesn't take too long to finish.*

## 📂 File Structure

```text
Sudoku-Christmas/
├── main.py                           # Main game source code
├── PlaywriteNO-VariableFont_wght.ttf # Custom Christmas font
└── README.md                         # Documentation
