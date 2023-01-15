# 再生するアーティスト名、アルバム名の一部を入力すると、　フォルダ内の*.flacファイルを再生リスト化しループ再生開始
# その他基本的な音楽再生アプリの機能（e.g. 一時停止、トラックの変更）が行える
# ipadからの編集テスト

import vlc
import glob
import os
import gc

#カレントディレクトリをこのファイルの絶対パスに変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("*** start ***")

# *.flacファイルを再生リスト化
path = open('path.txt', mode='r')
data = path.read()
path.close
print(data)

glflac = sorted(glob.glob(data))
l = vlc.MediaList(glflac)

# album.txtの中身リセット
albumlist = open('album.txt', mode='w', encoding='utf-8')
albumlist.write('')
albumlist.close()

# アルバムリストtextファイル作成
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

#playlist リセット
playlist = open('playlist.txt', mode='w', encoding='utf-8')
playlist.write('')
playlist.close()

# playlist
filename = [os.path.basename(r) for r in glflac]
playlist = open('playlist.txt', mode='a', encoding='utf-8')

i = 0
while i < len(glflac):
    playlist.write(f"{i+1}. {(filename)[i]}\n")
    i += 1

playlist.close()

# メディアプレイヤーオブジェクトの作成、再生
p = vlc.MediaListPlayer()
p.set_media_list(l)
p.set_playback_mode(vlc.PlaybackMode.loop)
p.play()

# メモリ解放
gc.collect()

# プレイヤーウィンドウ表示
import tkinter
from tkinter import ttk
root = tkinter.Tk()
root.title(u"music player")

root.option_add('*font', ('', 30))
root.config(bg='black') 
root.option_add('*Button.background', 'gray')
root.option_add('*Entry.background','gray')
root.resizable(0,0)

static = tkinter.Label(text=u'Music Player for VLC',bg='black',fg='white',font=("",50))
static.grid(columnspan=3)

# input number to select track
#OK
selectnum=tkinter.Entry(root, width=15)
selectnum.grid(row=2,column=0)

# imfo label
#OK
imfolabel=tkinter.Label(root,text=u'imfomation',bg='black',fg='white')
imfolabel.grid(row=0,column=1,columnspan=2)

# 操作ボタンの機能の関数
def btnpauseclick():
    p.pause()

def btnimfoclick():
    x = p.get_media_player().get_media()
    index = l.index_of_item(x)
    print(f"now playing: {index+1}. {filename[index]}\n")

def btnnextclick():
    p.next()

    x = p.get_media_player().get_media()
    index = l.index_of_item(x)
    print(f"next: {filename[index]}")

def btnbackclick():
    p.previous()

    x = p.get_media_player().get_media()
    index = l.index_of_item(x)
    print(f"next: {filename[index]}")

def btnselectclick():
    print("slect the track number")
    track = int(input("> "))
    p.play_item_at_index(track-1)  

    x = p.get_media_player().get_media()
    index = l.index_of_item(x)
    print(f"next: {filename[index]}")

def btnquitclick():
    p.stop()
    del p
    del l
    del glflac
    gc.collect()

# 操作ボタンの追加
#OK
btnpause=tkinter.Button(root, text="Pause or Play", 
    command=btnpauseclick)
btnpause.grid(row=3,column=0,columnspan=2)

btnimfo=tkinter.Button(root, text="Imfomation", 
    command=btnimfoclick)
btnpause.grid(row=0,colum=0)

btnnext=tkinter.Button(root, text="Next track", 
    command=btnnextclick)
btnpause.grid(row=1,colum=0)

btnback=tkinter.Button(root, text="Back track", 
    command=btnbackclick)
btnpause.grid(row=1,colum=1)

btnselect=tkinter.Button(root, text="Select track", 
    command=btnselectclick)
btnpause.grid(row=2,colum=1)

btnquit=tkinter.Button(root, text="Quit", 
    command=btnquitclick)
btnpause.grid(row=3,colum=2)





while True:
    data = input("> ")

    #PAUSE / PLAY
    if data == 'p':
        p.pause()

    #IMFORMATION
    elif data == 'i':
        x = p.get_media_player().get_media()
        index = l.index_of_item(x)
        print(f"now playing: {index+1}. {filename[index]}\n")
        
    #NEXT
    elif data == 'n':
        p.next()

        x = p.get_media_player().get_media()
        index = l.index_of_item(x)
        print(f"next: {filename[index]}")

    #BACK
    elif data == 'b':
        p.previous()

        x = p.get_media_player().get_media()
        index = l.index_of_item(x)
        print(f"next: {filename[index]}")

    #SELECT
    elif data == 's':
        print("slect the track number")
        track = int(input("> "))
        p.play_item_at_index(track-1)  

        x = p.get_media_player().get_media()
        index = l.index_of_item(x)
        print(f"next: {filename[index]}")

    #QUIT
    elif data == 'q':
        p.stop()

        break   

# メモリの解放
del p
del l
del glflac
gc.collect()

print("*** end ***") 