"""A Bingo game built with Python and Tkinter."""
import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

DEFAULT_MAP = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25];

CHECK_MAP = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];

class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

BOARD_SIZE = 5

DEFAULT_PLAYERS = (
    Player(label="You", color="blue"),
    Player(label="Enemy", color="green"),
)

class BingoGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self._current_moves = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]

    def toggle_player(self):
        """Return a toggled player."""
        self.current_player = next(self._players)

    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        return move_was_not_played

class BingoBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=25)
            self.columnconfigure(row, weight=1, minsize=25)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text=DEFAULT_MAP[row*5 + col],
                    font=font.Font(size=25),
                    fg="black",
                    width=4,
                    height=2,
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def play(self, event):
        """Handle a player's move."""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if CHECK_MAP[row*5 + col] == 0:
            CHECK_MAP[row*5 + col] = 1;
            if self._game.is_valid_move(move):
                self._update_button(clicked_btn)
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)
            else:
                pass
        else:
            msg = "Vi tri da duoc danh dau"
            self._update_display(msg)



    def _update_button(self, clicked_btn):
        clicked_btn.config(fg="red")


    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="1")
            button.config(fg="black")

def main():
    """Create the game's board and run its main loop."""
    game = BingoGame()
    board = BingoBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()
