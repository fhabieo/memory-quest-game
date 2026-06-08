 def card_xy(self,idx):
        c=idx%self.cols
        r=idx//self.cols
        return PAD+c*(CARD_W+GAP), PAD+r*(CARD_H+GAP)
   
  def idx_from_pos(self,x,y):
        for i in range(self.total):
            cx,cy=self.card_xy(i)
            if cx<=x<=cx+CARD_W and cy<=y<=cy+CARD_H:
                return i
        return None

  def on_click(self,event):
        if self.locked or self.game_over:
            return

        i=self.idx_from_pos(event.x,event.y)

        if i is None or self.flipped[i] or self.matched[i]:
            return

        self.flipped[i]=True
        self.selected.append(i)
        self.draw_card(i)

        if len(self.selected)==2:
            self.moves+=1
            a,b=self.selected

            if self.values[a]==self.values[b]:
                self.matched[a]=True
                self.matched[b]=True
                self.pairs_found+=1
                self.selected=[]

                if self.pairs_found==self.total//2:
                    self.win()
            else:
                self.locked=True
                self.root.after(800,self.hide_selected)

            self.update_labels()

    def hide_selected(self):
        for i in self.selected:
            self.flipped[i]=False

        self.selected=[]
        self.locked=False
        self.draw_all()
