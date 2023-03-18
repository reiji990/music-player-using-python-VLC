## music-player-using-python-VLC 

Python-VLCを使った.flacファイル用のミュージックプレイヤーです。  
GUI部分もPythonで書いており、Tkinterを使用しています。  
MacOS用に作成したものですが、Windowsでも動作します。但しUIデザインは異なります。  
始めにアーティスト名、アルバム名を入力すると、Musicフォルダ内でワードが部分一致したアルバム内の.flacファイルを再生します。  

![画面収録 2023-03-18 21 27 23](https://user-images.githubusercontent.com/101491438/226106478-b50e9510-fbc7-43fe-a426-54de8e486a00.gif)

## 事前準備

- Python実行環境
- VLCのインストール
- python-VLCの導入
- Musicフォルダの準備  
  Musicフォルダは、CDリッピング時やiTunes等で購入した時によく作成される下記構成の物をご準備ください。  
  Music/アーティスト名/アルバム名/.flacファイル  

## インストール後の操作

musicfolderpath.txtに再生するMusicフォルダのpathを入力してください。  
例:/Users/ユーザー名/Music  
あとはmusic player.pyを実行するだけ。  
