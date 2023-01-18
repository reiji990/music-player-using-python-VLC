import sys
import subprocess
import os
import gc
import tkinter as tk
from tkinter import ttk
import vlc
import glob
import threading

# カレントディレクトリをこのファイルの絶対パスに変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# class
class Music_player(tk.Frame):
    def __init__(root, master = None):
        super().__init__(master)
        root.master = master
        master.resizable(0,0)
        master.title('Music Player for VLC')
        master.option_add('*font', ('', 40))

# frame1 GUI
        root.frame1 = tk.Frame(root.master)
        root.frame1.pack()
        root.artist = tk.Label(root.frame1)
        root.artist.grid(row=0,column=0)
        root.artist['text'] = str('Artist')
        root.album = tk.Label(root.frame1)
        root.album.grid(row=1,column=0)
        root.album['text'] = str('Album')
        root.input1 = tk.Entry(root.frame1)
        root.input1.grid(row=0,column=1)
        root.input2 = tk.Entry(root.frame1)
        root.input2.grid(row=1,column=1)
        root.btnplay = tk.Button(root.frame1)
        root.btnplay.grid(row=2,column=0,columnspan=2)
        root.btnplay['text'] = str('Play')

# frame2
        def playframe():
                root.frame2 = tk.Frame(root.master)
                root.frame2.pack()
# 音楽再生
# *.flacファイルを再生リスト化
                path = open('path.txt', mode='r')
                data = path.read()
                path.close()
                print(data)
                
                glflac = sorted(glob.glob(data))
                l = vlc.MediaList(glflac)

# メディアプレイヤーオブジェクトの作成、再生
                p = vlc.MediaListPlayer()
                p.set_media_list(l)
                p.set_playback_mode(vlc.PlaybackMode.loop)
                p.play()

# album.txtの中身リセット
                albumlist = open('album.txt', mode='w', encoding='utf-8')
                albumlist.write('')
                albumlist.close()

# album.txtファイル作成
                allfoldername = [os.path.dirname(r) for r in glflac]

                foldername = []
                for element in allfoldername:
                        if element not in foldername:
                                foldername.append(element)

                i = 0
                while i < len(foldername):
                        albumlist = open('album.txt', mode='a', encoding='utf-8')
                        albumlist.write(f"{i+1}. {(foldername)[i]} \n")
                        i += 1

                albumlist.close()

# playlist.txt リセット
                playlist = open('playlist.txt', mode='w', encoding='utf-8')
                playlist.write('')
                playlist.close()

# playlist.txt作成
                filename = [os.path.basename(r) for r in glflac]
                playlist = open('playlist.txt', mode='a', encoding='utf-8')

                i = 0
                while i < len(glflac):
                        playlist.write(f"{i+1}. {(filename)[i]}\n")
                        i += 1

                playlist.close()

                info = p.get_media_player().get_media()
                index = l.index_of_item(info)

# frame2 GUI
                root.infolabel = tk.Label(root.frame2)
                root.infolabel.grid(row=0,column=0,columnspan=3)
                root.infolabel['text'] = f'now playing: {index+1}. {filename[index]}'


# Playbtnのコマンド内容
        def btnclick():
            text1in = str(root.input1.get())
            text2in = str(root.input2.get())
            path = open('path.txt', mode='w', encoding='utf-8')
            path.write('/System/Volumes/Data/Volumes/*/Music/*' + text1in + '*/*' + text2in + '*/*.flac' )
            path.close()
            root.frame1.destroy()
            playframe()


# playボタンのコマンド追加         
        root.btnplay['command']=btnclick



if __name__ == "__main__":
    gui = tk.Tk()
    app = Music_player(master = gui)
    app.mainloop()