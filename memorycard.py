import pygame   
import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
import os

BG="#0f0e17"
CARD_BACK="#1a1a2e"
CARD_FRONT="#16213e"
ACCENT="#e94560"
GOLD="#f5a623"
TEXT_LIGHT="#fffffe"
TEXT_DIM="#a7a9be"
MATCHED_BG="#0d3b2e"
MATCHED_FG="#00d084"
SHADOW="#070714"

EMOJIS=["🐉","🦋","🌙","⚡","🔮","🌺","🎯","🚀","🦊","🌊","💎","🎭","🍀","🦄","🌸","🎪","🍎","🍕"]

CARD_W=80
CARD_H=80
GAP=10
PAD=20

class MemoryGame:
    def __init__(self, root):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.root=root
        self.root.title("Memory Quest Deluxe")
        self.root.configure(bg=BG)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("soundtrack.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        
        self.match_sound = pygame.mixer.Sound("bener.wav")
        self.wrong_sound = pygame.mixer.Sound("salah.wav")
        self.win_sound = pygame.mixer.Sound("menang.wav")

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
        else:
            self.cols=4
            self.rows=4

        self.total=self.cols*self.rows

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
        tk.Button(bottom,text="Leaderboard",command=self.show_leaderboard).pack(side="left",padx=5)

    def new_game(self):
        pygame.mixer.stop()                                      # ← tambah ini
        self.click_sound = pygame.mixer.Sound("click.wav")      # ← tambah ini
        self.match_sound = pygame.mixer.Sound("bener.wav")      # ← tambah ini
        self.wrong_sound = pygame.mixer.Sound("salah.wav")      # ← tambah ini
        self.win_sound   = pygame.mixer.Sound("menang.wav")     # ← tambah ini
        pairs=random.sample(EMOJIS,self.total//2)
        self.values=pairs*2
        random.shuffle(self.values)

        self.flipped=[False]*self.total
        self.matched=[False]*self.total
        self.selected=[]
        self.wrong_cards=[]
        self.moves=0
        self.pairs_found=0
        self.locked=False
        self.game_over=False
        

        self.start_time=time.time()

        self.draw_all()
        self.update_labels()
        self.tick()

    def card_xy(self,idx):
        c=idx%self.cols
        r=idx//self.cols
        return PAD+c*(CARD_W+GAP), PAD+r*(CARD_H+GAP)

    def draw_all(self):
        self.canvas.delete("all")
        for i in range(self.total):
            self.draw_card(i)

    def draw_card(self,i):
        x,y=self.card_xy(i)

        face=self.flipped[i] or self.matched[i]

        self.canvas.create_rectangle(
            x+4,y+4,x+CARD_W+4,y+CARD_H+4,
            fill=SHADOW,outline=""
        )

        if i in self.wrong_cards:
            fill = "#ff4d4d"   # merah
        elif self.matched[i]:
            fill = MATCHED_BG
        elif face:
            fill = CARD_FRONT
        else:
            fill = CARD_BACK

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

        self.click_sound.play()

        if len(self.selected)==2:
            self.moves+=1
            a,b=self.selected

            if self.values[a]==self.values[b]:
                self.match_sound.play()
                self.matched[a]=True
                self.matched[b]=True
                self.pairs_found+=1
                self.selected=[]
                self.draw_all()
                self.update_labels()

                if self.pairs_found==self.total//2:
                    self.win()

            else:
                self.wrong_sound.play()
                self.wrong_cards=[a,b]
                self.draw_all()

                self.locked=True
                self.root.after(800,self.hide_selected)

    def hide_selected(self):
        self.wrong_cards=[]

        for i in self.selected:
          self.flipped[i]=False

        self.selected=[]
        self.locked=False
        self.draw_all()

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

    def tick(self):
        if not self.game_over:
            self.elapsed=int(time.time()-self.start_time)
            self.lbl_timer.config(text=f"{self.elapsed}s")
            self.root.after(500,self.tick)

    def update_labels(self):
        self.lbl_moves.config(text=f"Moves: {self.moves}")
        self.lbl_pairs.config(text=f"Pairs: {self.pairs_found}/{self.total//2}")

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

    def win(self):
        self.win_sound.play()
        pygame.time.wait(900)
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
