import tkinter as tk
from typing import Set

class TicTacToeFOL:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe with FOL")
        self.kb: Set[str] = set()
        self.current_player = "X"
        self.game_over = False
        self.player_names = {"X": "", "O": ""}
        self._setup_ui()
        self._init_kb()

    def _init_kb(self):
        """Initialize knowledge base with empty positions and adjacency rules"""
        self.kb = {f"Empty(P{i+1})" for i in range(9)}  # Using set comprehension
        adjacencies = [(1,2), (2,3), (4,5), (5,6), (7,8), (8,9),  # Horizontal
                      (1,4), (4,7), (2,5), (5,8), (3,6), (6,9),  # Vertical
                      (1,5), (5,9), (3,5), (5,7)]  # Diagonal
        
        for p1, p2 in adjacencies:
            self.kb.update({f"Adjacent(P{p1},P{p2})", f"Adjacent(P{p2},P{p1})"})
        self._log("Initial Knowledge Base:", sorted(self.kb))

    def _apply_rules(self, position: str):
        """Apply FOL rules using forward chaining"""
        new_facts = set()
        player = self.current_player
        lines = [["P1","P2","P3"], ["P4","P5","P6"], ["P7","P8","P9"],  # Rows
                ["P1","P4","P7"], ["P2","P5","P8"], ["P3","P6","P9"],  # Cols
                ["P1","P5","P9"], ["P3","P5","P7"]]  # Diagonals

        # Rule 1: Remove empty status
        if all(f in self.kb for f in [f"Occupied({position},{player})", f"Empty({position})"]):
            self.kb.remove(f"Empty({position})")
            self._log(f"Rule 1: {position} is no longer empty")

        # Rules 2 & 3: Check winning conditions
        for line in lines:
            occupied = [pos for pos in line if f"Occupied({pos},{player})" in self.kb]
            empty = [pos for pos in line if f"Empty({pos})" in self.kb]
            
            if len(occupied) == 2 and len(empty) == 1:  # Potential win
                new_facts.add(f"WinningMove({player},{empty[0]})")
                self._log(f"Rule 2: Winning move for {player} at {empty[0]}")
            
            if len(occupied) == 3:  # Win achieved
                new_facts.add(f"Win({player})")
                self._log(f"Rule 3: Win detected for {player}")
                for pos in occupied:
                    self.buttons[int(pos[1])-1].config(bg="yellow")

        self.kb.update(new_facts)

    def _make_move(self, pos: int):
        """Handle move and update game state"""
        if self.game_over:
            self.result_label.config(text="Game Over! Click 'New Game'", fg="red")
            return

        position = f"P{pos + 1}"
        if f"Empty({position})" in self.kb:
            self.kb.add(f"Occupied({position},{self.current_player})")
            self.buttons[pos].config(text=self.current_player, state="disabled")
            self._apply_rules(position)

            if f"Win({self.current_player})" in self.kb:
                self.result_label.config(text=f"🎉 {self.player_names[self.current_player]} Wins! 🎉", fg="green")
                self.game_over = True
            elif not any(f"Empty(P{i+1})" in self.kb for i in range(9)):
                self.result_label.config(text="It's a Draw!", fg="blue")
                self.game_over = True
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.turn_label.config(text=f"{self.player_names[self.current_player]}'s turn ({self.current_player})")

    def _setup_ui(self):
        """Create and configure UI elements"""
        game_frame = tk.Frame(self.window, padx=20, pady=20)
        game_frame.pack(side=tk.LEFT)
        
        # Player names and new game button
        name_frame = tk.Frame(game_frame)
        name_frame.pack(pady=10)
        for i, player in enumerate(["X", "O"]):
            tk.Label(name_frame, text=f"Player {player}:", font=("Arial", 12)).grid(row=0, column=i*2)
            entry = tk.Entry(name_frame, font=("Arial", 12))
            entry.grid(row=0, column=i*2+1, padx=5)
            setattr(self, f"player_{player.lower()}_entry", entry)
        
        tk.Button(name_frame, text="New Game", font=("Arial", 12), 
                 command=self._new_game).grid(row=0, column=4, padx=10)

        self.turn_label = tk.Label(game_frame, text="Enter player names and click 'New Game'",
                                 font=("Arial", 14))
        self.turn_label.pack(pady=5)

        # Game grid
        button_frame = tk.Frame(game_frame)
        button_frame.pack()
        self.buttons = [tk.Button(button_frame, text="", font=("Arial", 24),
                                width=5, height=2, command=lambda p=i: self._make_move(p))
                       for i in range(9)]
        for i, btn in enumerate(self.buttons):
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)

        self.result_label = tk.Label(game_frame, text="", font=("Arial", 16))
        self.result_label.pack(pady=10)

        # Knowledge base log
        log_frame = tk.Frame(self.window, padx=20, pady=20)
        log_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        tk.Label(log_frame, text="Knowledge Base and Inference Steps",
                font=("Arial", 14, "bold")).pack()
        self.log_text = tk.Text(log_frame, width=50, height=30, font=("Courier", 10))
        self.log_text.pack(pady=10)

    def _new_game(self):
        """Start new game after validating player names"""
        names = {p: getattr(self, f"player_{p.lower()}_entry").get().strip() 
                for p in ["X", "O"]}
        if not all(names.values()):
            self.result_label.config(text="Please enter names for both players!", fg="red")
            return

        self.player_names.update(names)
        self.current_player = "X"
        self.game_over = False
        
        for btn in self.buttons:
            btn.config(text="", state="normal", bg="white")
        
        self.result_label.config(text="")
        self.turn_label.config(text=f"{names['X']}'s turn (X)")
        self.log_text.delete(1.0, tk.END)
        self._init_kb()

    def _log(self, header: str, facts: list = None):
        """Log messages or facts to the knowledge base display"""
        self.log_text.insert(tk.END, f"\n{header}\n")
        if facts:
            for fact in facts:
                self.log_text.insert(tk.END, f"• {fact}\n")
        self.log_text.see(tk.END)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToeFOL()
    game.run()