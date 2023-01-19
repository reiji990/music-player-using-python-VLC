import sys
import subprocess
import os
import gc
import tkinter as tk
from tkinter import ttk
import vlc
import glob

# カレントディレクトリをこのファイルの絶対パスに変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# class
class Music_player(ttk.Frame):
    def __init__(root, master = None):
        super().__init__(master)
        root.master = master
        master.resizable(1000,1000)
        master.geometry('+1700+700')
        master.title('Music Player with python-VLC')
        master.option_add('*font', ('', 30))
        btnstyle = ttk.Style()
        btnstyle.configure('custom.TButton',font=(None,60))

# frame1 GUI
        root.frame1 = ttk.Frame(root.master)
        root.frame1.pack()
        root.artist = ttk.Label(root.frame1)
        root.artist.grid(row=0,column=0)
        root.artist['text'] = 'Artist'
        root.album = ttk.Label(root.frame1)
        root.album.grid(row=1,column=0)
        root.album['text'] = 'Album'
        root.input1 = ttk.Entry(root.frame1)
        root.input1.grid(row=0,column=1)
        root.input2 = ttk.Entry(root.frame1)
        root.input2.grid(row=1,column=1)
        root.btnplay = ttk.Button(root.frame1)
        root.btnplay.grid(row=2,column=0,columnspan=2)
        root.btnplay['text'] = 'Play'
        root.btnplay['style'] = 'custon.TButton'

# frame2
        def playframe():
                root.frame2 = ttk.Frame(root.master)
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
                gc.collect()

# frame2 GUI
                root.infolabel = tk.Message(root.frame2)
                root.infolabel.grid(row=3,column=0,columnspan=4)
                root.infolabel['text'] = f'{index+1}. {filename[index]}'
                root.infolabel['width'] = '400'
                root.backbtn = ttk.Button(root.frame2)
                root.backbtn.grid(row=2,column=0)
                root.backbtn['text'] = 'Back'
                root.backbtn['command'] = lambda:[backbtnfunc()]
                root.nextbtn = ttk.Button(root.frame2)
                root.nextbtn.grid(row=2,column=2)
                root.nextbtn['text'] = 'Next'
                root.nextbtn['command'] = lambda:[nextbtnfunc()]
                root.albumbtn = ttk.Button(root.frame2)
                root.albumbtn.grid(row=1,column=0)
                root.albumbtn['text'] = 'Album'
                root.albumbtn['command'] = lambda:[albumbtnfunc()]
                root.selectnum = ttk.Entry(root.frame2,width=5)
                root.selectnum.grid(row=0,column=0)
                root.selectbtn = ttk.Button(root.frame2)
                root.selectbtn.grid(row=0,column=1)
                root.selectbtn['text'] = 'Select'
                root.selectbtn['command'] = lambda:[selectbtnfunc()]
                root.playlistbtn = ttk.Button(root.frame2)
                root.playlistbtn.grid(row=1,column=1)
                root.playlistbtn['text'] = 'Playlist'
                root.playlistbtn['command'] = lambda:[playlistbtnfunc()]
                root.playpausebtn = ttk.Button(root.frame2)
                root.playpausebtn.grid(row=2,column=1)
                root.playpausebtn['text'] = 'Play / Pause'
                root.playpausebtn['command'] = lambda:[pausebtnfunc()]
                root.quitbtn = ttk.Button(root.frame2)
                root.quitbtn.grid(row=2,column=3)
                root.quitbtn['text'] = 'Quit'
                root.quitbtn['command'] = lambda:[quitbtnfunc()]
                
                def playlistbtnfunc():
                        f = open('playlist.txt','r')
                        data = f.read()
                        root.infolabel['text'] = data
                        master.resizable(1000,1000)
                def albumbtnfunc():
                        f = open('album.txt','r')
                        data = f.read()
                        root.infolabel['text'] = data
                        master.resizable(1000,1000)
                def nextbtnfunc():
                        p.next()
                        x = p.get_media_player().get_media()
                        index = l.index_of_item(x)
                        root.infolabel['text'] = f'{index+1}. {filename[index]}'
                def pausebtnfunc():
                        p.pause()
                        x = p.get_media_player().get_media()
                        index = l.index_of_item(x)
                        root.infolabel['text'] = f'{index+1}. {filename[index]}'
                def backbtnfunc():
                        p.previous()
                        x = p.get_media_player().get_media()
                        index = l.index_of_item(x)
                        root.infolabel['text'] = f'{index+1}. {filename[index]}'
                def selectbtnfunc():
                        track = int(root.selectnum.get())
                        root.selectnum.delete(0)
                        root.selectnum.delete(0)
                        root.selectnum.delete(0)
                        p.play_item_at_index(track-1)
                        x = p.get_media_player().get_media()
                        index = l.index_of_item(x)
                        root.infolabel['text'] = f'{index+1}. {filename[index]}'
                        master.resizable(1000,1000)
                def quitbtnfunc():
                        gc.collect()
                        root.quit()

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