def build_ui(self):
        top=tk.Frame(self.root,bg=BG)
        top.pack(fill="x",padx=10,pady=10)

        self.lbl_name=tk.Label(
            top,text=f"👤 {self.player_name}",
            bg=BG,fg=TEXT_LIGHT,font=("Arial",12,"bold")
        )
        self.lbl_name.pack(side="left")

        self.lbl_moves=tk.Label(top,text="Moves: 0",bg=BG,fg=TEXT_LIGHT)
        self.lbl_moves.pack(side="right",padx=10)

        self.lbl_timer=tk.Label(top,text="0s",bg=BG,fg=GOLD)
        self.lbl_timer.pack(side="right")

        self.lbl_pairs=tk.Label(top,text="Pairs: 0",bg=BG,fg=TEXT_LIGHT)
        self.lbl_pairs.pack(side="right",padx=10)

        w=self.cols*(CARD_W+GAP)+PAD
        h=self.rows*(CARD_H+GAP)+PAD

        self.canvas=tk.Canvas(self.root,width=w,height=h,bg=BG,highlightthickness=0)
        self.canvas.pack()

        self.canvas.bind("<Button-1>",self.on_click)

        bottom=tk.Frame(self.root,bg=BG)
        bottom.pack(pady=10)

        tk.Button(bottom,text="New Game",command=self.new_game).pack(side="left",padx=5)
        tk.Button(bottom,text="Reveal All",command=self.cheat).pack(side="left",padx=5)

  def draw_all(self):
        self.canvas.delete("all")
        for i in range(self.total):
            self.draw_card(i)
        tk.Button(bottom,text="Leaderboard",command=self.show_leaderboard).pack(side="left",padx=5)
    
  def draw_card(self,i):
        x,y=self.card_xy(i)

        face=self.flipped[i] or self.matched[i]

        self.canvas.create_rectangle(
            x+4,y+4,x+CARD_W+4,y+CARD_H+4,
            fill=SHADOW,outline=""
        )

        fill=MATCHED_BG if self.matched[i] else (CARD_FRONT if face else CARD_BACK)

        self.canvas.create_rectangle(
            x,y,x+CARD_W,y+CARD_H,
            fill=fill,outline=GOLD,width=2
        )

        if face:
            self.canvas.create_text(
                x+CARD_W//2,
                y+CARD_H//2,
                text=self.values[i],
                font=("Segoe UI Emoji",24)
            )
        else:
            self.canvas.create_text(
                x+CARD_W//2,
                y+CARD_H//2,
                text="?",
                fill="#4444aa",
                font=("Arial",22,"bold")
            )

