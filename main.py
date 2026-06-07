import tkinter as tk
from tkinter import messagebox
import time

class MemoryGame:

    def __init__(self, root):
        self.root = root
        self.root.title("✦ Memory Quest ✦")

        # dari Orang 5
        self.player_name = self.ask_player_name()
        self.choose_difficulty()

        # dari Orang 2
        self._build_ui()

        # dari Orang 3
        self._new_game()

    # =====================
    # TIMER
    # =====================

    def _tick(self):
        if not self.game_over:
            self.elapsed = int(
                time.time() - self.start_time
            )

            self.lbl_timer.config(
                text=f"⏱ {self.elapsed}s"
            )

            self.root.after(
                500,
                self._tick
            )

    # =====================
    # UPDATE LABEL
    # =====================

    def _update_labels(self):

        self.lbl_moves.config(
            text=f"Moves: {self.moves}"
        )

        self.lbl_pairs.config(
            text=f"Pairs: {self.pairs_found}/{self.total//2}"
        )

    # =====================
    # WIN CONDITION
    # =====================

    def _win(self):

        self.game_over = True

        self.elapsed = int(
            time.time() - self.start_time
        )

        # dari Orang 4
        self.save_score()

        if self.moves <= 18:
            rating = "⭐⭐⭐"

        elif self.moves <= 26:
            rating = "⭐⭐"

        else:
            rating = "⭐"

        messagebox.showinfo(
            "Victory!",
            f"🎉 Selamat {self.player_name}!\n\n"
            f"Waktu : {self.elapsed} detik\n"
            f"Moves : {self.moves}\n"
            f"Rating : {rating}"
        )

    # =====================
    # TESTING
    # =====================

    def reset_game(self):

        self.moves = 0
        self.elapsed = 0
        self.game_over = False

        self._new_game()

# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":

    root = tk.Tk()

    game = MemoryGame(root)

    root.mainloop()
