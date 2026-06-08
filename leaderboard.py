 def save_score(self):
        score=max(1,1000-(self.moves*10+self.elapsed))

        with open("leaderboard.txt","a",encoding="utf-8") as f:
            f.write(f"{self.player_name}|{score}|{self.elapsed}|{self.moves}\n")

  def show_leaderboard(self):
        if not os.path.exists("leaderboard.txt"):
            messagebox.showinfo("Leaderboard","Belum ada skor.")
            return

        data=[]

        with open("leaderboard.txt","r",encoding="utf-8") as f:
            for line in f:
                try:
                    name,score,t,m=line.strip().split("|")
                    data.append((name,int(score),t,m))
                except:
                    pass

        data.sort(key=lambda x:x[1],reverse=True)

        text="🏆 TOP 5 PLAYER\n\n"

        for i,row in enumerate(data[:5],1):
            text+=f"{i}. {row[0]} | Score {row[1]} | {row[2]}s | {row[3]} moves\n"

        messagebox.showinfo("Leaderboard",text)

