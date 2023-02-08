# music-player-using-python-VLC 

Python-VLCを使ったミュージックプレイヤーです。  
GUI部分もPythonで書いており、Tkinterを使用しています。  
MacOS用に作成したものですが、Windowsでも動作します。但しUIデザインは異なります。  
始めにアーティスト名、アルバム名を入力し、Musicフォルダ内でワードが部分一致したアルバムを再生します。  

![画面収録 2023-02-08 23 12 26](https://user-images.githubusercontent.com/101491438/217554235-16e67bb5-3577-4164-950d-d43cb5389c38.gif)

# 事前準備

- Python実行環境
- VLCのインストール
- python-VLCの導入
- Musicフォルダの準備  
  Musicフォルダは、CDリッピング時やiTunes等で購入した時によく作成される下記構成の物をご準備ください。  
  Music/アーティスト名/アルバム名/.flacファイル  

# インストール後の操作

musicfolderpath.txtに再生するMusicフォルダのpathを入力してください。  
例:/Users/ユーザー名/Music  
あとはmusic player.pyを実行するだけ。  

# カスタマイズ

アプリの初期位置、フォントサイズは作成者のモニターに合わせて絶対値で設定しているので、こちらは各自調整した方が良いかもです。(music player.py, Lines 20-21)  
