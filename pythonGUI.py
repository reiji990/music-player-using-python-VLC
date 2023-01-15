#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import subprocess
import os
import gc
import tkinter
from tkinter import ttk

# カレントディレクトリをこのファイルの絶対パスに変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# GUIアプリのデザイン
root = tkinter.Tk()
root.title(u"music player")

root.option_add('*font', ('', 30))
root.config(bg='black') 
root.option_add('*Button.background', 'gray')
root.option_add('*Entry.background','gray')
root.resizable(0,0)

static = tkinter.Label(text=u'Music Player for VLC',bg='black',fg='white',font=("",50))
static.grid(columnspan=3)


# 入力欄
artist = tkinter.Label(root, text=u'artist',bg='black',fg='white')
artist.grid(row=2,column=0)

album = tkinter.Label(root, text=u'album',bg='black',fg='white')
album.grid(row=3,column=0)

text1=tkinter.Entry(root, width=30)
text1.grid(row=2,column=1)

text2=tkinter.Entry(root, width=30)
text2.grid(row=3,column=1)

# pass.txtにリンク作成、別ファイルでpass.txtのリンクを取得、再生開始する関数(playボタンで実行)
def btnclick():
    text1in = str(text1.get())
    text2in = str(text2.get())
    path = open('path.txt', mode='w', encoding='utf-8')
    path.write('/System/Volumes/Data/Volumes/*/Music/*' + text1in + '*/*' + text2in + '*/*.flac' )
    path.close()
    import play
    root.destroy()

# playボタン
btnRead=tkinter.Button(root, text="Play", 
    command=btnclick)
btnRead.grid(row=5,columnspan=3)


gc.collect()
root.mainloop()