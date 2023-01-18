#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import subprocess
import os
import gc
import tkinter
from tkinter import ttk
import vlc
import glob
import tkmacosx

# カレントディレクトリをこのファイルの絶対パスに変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# GUIアプリのデザイン
root = tkinter.Tk()
root.title(u"music player")

root.option_add('*font', ('', 30))
root.config(bg='black') 
root.option_add('*Button.background', 'blue')
root.option_add('*Entry.background','gray')
root.option_add('*Label.background*','black')

# frame1
frame1 = tkinter.Frame(root, bg='black')
frame1.pack()

# title
title1 = tkinter.Label(frame1,text=u'Music Player for VLC',bg='black',fg='white',font=("",50))
title1.grid(columnspan=3)

# input
artist = tkinter.Label(frame1, text=u'artist',bg='black',fg='white')
artist.grid(row=2,column=0)

album = tkinter.Label(frame1, text=u'album',bg='black',fg='white')
album.grid(row=3,column=0)

text1=tkinter.Entry(frame1, width=30)
text1.grid(row=2,column=1)

text2=tkinter.Entry(frame1, width=30)
text2.grid(row=3,column=1)

# frame2
def playframe():
    frame2 = tkinter.Frame(root, bg='black')
    frame2.pack()

# 音楽再生
# *.flacファイルを再生リスト化
    path = open('path.txt', mode='r')
    data = path.read()
    path.close
    print(data)

    glflac = sorted(glob.glob(data))
    l = vlc.MediaList(glflac)

# メディアプレイヤーオブジェクトの作成、再生
    p = vlc.MediaListPlayer()
    p.set_media_list(l)
    p.set_playback_mode(vlc.PlaybackMode.loop)
    p.play()

# メモリ解放
    gc.collect()


# title2
    title2 = tkinter.Label(frame2,text=u'Music Player for VLC',bg='black',fg='white',font=("",50))
    title2.grid(columnspan=3)

# imfo label
    imfolabel=tkinter.Label(frame2,text=u'now playing: {index+1}. {filename[index]}',bg='black',fg='white')
    imfolabel.grid(row=1,column=0,columnspan=3)

# next track btn
    selectbtn=tkinter.Button(frame2,text=u'next track', width=20,command=lambda:[p.next()])
    selectbtn.grid(row=2,column=0)

# back track btn
    selectbtn=tkinter.Button(frame2,text=u'back track', width=20,command=lambda:[p.previous()])
    selectbtn.grid(row=2,column=1)

# albumlist btn
    selectbtn=tkinter.Button(frame2,text=u'Album List',bg='black',fg='white', width=20)
    selectbtn.grid(row=2,column=2)

# input number to select track
    selectnum=tkinter.Entry(frame2, width=20)
    selectnum.grid(row=3,column=0)

# select track btn
    selectbtn=tkinter.Button(frame2,text=u'select track',bg='black',fg='white', width=20)
    selectbtn.grid(row=3,column=1)

# playlist btn
    selectbtn=tkinter.Button(frame2,text=u'Playlist',bg='black',fg='white', width=20)
    selectbtn.grid(row=3,column=2)

# play pause btn
    selectbtn=tkinter.Button(frame2,text=u'Play / Pause',bg='black',fg='white', width=20,command=lambda:[p.pause()])
    selectbtn.grid(row=4,column=0,columnspan=2)

# quit btn
    selectbtn=tkinter.Button(frame2,text=u'Quit',bg='black',fg='white', width=20,command=lambda:[p.stop()])
    selectbtn.grid(row=4,column=2)

# pass.txtにリンク作成、frame1を消去、frame2に切替後、リンク取得して再生開始。
def btnclick():
    text1in = str(text1.get())
    text2in = str(text2.get())
    path = open('path.txt', mode='w', encoding='utf-8')
    path.write('/System/Volumes/Data/Volumes/*/Music/*' + text1in + '*/*' + text2in + '*/*.flac' )
#    path.write('C:/Users/834296/マイドライブ/music/*' + text1in + '*/*' + text2in + '*/*.flac' )
    path.close()

# frame1削除
    frame1.destroy()

# frame2作成
    playframe()

# playボタン
btnRead=tkinter.Button(frame1, text="Play", bg='black',
    command=btnclick)
btnRead.grid(row=5,columnspan=3)

gc.collect()
root.mainloop()