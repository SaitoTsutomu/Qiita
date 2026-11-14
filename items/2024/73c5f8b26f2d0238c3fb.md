title: NiceGUIの紹介
tags: Python WebAPI Webアプリケーション nicegui
url: https://qiita.com/SaitoTsutomu/items/73c5f8b26f2d0238c3fb
created_at: 2024-09-28 21:43:42+09:00
updated_at: 2025-03-05 05:17:15+09:00
body:

## NiceGUIとは

NiceGUIは、PythonでWebアプリケーションやWebAPIを作成するためのフレームワークです。

https://nicegui.io/

### 特徴

* シンプルな構文
* リアルタイム更新
* 豊富なウィジェット
* レスポンシブデザイン
* スタイルのカスタマイズ

## 動かしてみよう

JupyterLabで、簡単なサンプルを通してできることを確かめてみましょう。

2つのノートブックファイルを用意しました。次のリンク先の右上の`Download ZIP`ボタンを押してください。

[NiceGUI紹介用のgist](https://gist.github.com/SaitoTsutomu/a4c29457b1372d477bc5d517c7b19d6b)

ダウンロードしたファイルを解凍すると、`NiceGUI.ipynb`と`NiceGUI_browse.ipynb`ができます。
これらのファイルのある場所で作業してください。

## 手順

macOSでの手順を紹介します。Windowsの方は適宜読みかえてください。

次のように仮想環境を作成してください。

```
python3.12 -m venv venv
source venv/bin/activate
pip install nicegui jupyterlab pandas plotly
```

まずは、JupyterLabを起動します。

```zsh
jupyter lab
```

Jupyterでダウンロードした2つのノートブックを開いてください。
`NiceGUI_browse.ipynb`の方を右にドラッグして次のようにしてください。

![スクリーンショット 2024-09-28 21.07.10.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/226d3a92-333e-4a67-5d00-6aa27b0c7ca3.png)

左のノートブックを順に実行していきます。
「Hello world」の下のセルは、セルの内容をファイルに出力するようになっています。

```python:セル
%%file demo.py

from nicegui import ui

ui.label("Hello world!")

ui.run()
```

このセルを実行すると、`demo.py`というファイルが作成されます。

JupyterLabを起動したターミナルとは別のターミナルから、次のようにして`demo.py`を起動しましょう。

```zsh
source venv/bin/activate
python demo.py
```

新しくブラウザが開きますが、閉じてください。
JupyterLabに戻って、`NiceGUI_browse.ipynb`の最初のセルを実行してください。
InnerFrameで、NiceGUIの画面が確認できます。

以降はノートブックの簡単な解説です。

### Hello world

このサンプルでは、単に「Hello world!」と表示されます。

### ボタン

「ボタン」の下のセルを実行すると、`demo.py`が上書きされます。niceguiがホットリロードで起動されているので、自動的に再実行されます。
少し待つと、画面右の`NiceGUI_browse.ipynb`の画面が変わります。

右の画面の「PUSH」を押すと、ラベルの文字が「Clicked!」に変わります。

### スタイル

このサンプルではボタンを押すとラベルのスタイルを変更して赤くします。

### マークダウンなど

コードにUIの部品を書くと、Streamlitのように画面に表示されます。
ここでは、マークダウンとマーメイドの図と日付入力を表示しています。

### レイアウト

2行2列のラベル表示と、カードという表示のサンプルです。

### バインド

ラベルの文字を、日付の値にバインドしています。
この結果、日付を変えるとラベルの文字が自動で変わります。

### グリッド

pandasのDataFrameをグリッドを使って表示しています。

### グラフ

plotlyのグラフのサンプルです。

### 動画

動画の埋め込みのサンプルです。

### インタラクティブイメージ

インタラクティブイメージのサンプルです。
画像をクリックすると水色の丸が描画されます。

### ルーティング

最初にリンクが表示されています。リンクをクリックすると別のページに移動します。
JupyterLabでは、InnerFrameで表示されているのでわかりませんが、URLが変わっています。

次のセルを実行すると、`top`という関数にトップページを定義します。
また、クリック先のページからトップページに戻るリンクも追加しているので、行ったり来たりできます。

### API

WebAPIのサンプルです。
このように、NiceGUIでは、WebアプリケーションとWebAPIを両方作成できます。

ここで紹介した以外にもいろいろなことができるようです。次のExamplesも参考にしてみてください。

https://nicegui.io/#examples

## 電卓アプリケーション

[fletのGallery](https://flet.dev/gallery/)にあるCalculatorのUIを真似て電卓を作ってみました。下記のように実行できます。

```zsh
pip install -U nicegui-calculator
calculator
```

![](https://raw.githubusercontent.com/SaitoTsutomu/nicegui-calculator/master/images/main.png)

このUI構築のメインは[7行](https://github.com/SaitoTsutomu/nicegui-calculator/blob/master/src/nicegui_calculator/main.py#L21-L27)です！シンプルですね。

```python
with ui.card().classes("rounded-2xl bg-black"):
    label = ui.label().classes("text-xl w-full text-right text-white")
    label.bind_text(calculator, "value")
    for row in rows:
        with ui.row():
            for text, i in row:
                ui.button(text, on_click=calculator.act).classes(button_styles[i])
```

## pytest

pytestのGUI用のフィクスチャが用意されています。そのため、GUIのテストを簡単に記述できます。
詳しくは、次を参照してください。

https://qiita.com/SaitoTsutomu/items/9800bfe7d2b31b9f2c59

## さいごに

ちょっと動かしてみた印象です。

* 構文がわかりやすい
* Streamlitより本格的なWebアプリケーションを作りやすそう
* Djangoのような本格的なWebアプリケーション向けではなさそう

以上

