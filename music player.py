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

# classの設定
class Music_player(ttk.Frame):
	# __init__() メソッドは、新しく作成されたオブジェクトを初期化します。定義されたクラスの新しいインスタンスが作成されるたびに呼び出されます。
	# 要するに、rootの中にインスタンスmaseterを設置した。
        def __init__(root, master = None):
                super().__init__(master)
                root.master = master
                master.resizable(1000,1000)
                master.geometry('+1700+700')
                master.title('Music Player with python-VLC')
                master.option_add('*font', ('', 30))

                # inputframe 各ウィジェット配置
                root.inputframe = ttk.Frame(root.master)
                root.inputframe.pack()
                
                #ボタンのスタイル設定
                root.style = ttk.Style(root.inputframe)
                root.style.configure('default.TButton', font=(None, 20))
                
                root.artist = ttk.Label(root.inputframe)
                root.artist.grid(row=0,column=0)
                root.artist['text'] = 'Artist'

                root.album = ttk.Label(root.inputframe)
                root.album.grid(row=1,column=0)
                root.album['text'] = 'Album'

                root.artistinput = ttk.Entry(root.inputframe)
                root.artistinput.grid(row=0,column=1)

                root.albuminput = ttk.Entry(root.inputframe)
                root.albuminput.grid(row=1,column=1)
                
                
                root.btnplay = ttk.Button(root.inputframe, width=20, style= 'default.TButton')
                root.btnplay.grid(row=2,column=0,columnspan=2)
                
                root.btnplay['text'] = 'Play'

                # Playbtnのコマンド内容
                def btnclick():
                        text1in = str(root.artistinput.get())
                        text2in = str(root.albuminput.get())
                        path = open('path.txt', mode='w', encoding='utf-8')
                        path.write('/System/Volumes/Data/Volumes/*/Music/*' + text1in + '*/*' + text2in + '*/*.flac' )
                        path.close()
                        root.inputframe.destroy()
                        framechange()

                # playbtnコマンド設定
                root.btnplay['command']=btnclick

                # frame切り替え、音楽再生開始関数(inputframeのplaybtnで実行)
                def framechange():
                        root.playframe = ttk.Frame(root.master)
                        root.playframe.pack()

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

                        # 再生中楽曲インデックスの取得
                        info = p.get_media_player().get_media()
                        index = l.index_of_item(info)
                        gc.collect()
                        
                        # ボタンのスタイル設定
                        root.style = ttk.Style(root.playframe)
                        root.style.configure('default.TButton', font=(None, 20))
                        
                        # playframe 各ウィジェット配置
                        root.selectnum = ttk.Entry(root.playframe,width=5)
                        root.selectnum.grid(row=0,column=0)

                        root.selectbtn = ttk.Button(root.playframe, style= 'default.TButton')
                        root.selectbtn.grid(row=0,column=1)
                        root.selectbtn['text'] = 'Select'
                        root.selectbtn['command'] = lambda:[selectbtnfunc()]
                        
                        root.albumbtn = ttk.Button(root.playframe, style= 'default.TButton')
                        root.albumbtn.grid(row=1,column=0)
                        root.albumbtn['text'] = 'Album'
                        root.albumbtn['command'] = lambda:[albumbtnfunc()]

                        root.backbtn = ttk.Button(root.playframe, style= 'default.TButton')
                        root.backbtn.grid(row=2,column=0)
                        root.backbtn['text'] = 'Back'
                        root.backbtn['command'] = lambda:[backbtnfunc()]

                        root.playlistbtn = ttk.Button(root.playframe, style= 'default.TButton')
                        root.playlistbtn.grid(row=1,column=1)
                        root.playlistbtn['text'] = 'Playlist'
                        root.playlistbtn['command'] = lambda:[playlistbtnfunc()]

                        root.playpausebtn = ttk.Button(root.playframe, style= 'default.TButton')
                        root.playpausebtn.grid(row=2,column=1)
                        root.playpausebtn['text'] = 'Play / Pause'
                        root.playpausebtn['command'] = lambda:[pausebtnfunc()]

                        root.nextbtn = ttk.Button(root.playframe, style= 'default.TButton')
                        root.nextbtn.grid(row=2,column=2)
                        root.nextbtn['text'] = 'Next'
                        root.nextbtn['command'] = lambda:[nextbtnfunc()]

                        root.quitbtn = ttk.Button(root.playframe, style= 'default.TButton')
                        root.quitbtn.grid(row=2,column=3)
                        root.quitbtn['text'] = 'Quit'
                        root.quitbtn['command'] = lambda:[quitbtnfunc()]

                        root.infolabel = tk.Message(root.playframe)
                        root.infolabel.grid(row=3,column=0,columnspan=4)
                        root.infolabel['text'] = f'{index+1}. {filename[index]}'
                        root.infolabel['width'] = '400'

                        # playframe 各ウィジェットの機能                
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
                        def albumbtnfunc():
                                f = open('album.txt','r')
                                data = f.read()
                                root.infolabel['text'] = data
                                master.resizable(1000,1000)
                        def playlistbtnfunc():
                                f = open('playlist.txt','r')
                                data = f.read()
                                root.infolabel['text'] = data
                                master.resizable(1000,1000)
                        def backbtnfunc():
                                p.previous()
                                x = p.get_media_player().get_media()
                                index = l.index_of_item(x)
                                root.infolabel['text'] = f'{index+1}. {filename[index]}'
                        def pausebtnfunc():
                                p.pause()
                                x = p.get_media_player().get_media()
                                index = l.index_of_item(x)
                                root.infolabel['text'] = f'{index+1}. {filename[index]}'
                        def nextbtnfunc():
                                p.next()
                                x = p.get_media_player().get_media()
                                index = l.index_of_item(x)
                                root.infolabel['text'] = f'{index+1}. {filename[index]}'
                        def quitbtnfunc():
                                gc.collect()
                                root.quit()

if __name__ == '__main__':
    gui = tk.Tk()
    app = Music_player(master = gui)
    app.mainloop()