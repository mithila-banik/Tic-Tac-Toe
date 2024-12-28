# **Tic-Tac-Toe with First Order Logic (FOL)**
A Python implementation of the classic Tic-Tac-Toe game enhanced with First Order Logic for move validation and win detection. This project demonstrates the application of logical reasoning in game development using a knowledge base system.
# **Features**

Graphical user interface built with Tkinter
First Order Logic (FOL) implementation for game rules and win detection
Real-time knowledge base updates and visualization
Two-player gameplay with custom player names
Visual highlighting of winning combinations
Detailed logging of logical inferences and game state changes

# **Requirements**

Python 3.6+
tkinter (usually comes with Python installation)
typing module

# **Installation**

Clone this repository:

git clone https://github.com/yourusername/tictactoe-fol.git
cd tictactoe-fol

Run the game:

python tictactoe_fol.py

# **How It Works**
# **Knowledge Base System**
The game uses a First Order Logic knowledge base to maintain and reason about the game state. The knowledge base contains facts about:

Empty positions: Empty(Px) where x is the position number
Occupied positions: Occupied(Px,Player) where Player is either X or O
Adjacent positions: Adjacent(Px,Py) for connected positions
Winning moves: WinningMove(Player,Px) for potential winning positions
Win states: Win(Player) when a player has won

# **Logical Rules**
The game implements several logical rules:

**Position Occupancy Rule** : When a position becomes occupied, it's no longer empty
**Winning Move Detection**: Identifies potential winning moves when a player has two positions in a line
**Win Detection**: Determines when a player has won by occupying three positions in a line

# **Class Structure**
# **TicTacToeFOL**
Main game class with the following key methods:

__init__(): Initializes the game window and knowledge base
_init_kb(): Sets up initial knowledge base facts
_apply_rules(): Applies logical rules after each move
_make_move(): Handles player moves and game state updates
_setup_ui(): Creates the graphical interface
_new_game(): Resets the game state
_log(): Updates the knowledge base display

# **Game Interface**
The interface consists of:

Player name input fields
New Game button
3x3 game grid
Turn indicator
Result display
Knowledge base log showing logical inferences

# **How to Play** 

Enter names for both players (X and O)
Click "New Game" to start
Players take turns clicking empty squares to make moves
The game automatically detects wins and draws
Watch the knowledge base log to see the logical reasoning behind each move

# **Project Structure**

tictactoe-fol/
│
├── tictactoe_fol.py    # Main game implementation
├── README.md           # This file
└── requirements.txt    # Project dependencies

# **Acknowledgments**

Inspired by classical AI approaches to game theory
Built with Python and Tkinter
Uses First Order Logic concepts for game reasoning
