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
        else:
            self.cols=4
            self.rows=4

        self.total=self.cols*self.rows

  def cheat(self):
        for i in range(self.total):
            self.flipped[i]=True

        self.draw_all()
        self.root.after(1500,self.restore_cheat)

  def restore_cheat(self):
        for i in range(self.total):
            if not self.matched[i]:
                self.flipped[i]=False
        self.draw_all()
