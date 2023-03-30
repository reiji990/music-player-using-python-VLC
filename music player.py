import glob
import os
import tkinter as tk
from tkinter import ttk
import vlc
import datetime
import csv

# カレントディレクトリをこのファイルの絶対パスに変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class MusicPlayer(ttk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # アプリの初期位置座標設定
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width/2)-150)
        y = int((screen_height/2)-50)

        # ウィンドウの初期設定(大きさ、表示位置、アプリタイトル、フォントサイズ)
        master.resizable()
        master.geometry("+{}+{}".format(x,y))
        master.option_add("*font", ("Arial", 20))
        master.title("Music Player using Python-VLC")

        # input_frame作成
        self.input_frame = ttk.Frame(self.master)
        self.input_frame.pack()

        self.style = ttk.Style(self.input_frame)
        self.style.configure("default.TButton", font=(None, 20))

        # input_frame 各ウィジェット追加
        self.artist_label = ttk.Label(self.input_frame, text="Artist")
        self.artist_label.grid(row=0, column=0)

        self.album_label = ttk.Label(self.input_frame, text="Album")
        self.album_label.grid(row=1, column=0)

        self.artist_input = ttk.Entry(self.input_frame)
        self.artist_input.grid(row=0, column=1)

        self.album_input = ttk.Entry(self.input_frame)
        self.album_input.grid(row=1, column=1)

        self.search_button = ttk.Button(self.input_frame, text="Search", width=20, style="default.TButton", command=self._search_button_clicked)
        self.search_button.grid(row=2, column=0, columnspan=2)
    
    # search_buttonのイベント作成
    def _search_button_clicked(self):
        artist = self.artist_input.get()
        album = self.album_input.get()
        music_folder = open("musicfolderpath.txt", mode="r", encoding="utf_8_sig").read()
        self.path = os.path.join(music_folder, f"*{artist}*/*{album}*/*.flac")
        self.input_frame.pack_forget()
        self._create_play_frame()

    # play_frame作成
    def _create_play_frame(self):
        self.play_frame = ttk.Frame(self.master)
        self.play_frame.pack()

        # 音楽再生
        print(self.path)
        self.flac_files = sorted(glob.glob(self.path))
        self.media_list = vlc.MediaList(self.flac_files)
        self.media_instance = vlc.Instance('--no-xlib')
        self.media_player = vlc.MediaListPlayer()
        self.media_player.set_media_list(self.media_list)
        self.media_player.set_playback_mode(vlc.PlaybackMode.loop)
        self.media_player.play()

        # album.csv作成
        self.all_folder_names = sorted({os.path.dirname(flac_file) for flac_file in self.flac_files})

        with open("album.csv", mode="w", encoding="utf_8_sig", newline="") as album_list:
            album_list_writer = csv.writer(album_list)
            for i, folder_name in enumerate(self.all_folder_names):
                album_list_writer.writerow([i+1, folder_name])

        # playlist.csv作成
        self.file_names = [os.path.basename(flac_file) for flac_file in self.flac_files]

        with open("playlist.csv", mode="w", encoding="utf_8_sig", newline="") as playlist:
            playlist_writer = csv.writer(playlist)
            for i, file_name in enumerate(self.file_names):
                playlist_writer.writerow([i+1, file_name])

        self.style = ttk.Style(self.play_frame)
        self.style.configure("default.TButton")
        
        # play_frameのウィジェット作成
        self.selectnum = ttk.Entry(self.play_frame, width=5)
        self.selectnum.grid(row=1, column=2)

        self.select_button = ttk.Button(self.play_frame, text="Select", command=self.select_button_clicked)
        self.select_button.grid(row=1, column=3)

        self.album_button = ttk.Button(self.play_frame, text="Album", command=self.album_button_clicked)
        self.album_button.grid(row=1, column=0)

        self.back_button = ttk.Button(self.play_frame, text="<<", command=self.back_button_clicked)
        self.back_button.grid(row=2, column=0)

        self.playlist_button = ttk.Button(self.play_frame, text="Playlist", command=self.playlist_button_clicked)
        self.playlist_button.grid(row=1, column=1)

        self.playpause_button = ttk.Button(self.play_frame, text="Play / Pause", command=self.pause_button_clicked)
        self.playpause_button.grid(row=2, column=1)

        self.next_button = ttk.Button(self.play_frame, text=">>", command=self.next_button_clicked)
        self.next_button.grid(row=2, column=2)

        self.return_button = ttk.Button(self.play_frame, text="Return", command=self.return_button_clicked)
        self.return_button.grid(row=0, column=3)

        self.infolabel = tk.Message(self.play_frame, width=400)
        self.infolabel.grid(row=4, column=0, columnspan=4)

        self.timelabel = tk.Message(self.play_frame, font=("Arial",15), width=80, anchor=tk.E)
        self.timelabel.grid(row=3, column=3)
        self.timelabel["text"] = f"/"

        self.listlabel = tk.Message(self.play_frame, width=350)
        self.listlabel.grid(row=5, column=0, columnspan=4)

        x = self.media_player.get_media_player().get_media()
        index = self.media_list.index_of_item(x)
        self.infolabel["text"] = f"{index+1}. {self.file_names[index]}"

        self.volume_scale = ttk.Scale(self.play_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda x: self.media_player.get_media_player().audio_set_volume(int(float(x))))
        self.volume_scale.set(100)
        self.volume_scale.grid(row=2, column=3)

        self.progress_bar = ttk.Progressbar(self.play_frame, orient="horizontal", length=250, mode="determinate")
        self.progress_bar.grid(row=3, column=0, columnspan=3)
        self.update()

        # プログレスバー、秒数表示の更新
    def update(self):
        value = self.media_player.get_media_player().get_time()
        maximum = self.media_player.get_media_player().get_length()
        self.progress_bar["value"] = value
        self.progress_bar["maximum"] = maximum

        x = self.media_player.get_media_player().get_media()
        index = self.media_list.index_of_item(x)
        self.infolabel["text"] = f"{index+1}. {self.file_names[index]}"

        Converted_Value = datetime.time(hour=int(value/1000//3600%60), minute=int(value/1000//60%60), second=value//1000%60)
        Converted_Maximum = datetime.time(hour=int(maximum/1000//3600%60), minute=int(maximum/1000//60%60), second=maximum//1000%60)
        
        self.timelabel["text"] = f"{Converted_Value} / {Converted_Maximum}"
        self.after(200, self.update)

    # play_frameの各ウィジェットのイベント追加
    def select_button_clicked(self):
        track = int(float(self.selectnum.get()))
        self.selectnum.delete(0, tk.END)
        self.media_player.play_item_at_index(track-1)
        self.listlabel["text"] = ""

    def album_button_clicked(self):
        with open("album.csv", "r", encoding="utf_8_sig") as f:
            data = f.read()
            self.listlabel["text"] = data

    def playlist_button_clicked(self):
        with open("playlist.csv", "r", encoding="utf_8_sig") as f:
            data = f.read()
            self.listlabel["text"] = data.replace('\"','')

    def back_button_clicked(self):
        self.media_player.previous()
        self.listlabel["text"] = ""

    def next_button_clicked(self):
        self.media_player.next()
        self.listlabel["text"] = ""

    def pause_button_clicked(self):
        self.media_player.pause()
        self.listlabel["text"] = ""

    def return_button_clicked(self):
        self.media_player.stop()
        self.play_frame.pack_forget()
        self.input_frame.pack()

if __name__ == "__main__":
    gui = tk.Tk()
    app = MusicPlayer(master=gui)
    app.mainloop()
