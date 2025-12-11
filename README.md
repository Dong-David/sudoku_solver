# 🎄 Sudoku Noel Edition ❄️

Welcome to **Sudoku Noel Edition**! This is a festive, holiday-themed version of the classic Sudoku puzzle game, built using **Python** and **Pygame**.

The game features a warm Christmas atmosphere with falling snow, a glassmorphism UI, wooden button textures, and a smart auto-solver.

![Sudoku Demo](https://github.com/user-attachments/assets/274f000f-2131-4901-a2fd-46ff6f47244b)
*(Screenshot placeholder)*

---

## ✨ Key Features

* **Festive Atmosphere:**
    * Christmas tree background.
    * Continuous **Snowfall Animation**.
    * Modern **Glassmorphism** grid design (transparent glass effect).
    * **Wood Texture** buttons for a cozy feel.

* **Smart Error Detection (New):**
    * **Real-time Validation:** If you enter a number that conflicts with the row, column, or 3x3 box, it will immediately turn **Crimson Red** to alert you.
    * Valid numbers appear in Blue or Gray depending on the state.

* **Two Game Modes:**
    * **Player Mode:** The game generates a random, solvable puzzle for you.
    * **Input Mode:** Allows you to input a puzzle from a newspaper or book to let the computer solve it.

* **Visual Solver:**
    * Watch the computer solve the puzzle in real-time using the **Backtracking Algorithm**.
    * Includes an optimized speed-up feature (frame skipping) so you don't have to wait too long.

## 🛠️ Prerequisites & Installation

To play this game, you need Python installed on your computer.

1.  **Install Python:** Download it from [python.org](https://www.python.org/).
2.  **Install Pygame:** Open your Terminal (macOS/Linux) or Command Prompt (Windows) and run:
    ```bash
    pip install pygame==2.5.2 opencv-python==4.10.0.84 numpy==1.26.4 Pillow==10.3.0 imutils==0.5.4 easyocr
    ```

---

## 📂 File Structure (Important)

For the game to load textures and fonts correctly, ensure your folder looks exactly like this:

```text
Sudoku-Noel/
├── main.py            # The main game script
├── 1295969.jpg        # Background image (Christmas Tree)
├── 428228.jpg         # Wood texture image (For buttons)
├── Playwrite.ttf      # Custom font file
└── README.md          # This documentation
```

> **Note:** If the images or font are missing, the game will still run using default colors and system fonts.

## 🚀 How to Run

1. Navigate to the game folder in your Terminal/Command Prompt.
2. Run the following command:

```bash
python main.py
```

---

## 🎮 Controls

### Mouse & Keyboard
* **Left Click:** Select a cell or click buttons.
* **Number Keys (1-9):** Fill the selected cell with a number.
* **Arrow Keys:** Move the selection highlight (Up, Down, Left, Right).
* **Backspace / Delete / 0:** Clear the number in the selected cell.

### Buttons
* **New Game:** Generates a fresh, random board.
* **Input Mode:** Clears the board so you can enter your own custom puzzle.
* **Solve Now:** Triggers the AI to auto-solve the current board.
* **Reset:** Resets the board to its initial state (removes player inputs).

---

## 🧠 The Algorithm

This project utilizes the **Backtracking Algorithm** to solve Sudoku grids:

1. Finds the first empty cell.
2. Attempts to place numbers 1 through 9.
3. Checks validity against the Row, Column, and 3x3 Box.
4. Recursively moves to the next cell.
5. If a dead-end is reached, it backtracks to the previous cell and tries the next number.

---
**Enjoy the game and Merry Christmas! 🎅🎄**
