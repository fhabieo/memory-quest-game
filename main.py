class MemoryGame:
    def __init__(self, root):
        self.root=root
        self.root.title("Memory Quest Deluxe")
        self.root.configure(bg=BG)

        self.player_name=simpledialog.askstring("Nama Pemain","Masukkan nama pemain:")
        if not self.player_name:
            self.player_name="Player"

        self.choose_difficulty()
        self.build_ui()
        self.new_game()

    def choose_difficulty(self):
        diff=simpledialog.askstring(
            "Difficulty",
            "Pilih:\nEasy\nMedium\nHard"
        )

        diff=(diff or "easy").lower()

        if diff=="hard":
            self.cols=6
            self.rows=6
        elif diff=="medium":
            self.cols=5
            self.rows=4
            
     def new_game(self):
        pairs=random.sample(EMOJIS,self.total//2)
        self.values=pairs*2
        random.shuffle(self.values)

        self.flipped=[False]*self.total
        self.matched=[False]*self.total
        self.selected=[]

        self.moves=0
        self.pairs_found=0
        self.locked=False
        self.game_over=False

        self.start_time=time.time()

        self.draw_all()
        self.update_labels()
        self.tick()
        else:
            self.cols=4
            self.rows=4

        self.total=self.cols*self.rows
         
     def tick(self):
        if not self.game_over:
            self.elapsed=int(time.time()-self.start_time)
            self.lbl_timer.config(text=f"{self.elapsed}s")
            self.root.after(500,self.tick)

    def update_labels(self):
        self.lbl_moves.config(text=f"Moves: {self.moves}")
        self.lbl_pairs.config(text=f"Pairs: {self.pairs_found}/{self.total//2}")

    def win(self):
        self.game_over=True
        self.elapsed=int(time.time()-self.start_time)

        self.save_score()

        score=max(1,1000-(self.moves*10+self.elapsed))

        messagebox.showinfo(
            "Menang!",
            f"Selamat {self.player_name}!\n\n"
            f"Waktu : {self.elapsed}s\n"
            f"Moves : {self.moves}\n"
            f"Score : {score}"
        )

if __name__=="__main__":
    root=tk.Tk()
    MemoryGame(root)
    root.mainloop()
    
