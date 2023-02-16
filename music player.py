import glob
import gc
import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk
import vlc

# カレントディレクトリをこのファイルの絶対パスに変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class MusicPlayer(ttk.Frame):
    """A music player GUI built using Python-VLC."""

    def __init__(self, master=None):
        """Initialize the music player."""
        super().__init__(master)
        self.master = master

        # ウィンドウの初期設定(大きさ、表示位置、アプリタイトル、フォントサイズ)
        master.resizable(1000, 1000)
        master.geometry("+2200+500")
        master.title("Music Player using Python-VLC")
        master.option_add("*font", ("", 20))

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

        self.play_button = ttk.Button(self.input_frame, text="Play", width=20, style="default.TButton", command=self._play_button_clicked)
        self.play_button.grid(row=2, column=0, columnspan=2)

    # play_buttonのイベント作成
    def _play_button_clicked(self):
        artist = self.artist_input.get()
        album = self.album_input.get()
        music_folder = open("musicfolderpath.txt", mode="r").read()
        path = os.path.join(music_folder, f"*{artist}*/*{album}*/*.flac")
        with open("path.txt", mode="w", encoding="utf-8") as file:
            file.write(path)

        self.input_frame.destroy()
        self._create_play_frame()

    # play_frame作成
    def _create_play_frame(self):
        self.play_frame = ttk.Frame(self.master)
        self.play_frame.pack()

        # 音楽再生
        path = open("path.txt", mode="r").read()
        print(path)
        self.flac_files = sorted(glob.glob(path))
        self.media_list = vlc.MediaList(self.flac_files)
        self.media_player = vlc.MediaListPlayer()
        self.media_player.set_media_list(self.media_list)
        self.media_player.set_playback_mode(vlc.PlaybackMode.loop)
        self.media_player.play()

        # album.txtクリア
        with open("album.txt", mode="w", encoding="utf-8"):
            pass

        # album.txt作成
        self.all_folder_names = sorted({os.path.dirname(flac_file) for flac_file in self.flac_files})

        with open("album.txt", mode="a", encoding="utf-8") as album_list:
            for i, folder_name in enumerate(self.all_folder_names):
                album_list.write(f"{i+1}. {folder_name}\n")

        # playlist.txtクリア
        with open("playlist.txt", mode="w", encoding="utf-8"):
            pass 

        # playlist.txt作成
        self.file_names = [os.path.basename(flac_file) for flac_file in self.flac_files]

        with open("playlist.txt", mode="a", encoding="utf-8") as playlist:
            for i, file_name in enumerate(self.file_names):
                playlist.write(f"{i+1}. {file_name}\n")
        
        self.style = ttk.Style(self.play_frame)
        self.style.configure("default.TButton", font=(None, 20))
        
        # play_frameのウィジェット作成
        self.selectnum = ttk.Entry(self.play_frame, width=5)
        self.selectnum.grid(row=0, column=0)

        self.select_button = ttk.Button(self.play_frame, text="Select", command=self.select_button_clicked)
        self.select_button.grid(row=0, column=1)

        self.album_button = ttk.Button(self.play_frame, text="Album", command=self.album_button_clicked)
        self.album_button.grid(row=1, column=0)

        self.back_button = ttk.Button(self.play_frame, text="Back", command=self.back_button_clicked)
        self.back_button.grid(row=2, column=0)

        self.playlist_button = ttk.Button(self.play_frame, text="Playlist", command=self.playlist_button_clicked)
        self.playlist_button.grid(row=1, column=1)

        self.playpause_button = ttk.Button(self.play_frame, text="Play / Pause", command=self.pause_button_clicked)
        self.playpause_button.grid(row=2, column=1)

        self.next_button = ttk.Button(self.play_frame, text="Next", command=self.next_button_clicked)
        self.next_button.grid(row=2, column=2)

        self.quit_button = ttk.Button(self.play_frame, text="Quit", command=self.quit_button_clicked)
        self.quit_button.grid(row=2, column=3)

        self.infolabel = tk.Message(self.play_frame, width=400)
        self.infolabel.grid(row=3, column=0, columnspan=4)
        
        x = self.media_player.get_media_player().get_media()
        index = self.media_list.index_of_item(x)
        self.infolabel["text"] = f"{index+1}. {self.file_names[index]}"

# test用のfilelist表示ボタン(リリース前に削除する)
        self.file_list_button = ttk.Button(self.play_frame, text="filelist", command=self.filelist_clicked)
        self.file_list_button.grid(row=1, column=3)

    def filelist_clicked(self):
        with open("album.txt", "r") as f:
            data = f.read()
            self.infolabel["text"] = self.flac_files

    # play_frameの各ウィジェットのイベント追加
    def select_button_clicked(self):
        track = int(self.selectnum.get())
        self.selectnum.delete(0, tk.END)
        self.media_player.play_item_at_index(track-1)
        x = self.media_player.get_media_player().get_media()
        index = self.media_list.index_of_item(x)
        self.infolabel["text"] = f"{index+1}. {self.file_names[index]}"

    def album_button_clicked(self):
        with open("album.txt", "r") as f:
            data = f.read()
            self.infolabel["text"] = data

    def playlist_button_clicked(self):
        with open("playlist.txt", "r") as f:
            data = f.read()
            self.infolabel["text"] = data

    def back_button_clicked(self):
        self.media_player.previous()
        x = self.media_player.get_media_player().get_media()
        index = self.media_list.index_of_item(x)
        self.infolabel["text"] = f"{index+1}. {self.file_names[index]}"

    def next_button_clicked(self):
        self.media_player.next()
        x = self.media_player.get_media_player().get_media()
        index = self.media_list.index_of_item(x)
        self.infolabel["text"] = f"{index+1}. {self.file_names[index]}"

    def pause_button_clicked(self):
        self.media_player.pause()
        x = self.media_player.get_media_player().get_media()
        index = self.media_list.index_of_item(x)
        self.infolabel["text"] = f"{index+1}. {self.file_names[index]}"

    def quit_button_clicked(self):
        self.quit()

if __name__ == "__main__":
    gui = tk.Tk()
    app = MusicPlayer(master=gui)
    app.mainloop()
