import tkinter as tk
import threading

class GUI(tk.Frame):
    def __init__(self,master = None):
        super().__init__(master)
        self.master = master
        master.geometry("300x300")
        master.title("Test")

        self.count = 0 # labelに定義する値のバッファ

        self.test = tk.Frame(self.master)# 必要ないっちゃないですが、画面を管理するために一旦別フレームを生成しています。
        self.test.pack()
        self.label = tk.Label(self.test)
        self.label.pack()
        self.label["text"] = str(self.count) # labelの値を初期化

        self.timeEvent()# タイマー起動

    # タイマー起動用関数
    def timeEvent(self):
        th = threading.Thread(target=self.update)# スレッドインスタンス生成
        th.start()# スレッドスタート
        self.after(1000, self.timeEvent)# ここで、再帰的に関数を呼び出す

    # スレッド処理実体
    def update(self):
        self.count += 1
        print(self.count) # デバッグメッセージ
        self.label["text"] = str(self.count) # labelの値を更新      

if __name__ == "__main__":
    gui = tk.Tk()
    app = GUI(master = gui)
    app.mainloop()

