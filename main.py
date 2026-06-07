# =====================
# KETUA
# =====================

def __init__(self, root: tk.Tk):
    self.root = root
    self.root.title("✦ Memory Quest ✦")
    self.root.configure(bg=BG)
    self.root.resizable(False, False)

    self._build_ui()
    self._new_game()


def _new_game(self):
    pairs = random.sample(EMOJIS, TOTAL // 2)
    self.values = pairs * 2
    random.shuffle(self.values)

    self.flipped   = [False] * TOTAL
    self.matched   = [False] * TOTAL
    self.selected  = []

    self.moves = 0
    self.pairs_found = 0

    self.locked = False

    self.start_time = time.time()
    self.elapsed = 0
    self.game_over = False

    self._update_labels()
    self._draw_all()
    self._tick()


def _win(self):
    self.game_over = True

    self.elapsed = int(
        time.time() - self.start_time
    )

    rating = (
        "⭐⭐⭐"
        if self.moves <= 18
        else (
            "⭐⭐"
            if self.moves <= 26
            else "⭐"
        )
    )

    msg = (
        f"🎉  Selamat!  🎉\n\n"
        f"Kamu menyelesaikan game dalam\n"
        f"{self.moves} gerakan  ·  "
        f"{self.elapsed} detik\n\n"
        f"Rating: {rating}"
    )

    self.root.after(
        400,
        lambda: messagebox.showinfo(
            "Victory!",
            msg
        )
    )


def _tick(self):

    if not self.game_over:

        self.elapsed = int(
            time.time() -
            self.start_time
        )

        self.lbl_timer.config(
            text=f"⏱ {self.elapsed}s"
        )

        self.root.after(
            500,
            self._tick
        )


def _update_labels(self):

    self.lbl_moves.config(
        text=f"Moves: {self.moves}"
    )

    self.lbl_pairs.config(
        text=f"Pairs: "
             f"{self.pairs_found}/"
             f"{TOTAL // 2}"
    )


# =====================
# ENTRY POINT
# =====================

if __name__ == "__main__":

    root = tk.Tk()

    MemoryGame(root)

    root.mainloop()
